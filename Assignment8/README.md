# Assignment 8 — Monitor a Machine Learning Model Using Prometheus and Grafana

This project serves a Scikit-learn Iris classifier through FastAPI, exports operational metrics in Prometheus format, scrapes those metrics with Prometheus, and visualizes them in Grafana.

## Project files

- `train_model.py` — trains and saves a Random Forest classifier using the Iris dataset.
- `app.py` — FastAPI prediction service and Prometheus instrumentation.
- `prometheus/prometheus.yml` — Prometheus scrape configuration.
- `docker-compose.yml` — runs the API, Prometheus and Grafana.
- `grafana/` — provisions the Prometheus data source and monitoring dashboard.
- `load_test.py` — sends valid and invalid prediction requests to create monitoring traffic.
- `tests/test_api.py` — basic API and metrics tests.

## Exported metrics

- `ml_prediction_requests_total` — prediction endpoint requests, labeled by method and HTTP status.
- `ml_prediction_errors_total` — failed prediction endpoint requests, labeled by bounded error reason.
- `ml_prediction_latency_seconds` — prediction endpoint request latency histogram.
- `ml_predictions_total` — successful predictions, labeled by predicted class.

## Run with Docker Compose

From this directory, run `docker compose up --build -d`.

- FastAPI docs: `http://localhost:8000/docs`
- Metrics: `http://localhost:8000/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (initial local credentials: `admin` / `admin`; change them before any non-local deployment).

Prometheus scrapes `app:8000` because services address one another by their Compose service names on the Compose network.

## Generate traffic

Install the local client dependency if needed, then run `python load_test.py` from this directory. The script sends mostly valid requests and one invalid request in every ten requests. Observe the Grafana dashboard and Prometheus queries after traffic has been generated.

## Run tests locally

Install dependencies with `pip install -r requirements.txt`, then run `pytest -q`. The API trains the model automatically at startup if the model artifact is absent.

## Important scope note

This implementation monitors serving operations (request volume, latency, errors and scrape availability). It does not measure model drift or production prediction accuracy because those require additional reference data and/or ground-truth labels. CPU and memory panels require an additional host/container metrics exporter and are not included in this baseline.

The default Grafana credentials are for a local demonstration only. Do not expose these services publicly with default credentials.
