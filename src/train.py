import pandas as pd
from src.model import build_model, save_model

FEATURE_PATH = "data/processed/features.csv"
MODEL_PATH = "models/ids_model_v1.pkl"


def train_model():
    df = pd.read_csv(FEATURE_PATH)

    model = build_model()
    model.fit(df)

    save_model(model, MODEL_PATH)
    print("✅ Model training completed")


if __name__ == "__main__":
    train_model()
