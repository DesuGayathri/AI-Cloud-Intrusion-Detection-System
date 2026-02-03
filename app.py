'''from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("model/isolation_forest.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    df = pd.DataFrame([data])

    score = model.decision_function(df)[0]
    risk = int((1 - score) * 100)

    return jsonify({"risk_score": risk})

if __name__ == "__main__":
    app.run(debug=True)'''



from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
model = joblib.load("model/isolation_forest.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    cpu = data['cpu_usage']
    memory = data['memory_usage']
    logins = data['login_attempts']

    features = pd.DataFrame(
        [[cpu, memory, logins]],
        columns=["cpu_usage", "memory_usage", "login_attempts"])

    anomaly_score = model.decision_function(features)[0]
    risk_score = int((1 - anomaly_score) * 100)
    risk_score = max(0, min(100, risk_score))


    # ---- Simulated Risk Score (replace with Isolation Forest output) ----
    risk_score = min(100, int((cpu + memory + logins) / 3))

    # ---- Rule-based interpretation (very common in SOC systems) ----
    if risk_score < 30:
        attack_type = "Normal Activity"
        affected_resource = "None"
        recommended_action = "No action required. Continue monitoring."
    
    elif risk_score < 70:
        attack_type = "Suspicious Activity"
        affected_resource = "Compute Instance"
        recommended_action = "Monitor traffic and review system logs."

    else:
        attack_type = "Brute Force / Resource Abuse"
        affected_resource = "Authentication & VM Resources"
        recommended_action = "Block IP, enable MFA, and isolate affected VM."

    return jsonify({
        "risk_score": risk_score,
        "attack_type": attack_type,
        "affected_resource": affected_resource,
        "recommended_action": recommended_action
    })

if __name__ == '__main__':
    app.run(debug=True)

