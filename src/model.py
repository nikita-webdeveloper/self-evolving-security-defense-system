from sklearn.ensemble import IsolationForest
import joblib
import os


def build_model():
    model = IsolationForest(
        n_estimators=100,
        contamination=0.2,
        random_state=42
    )
    return model


def save_model(model, path):
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, path)
    print("✅ Model saved")


def load_model(path):
    return joblib.load(path)
