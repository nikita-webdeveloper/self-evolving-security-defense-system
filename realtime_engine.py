import time
from src.data_preprocessing import clean_logs
from src.feature_engineering import extract_features
from src.evaluate import evaluate_logs

print("🚀 Real-Time Security Engine Started")

while True:
    print("🔎 Checking for new logs...")

    # Step 1: Rebuild pipeline for new raw logs
    clean_logs()
    extract_features()

    # Step 2: Evaluate only new entries
    evaluate_logs()

    print("⏳ Waiting for next cycle...\n")
    time.sleep(5)
