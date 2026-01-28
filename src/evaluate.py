import pandas as pd
from src.model import load_model
import json
import os

ATTACK_THRESHOLD = -0.01

FEATURE_PATH = "data/processed/features.csv"
MODEL_PATH = "models/ids_model_latest.pkl"
COUNT_PATH = "results/processed_count.json"
LOGS_PATH = "results/processed_logs.json"



def get_processed_log_count():
    if os.path.exists(COUNT_PATH):
        with open(COUNT_PATH, "r") as f:
            data = json.load(f)
            return data.get("last_processed_count", 0)
    return 0



def save_processed_log_count(count):
    os.makedirs("results", exist_ok=True)
    with open(COUNT_PATH, "w") as f:
        json.dump({"last_processed_count": count}, f)



def evaluate_logs():
    df = pd.read_csv(FEATURE_PATH)

    last_processed = get_processed_log_count()
    current_total = len(df)

    if last_processed >= current_total:
        return None

    new_df = df.iloc[last_processed:].copy()

    model = load_model(MODEL_PATH)

    predictions = model.predict(new_df)
    scores = model.decision_function(new_df)

    new_df["anomaly"] = predictions
    new_df["anomaly_score"] = scores

    def classify(row):
        if row["attempt_score"] > 0.7 or row["anomaly_score"] < -0.3:
            return "ATTACK"
        elif row["attempt_score"] > 0.2 or row["anomaly_score"] < -0.1:
            return "SUSPICIOUS"
        else:
            return "NORMAL"

    new_df["threat_level"] = new_df.apply(classify, axis=1)

    # -----------------------------------
    # SAVE BACK TO FEATURES
    # -----------------------------------
    df.loc[new_df.index, "anomaly_score"] = new_df["anomaly_score"]
    df.loc[new_df.index, "threat_level"] = new_df["threat_level"]
    df.to_csv(FEATURE_PATH, index=False)

    # -----------------------------------
    # ALERTS & LEARNING
    # -----------------------------------
    if not new_df.empty:
        print("\n🔍 Detection Results (New Logs):")
        print(new_df[["anomaly_score", "threat_level"]])

        from src.alerts import generate_alerts
        from src.evolve import evolve_system

        generate_alerts(new_df)
        evolve_system(new_df)

    # -----------------------------------
    # UPDATE GLOBAL METRICS
    # -----------------------------------
    old_metrics = {}

    if os.path.exists("results/metrics_after_learning.json"):
        with open("results/metrics_after_learning.json") as f:
            old_metrics = json.load(f)

    metrics = {
        "normal": old_metrics.get("normal", 0)
        + int((new_df["threat_level"] == "NORMAL").sum()),

        "suspicious": old_metrics.get("suspicious", 0)
        + int((new_df["threat_level"] == "SUSPICIOUS").sum()),

        "attacks": old_metrics.get("attacks", 0)
        + int((new_df["threat_level"] == "ATTACK").sum())
    }

    os.makedirs("results", exist_ok=True)
    with open("results/metrics_after_learning.json", "w") as f:
        json.dump(metrics, f, indent=4)

    # -----------------------------------
    # SAVE PROCESSED LOGS FOR DASHBOARD
    # -----------------------------------
    os.makedirs("results", exist_ok=True)

    existing_logs = []

    if os.path.exists(LOGS_PATH):
        with open(LOGS_PATH, "r") as f:
            loaded = json.load(f)

            if isinstance(loaded, list):
                existing_logs = loaded
            else:
                existing_logs = []



    new_logs = new_df.to_dict(orient="records")
    existing_logs.extend(new_logs)

    with open(LOGS_PATH, "w") as f:
        json.dump(existing_logs, f, indent=4)

    # -----------------------------------
    # SAVE COUNT & RETURN
    # -----------------------------------
    save_processed_log_count(current_total)
    return new_df
