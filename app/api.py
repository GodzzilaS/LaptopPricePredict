from io import BytesIO

import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import ORJSONResponse

from app.config import MODEL_PATH
from app.model import LaptopPriceModel
from app.schemas import PredictionResponse
from app.security_utils import sanitize_dataframe, encrypt_ram, print_first_five_decrypted_ram

app = FastAPI(
    title="API предсказания цен для ноутбуков",
    description="API предсказания цен для ноутбуков, использующая XGBoost модель",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
def load_model():
    try:
        app.state.model = LaptopPriceModel.load(MODEL_PATH)
        print(f"Используем модель: {MODEL_PATH}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке модели: {str(e)}") from e


@app.post("/predict/", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(BytesIO(content))

        try:
            df = sanitize_dataframe(df)
        except ValueError as ve:
            raise HTTPException(400, f"Проверка безопасности не пройдена: {str(ve)}")

        df_encrypted = encrypt_ram(df.copy(), ram_column="RAM_Size", new_column="RAM_encrypted")
        print_first_five_decrypted_ram(df_encrypted, encrypted_column="RAM_encrypted")

        predictions = app.state.model.predict(df)
        return {"predictions": predictions.tolist()}
    except pd.errors.ParserError:
        raise HTTPException(400, "Неверный формат CSV-файла")
    except Exception as e:
        raise HTTPException(500, f"Ошибка предсказания: {str(e)}")
