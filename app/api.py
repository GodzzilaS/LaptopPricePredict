from io import BytesIO

import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import ORJSONResponse

from app.config import MODEL_PATH
from app.model import LaptopPriceModel
from app.schemas import PredictionResponse

app = FastAPI(
    title="Laptop Price Prediction API",
    description="API for predicting laptop prices using XGBoost model",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
def load_model():
    try:
        app.state.model = LaptopPriceModel.load(MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}") from e


@app.post("/predict/", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(BytesIO(content))
        predictions = app.state.model.predict(df)
        return {"predictions": predictions.tolist()}
    except pd.errors.ParserError:
        raise HTTPException(400, "Invalid CSV file format")
    except Exception as e:
        raise HTTPException(500, f"Prediction failed: {str(e)}")
