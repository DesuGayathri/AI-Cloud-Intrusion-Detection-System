'''import pandas as pd
import numpy as np
import joblib
import os

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

print("Loading cleaned dataset...")

df = pd.read_csv("clean_dataset.csv")

print("Dataset shape:", df.shape)

# Isolation Forest performs better when scaled
scaler = StandardScaler()

# MODEL (ZERO-DAY DETECTION)

model = IsolationForest(
    n_estimators=200,      
    contamination=0.05,    
    random_state=42,
    n_jobs=-1              
)

# CREATE PIPELINE (INDUSTRY STYLE)

pipeline = Pipeline([
    ("scaler", scaler),
    ("model", model)
])

print("Training model...")

pipeline.fit(df)

print("Training completed")

# SAVE MODEL
os.makedirs("model", exist_ok=True)
joblib.dump(pipeline, "model/isolation_forest_pipeline.pkl")

print("Model saved successfully")

# Calculate risk scores preview

scores = pipeline.named_steps["model"].decision_function(
    pipeline.named_steps["scaler"].transform(df)
)

risk_scores = (1 - scores) * 100

print("Sample risk scores:")
print(risk_scores[:10]) '''

import pandas as pd
import numpy as np
import joblib
import os

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

print("Loading cleaned dataset...")

df = pd.read_csv("clean_dataset.csv")

print("Dataset shape:", df.shape)

# SAFETY CHECK

if df.isnull().sum().sum() > 0:
    print("WARNING: Null values detected. Filling with 0.")
    df.fillna(0, inplace=True)

# CREATE PIPELINE

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42,
        n_jobs=-1
    ))
])

print("Training model...")

pipeline.fit(df)

print("Training completed")

# SAVE MODEL

os.makedirs("model", exist_ok=True)

MODEL_PATH = "model/isolation_forest_pipeline.pkl"
joblib.dump(pipeline, MODEL_PATH)

print("Model saved successfully at:", MODEL_PATH)

# TEST RISK SCORES 

scores = pipeline.decision_function(df)

risk_scores = (1 - scores) * 100

print("\nSample risk scores:")
print(risk_scores[:10])

# Show features used by model 
print("\nModel feature order:")
print(pipeline.feature_names_in_)

