from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODELS_DIR / "laptop_price_model.pkl"
DATA_PATH = DATA_DIR / "Laptop_price.csv"


class Config:
    test_size = 0.2
    random_state = 42
    model_params = {
        "n_estimators": 100,
        "learning_rate": 0.1,
        "max_depth": 5,
        "random_state": 42,
    }
