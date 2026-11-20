import pandas as pd
import numpy as np
import joblib
import os

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif

# Create folders
os.makedirs("models", exist_ok=True)
os.makedirs("output", exist_ok=True)

# STEP 1: Load Dataset
raw = pd.read_csv("data/adult.csv", header=None)

# Fix quoted CSV format
df = raw[0].str.split(",", expand=True)
df.columns = df.iloc[0].str.strip()
df = df.iloc[1:].reset_index(drop=True)

print("Dataset Loaded Successfully")
print("Original Shape:", df.shape)

# STEP 2: Data Cleaning
df = df.apply(lambda col: col.str.strip())
df.replace("?", np.nan, inplace=True)
df.drop_duplicates(inplace=True)

# Convert numerical columns
num_cols = [
    "age", "fnlwgt", "educational-num",
    "capital-gain", "capital-loss", "hours-per-week"
]

for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df.dropna(subset=["income"], inplace=True)

print("Missing values identified and handled")
print("Duplicates removed")

# STEP 3: Separate Features and Target
X = df.drop("income", axis=1)
y = df["income"]

cat_cols = X.select_dtypes(include="object").columns.tolist()

# STEP 4: Numerical Pipeline
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# STEP 5: Categorical Pipeline
cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# STEP 6: Column Transformer
preprocessor = ColumnTransformer([
    ("num", num_pipeline, num_cols),
    ("cat", cat_pipeline, cat_cols)
])

# STEP 7: Feature Selection
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("feature_selection", SelectKBest(score_func=f_classif, k=10))
])

# Transform Dataset
X_transformed = pipeline.fit_transform(X, y)

# Get selected feature names
all_features = pipeline.named_steps[
    "preprocessor"
].get_feature_names_out()

selected_features = all_features[
    pipeline.named_steps["feature_selection"].get_support()
]

print("\nSelected Features:")
print(selected_features)

print("\nTransformed Shape:", X_transformed.shape)

# STEP 8: Save Transformed Dataset
if hasattr(X_transformed, "toarray"):
    X_transformed = X_transformed.toarray()

result = pd.DataFrame(
    X_transformed,
    columns=selected_features
)

result.to_csv("output/transformed_data.csv", index=False)

# STEP 9: Save Pipeline
joblib.dump(pipeline, "models/feature_pipeline.pkl")

print("\nPipeline Saved Successfully")

# STEP 10: Reuse Pipeline
loaded_pipeline = joblib.load("models/feature_pipeline.pkl")

sample = X.iloc[[0]]
new_result = loaded_pipeline.transform(sample)

print("\nSaved Pipeline Loaded Successfully")
print("New Sample Transformed Successfully")
print("New Sample Shape:", new_result.shape)

print("\nAssignment Completed Successfully!")