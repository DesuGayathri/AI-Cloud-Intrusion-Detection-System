import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

os.makedirs("model", exist_ok=True)

data = pd.read_csv("data/cloud_logs.csv")

X = data[['cpu_usage', 'memory_usage', 'login_attempts']]

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

joblib.dump(model, "model/isolation_forest.pkl")
print("Model trained and saved!")
