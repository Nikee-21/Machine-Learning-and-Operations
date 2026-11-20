import os
import joblib
import pandas as pd

from sklearn.metrics import accuracy_score


# Test 1: Check whether model file exists
def test_model_exists():
    assert os.path.exists("artifacts/model.pkl")


# Test 2: Check whether accuracy file exists
def test_accuracy_exists():
    assert os.path.exists("artifacts/accuracy.txt")


# Test 3: Check model accuracy
def test_model_accuracy():
    with open("artifacts/accuracy.txt", "r") as file:
        accuracy = float(file.read())

    assert accuracy >= 0.80, "Model accuracy is below 80%"


# Test 4: Check prediction functionality
def test_prediction():
    model = joblib.load("artifacts/model.pkl")

    student = pd.DataFrame([{
        "CGPA": 8.5,
        "Attendance": 92,
        "CodingScore": 85,
        "Projects": 3,
        "Internship": 1
    }])

    prediction = model.predict(student)[0]

    assert prediction in [0, 1]


# Test 5: Check prediction output
def test_prediction_output():
    model = joblib.load("artifacts/model.pkl")

    student = pd.DataFrame([{
        "CGPA": 5.8,
        "Attendance": 62,
        "CodingScore": 45,
        "Projects": 1,
        "Internship": 0
    }])

    prediction = model.predict(student)[0]

    assert prediction == 0