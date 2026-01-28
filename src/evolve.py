# import pandas as pd
# import os
# from src.model import build_model, save_model, load_model


# FEATURE_PATH = "data/processed/features.csv"
# LEARNED_PATH = "data/processed/learned_attacks.csv"
# MODEL_PATH = "models/ids_model_latest.pkl"


# def evolve_system(df):
#     # keep only threats
#     threats = df[df["threat_level"] != "NORMAL"]

#     if threats.empty:
#         print("✅ No new threats to learn from")
#         return

#     os.makedirs("data/processed", exist_ok=True)

#     # append learned attacks
#     # if os.path.exists(LEARNED_PATH):
#     #     old = pd.read_csv(LEARNED_PATH)
#     #     threats = pd.concat([old, threats])

#     if os.path.exists(LEARNED_PATH) and os.path.getsize(LEARNED_PATH) > 0:
#         old = pd.read_csv(LEARNED_PATH)
#         threats = pd.concat([old, threats])


#     threats.to_csv(LEARNED_PATH, index=False)
#     print("🧠 New threats stored")

#     # retrain model
#     features = pd.read_csv(FEATURE_PATH)

#     model = build_model()
#     model.fit(features)

#     save_model(model, MODEL_PATH)
#     print("🔁 Model evolved successfully")





import json
import os
import hashlib

KNOWN_ATTACKS_PATH = "results/known_attacks.json"

def evolve_system(df):

    if os.path.exists(KNOWN_ATTACKS_PATH):
        with open(KNOWN_ATTACKS_PATH, "r") as f:
            known_attacks = json.load(f)
    else:
        known_attacks = []

    new_attack_detected = False

    for _, row in df.iterrows():
        if row["threat_level"] == "ATTACK":

            feature_values = row.drop(
                ["anomaly", "threat_level"],
                errors="ignore"
            ).values

            pattern_string = ",".join(map(str, feature_values))
            pattern_hash = hashlib.sha256(pattern_string.encode()).hexdigest()

            if not any(a["pattern_hash"] == pattern_hash for a in known_attacks):
                print("🚨 NEW UNKNOWN ATTACK PATTERN DETECTED 🚨")
                known_attacks.append({
                    "pattern_hash": pattern_hash,
                    "first_seen_score": round(float(row["anomaly_score"]), 2)
                })
                new_attack_detected = True

    if new_attack_detected:
        os.makedirs("results", exist_ok=True)
        with open(KNOWN_ATTACKS_PATH, "w") as f:
            json.dump(known_attacks, f, indent=4)
        print("🧠 Threat memory updated with new patterns")
    else:
        if known_attacks:
            print("🧠 Threat memory verified (no new patterns)")
