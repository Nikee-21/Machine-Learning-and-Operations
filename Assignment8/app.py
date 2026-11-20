from pathlib import Path
import time
from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, make_asgi_app

from train_model import train_and_save_model, MODEL_PATH

REQUESTS = Counter(
    "ml_prediction_requests_total",
    "Total number of requests to the prediction endpoint",
    ["method", "status"],
)
ERRORS = Counter(
    "ml_prediction_errors_total",
    "Total number of failed prediction requests",
    ["reason"],
)
LATENCY = Histogram(
    "ml_prediction_latency_seconds",
    "Prediction endpoint request latency in seconds",
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)
PREDICTIONS = Counter(
    "ml_predictions_total",
    "Total number of successful model predictions",
    ["predicted_class"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MODEL_PATH.exists():
        train_and_save_model()
    bundle = joblib.load(MODEL_PATH)
    app.state.model = bundle["model"]
    app.state.feature_names = bundle["feature_names"]
    app.state.target_names = bundle["target_names"]
    yield


app = FastAPI(
    title="Iris Prediction API with Prometheus Monitoring",
    description="A Scikit-learn Iris classifier instrumented with Prometheus metrics.",
    version="1.0.0",
    lifespan=lifespan,
)


class IrisFeatures(BaseModel):
    sepal_length: float = Field(gt=0, le=10)
    sepal_width: float = Field(gt=0, le=10)
    petal_length: float = Field(gt=0, le=10)
    petal_width: float = Field(gt=0, le=10)


@app.middleware("http")
async def monitor_prediction_requests(request: Request, call_next):
    if request.url.path != "/predict":
        return await call_next(request)

    start = time.perf_counter()
    status = "500"
    try:
        response = await call_next(request)
        status = str(response.status_code)
        if response.status_code >= 400:
            ERRORS.labels(reason=f"http_{response.status_code}").inc()
        return response
    except Exception:
        ERRORS.labels(reason="internal_error").inc()
        raise
    finally:
        elapsed = time.perf_counter() - start
        LATENCY.observe(elapsed)
        REQUESTS.labels(method=request.method, status=status).inc()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(features: IrisFeatures, request: Request):
    model = request.app.state.model
    target_names = request.app.state.target_names
    values = [[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]]
    prediction = int(model.predict(values)[0])
    label = target_names[prediction]
    PREDICTIONS.labels(predicted_class=label).inc()
    return {"prediction": prediction, "class_name": label}


app.mount("/metrics", make_asgi_app())
