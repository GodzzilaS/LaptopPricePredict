from pydantic import BaseModel


class PredictionResponse(BaseModel):
    predictions: list[float]
