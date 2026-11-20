from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field


MODEL_PATH = Path("artifacts/iris_model.joblib")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MODEL_PATH.exists():
        raise RuntimeError("Model not found. Run train_model.py first.")

    app.state.model_bundle = joblib.load(MODEL_PATH)
    yield
    app.state.model_bundle = None


app = FastAPI(
    title="Iris Classification API",
    description="Machine Learning Model Serving using FastAPI",
    version="1.0.0",
    lifespan=lifespan
)


class PredictionRequest(BaseModel):
    sepal_length: float = Field(gt=0, le=20)
    sepal_width: float = Field(gt=0, le=20)
    petal_length: float = Field(gt=0, le=20)
    petal_width: float = Field(gt=0, le=20)


@app.get("/")
def root():
    return {
        "message": "Welcome to Iris Classification API",
        "documentation": "/docs"
    }


@app.get("/health")
def health(request: Request):
    return {
        "status": "healthy",
        "model_loaded": request.app.state.model_bundle is not None
    }


@app.get("/model-info")
def model_info(request: Request):
    bundle = request.app.state.model_bundle

    return {
        "model_type": type(bundle["model"]).__name__,
        "model_version": bundle["model_version"],
        "feature_names": bundle["feature_names"],
        "target_names": bundle["target_names"],
        "test_accuracy": bundle["test_accuracy"]
    }


@app.post("/predict")
def predict(data: PredictionRequest, request: Request):

    bundle = request.app.state.model_bundle
    model = bundle["model"]

    features = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])

    try:
        prediction = int(model.predict(features)[0])
        probabilities = model.predict_proba(features)[0]

        probability_dict = {
            name: round(float(probability), 4)
            for name, probability in zip(
                bundle["target_names"], probabilities
            )
        }

        return {
            "predicted_class": prediction,
            "predicted_species": bundle["target_names"][prediction],
            "confidence": round(float(probabilities[prediction]), 4),
            "probabilities": probability_dict,
            "model_version": bundle["model_version"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed."
        ) from error