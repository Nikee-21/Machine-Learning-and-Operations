import joblib
import pandas as pd

# Load trained model
model = joblib.load("artifacts/model.pkl")

# Sample student data
student = pd.DataFrame([{
    "CGPA": 8.5,
    "Attendance": 92,
    "CodingScore": 85,
    "Projects": 3,
    "Internship": 1
}])

# Predict placement
prediction = model.predict(student)[0]

if prediction == 1:
    print("Student Placement Prediction: PLACED")
else:
    print("Student Placement Prediction: NOT PLACED")