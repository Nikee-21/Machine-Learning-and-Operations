from fastapi.testclient import TestClient
from main import app


def test_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome" in response.json()["message"]


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["model_loaded"] is True


def test_model_info():
    with TestClient(app) as client:
        response = client.get("/model-info")
        assert response.status_code == 200
        assert response.json()["model_type"] == "RandomForestClassifier"


def test_prediction():
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        )

        assert response.status_code == 200

        result = response.json()

        assert result["predicted_species"] in [
            "setosa", "versicolor", "virginica"
        ]

        assert 0 <= result["confidence"] <= 1


def test_invalid_input():
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json={
                "sepal_length": -5,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        )

        assert response.status_code == 422


def test_missing_input():
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5
            }
        )

        assert response.status_code == 422