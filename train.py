from app.config import MODEL_PATH
from app.model import LaptopPriceModel

if __name__ == "__main__":
    print("Запуск обучения модели...")
    model = LaptopPriceModel()
    model.train()
    print(f"Модель сохранена в {MODEL_PATH}")
