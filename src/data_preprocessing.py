import pandas as pd
import os

RAW_PATH = "data/raw/system_logs.csv"
CLEAN_PATH = "data/processed/clean_logs.csv"


def clean_logs():
    # load raw logs
    df = pd.read_csv(RAW_PATH)

    # basic cleaning
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # normalize status
    df["status"] = df["status"].str.lower()

    # save cleaned logs
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)

    print("✅ Clean logs saved successfully")


if __name__ == "__main__":
    clean_logs()
