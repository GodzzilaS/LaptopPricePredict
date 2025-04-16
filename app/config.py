from pathlib import Path
from cryptography.fernet import Fernet

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODELS_DIR / "laptop_price_model.pkl"
DATA_PATH = DATA_DIR / "Laptop_price.csv"

FERNET_KEY = b'0G-M8viI4L0Y9oG5FxNq1Yy1gM4yCrHf9ZKxjG1yc30='


class Config:
    test_size = 0.2
    random_state = 42
    model_params = {
        "n_estimators": 100,
        "learning_rate": 0.1,
        "max_depth": 5,
        "random_state": 42,
    }
