from src.data_preprocessing import clean_logs
from src.feature_engineering import extract_features
from src.train import train_model
from src.evaluate import evaluate_logs

def main():
    print("🚀 Starting Self-Evolving Security Defense System")

    clean_logs()
    extract_features()
    train_model()
    evaluate_logs()

    print("✅ System execution completed")

if __name__ == "__main__":
    main()
