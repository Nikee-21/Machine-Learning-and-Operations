import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Dataset path
DATA_PATH = "data/student_placement.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully!")
print("Dataset Shape:", df.shape)

# Validate dataset
required_columns = [
    "CGPA",
    "Attendance",
    "CodingScore",
    "Projects",
    "Internship",
    "Placement"
]

if not all(column in df.columns for column in required_columns):
    raise ValueError("Missing required columns!")

if df.isnull().values.any():
    raise ValueError("Dataset contains missing values!")

if df.duplicated().any():
    raise ValueError("Dataset contains duplicate records!")

if not set(df["Placement"].unique()).issubset({0, 1}):
    raise ValueError("Invalid placement labels!")

print("Data Validation Successful!")

# Separate features and target
X = df.drop("Placement", axis=1)
y = df["Placement"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=1,
    stratify=y
)

# Train Decision Tree model
model = DecisionTreeClassifier(random_state=1)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model
os.makedirs("artifacts", exist_ok=True)

joblib.dump(model, "artifacts/model.pkl")

# Save accuracy
with open("artifacts/accuracy.txt", "w") as file:
    file.write(str(accuracy))

print("Model saved successfully!")