import pandas as pd
import os

CLEAN_PATH = "data/processed/clean_logs.csv"
FEATURE_PATH = "data/processed/features.csv"


def extract_features():
    df = pd.read_csv(CLEAN_PATH)

    # feature 1: failed login
    df["failed"] = df["status"].apply(lambda x: 1 if x == "failed" else 0)

    # feature 2: login attempt
    df["login"] = df["action"].apply(lambda x: 1 if x == "login" else 0)

    # feature 3: admin access
    df["is_admin"] = df["user"].apply(lambda x: 1 if x == "admin" else 0)

    # feature 4: normalized attempts
    df["attempt_score"] = df["attempts"] / df["attempts"].max()

    features = df[
        ["failed", "login", "is_admin", "attempt_score"]
    ]

    os.makedirs("data/processed", exist_ok=True)
    features.to_csv(FEATURE_PATH, index=False)

    print("✅ Features extracted successfully")


if __name__ == "__main__":
    extract_features()
