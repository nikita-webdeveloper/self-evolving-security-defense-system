import datetime
import json
import os


def generate_alerts(df):
    alerts = []

    for _, row in df.iterrows():
        if row["threat_level"] == "ATTACK":
            severity = "HIGH"
        elif row["threat_level"] == "SUSPICIOUS":
            severity = "MEDIUM"
        else:
            severity = "LOW"

        alert = {
            "timestamp": str(datetime.datetime.now()),
            "severity": severity,
            "anomaly_score": float(row["anomaly_score"]),
            "threat_level": row["threat_level"]
        }

        alerts.append(alert)

    os.makedirs("results", exist_ok=True)

    with open("results/alerts.log", "a") as f:
        for alert in alerts:
            f.write(json.dumps(alert) + "\n")

    print("🚨 Alerts generated and logged")
