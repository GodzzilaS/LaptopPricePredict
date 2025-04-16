from app.config import MODEL_PATH
from app.model import LaptopPriceModel

if __name__ == "__main__":
    print("Starting model training...")
    model = LaptopPriceModel()
    model.train()
    print(f"Model saved to {MODEL_PATH}")
