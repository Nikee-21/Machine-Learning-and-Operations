from pathlib import Path
import joblib

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# 1. Load Iris dataset
iris = load_iris()

X = iris.data
y = iris.target

# 2. Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 3. Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# 4. Evaluate model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Training Completed!")
print("Model Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=iris.target_names))

# 5. Save model and metadata
model_bundle = {
    "model": model,
    "target_names": iris.target_names.tolist(),
    "feature_names": iris.feature_names,
    "test_accuracy": float(accuracy),
    "model_version": "1.0.0"
}

Path("artifacts").mkdir(exist_ok=True)

joblib.dump(model_bundle, "artifacts/iris_model.joblib")

print("\nModel Saved Successfully!")
print("Location: artifacts/iris_model.joblib")