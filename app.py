from flask import Flask, jsonify, render_template
import joblib
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

print("Loading model...")


# LOAD MODEL


MODEL_PATH = "model/isolation_forest_pipeline.pkl"

if not os.path.exists(MODEL_PATH):
    raise Exception("Model not found!")

pipeline = joblib.load(MODEL_PATH)

print("Model loaded successfully")


# LOAD DATASET (LIVE STREAM)


DATASET_PATH = "clean_dataset.csv"

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded:", df.shape)

current_index = 0


# ATTACK CLASSIFICATION

def classify_attack(data, risk):

    if data["Total Fwd Packets"] > 10000:
        return "DDoS Attack", "Network Gateway", "Block suspicious IP"

    elif data["SYN Flag Count"] > 50:
        return "Port Scanning", "Firewall", "Enable IPS rules"

    elif data["Flow Bytes/s"] > 1000000:
        return "Data Exfiltration", "Storage Service", "Investigate outbound traffic"

    elif risk > 70:
        return "Unknown Zero-Day Behaviour", "Cloud Infrastructure", "Isolate instance"

    return "Normal Activity", "None", "No action required"

def send_email_alert(risk, attack):

    msg = MIMEText(f"High Risk Detected\nRisk Score: {risk}\nAttack: {attack}")
    msg["Subject"] = "AI Cloud Security Alert"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "receiver_email@gmail.com"

    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("your_email@gmail.com","APP_PASSWORD")
    server.send_message(msg)
    server.quit()


# ROUTES


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/auto_predict")
def auto_predict():
    
    global current_index
    
    try:

        # LOOP DATASET LIKE LIVE STREAM
        row = df.iloc[current_index]

        current_index += 1

        if current_index >= len(df):
            current_index = 0

        data_dict = row.to_dict()

        input_df = pd.DataFrame([data_dict])

        # ML PREDICTION
        score = pipeline.decision_function(input_df)[0]

        risk = int(max(0, min(100, (1 - score) * 100)))

        attack_type, resource, action = classify_attack(data_dict, risk)

        return jsonify({
            "risk_score": risk,
            "attack_type": attack_type,
            "affected_resource": resource,
            "recommended_action": action
        })
        if risk > 70:
            send_email_alert(risk, attack_type)

    except Exception as e:
        return jsonify({"error": str(e)})
    
    

if __name__ == "__main__":
    app.run(debug=True)
