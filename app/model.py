import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from xgboost import XGBRegressor

from app.config import Config, MODEL_PATH, DATA_PATH


class LaptopPriceModel:
    def __init__(self):
        self.pipeline = None
        self.preprocessor = None

    def build_preprocessor(self, X: pd.DataFrame) -> ColumnTransformer:
        num_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_features = X.select_dtypes(include=['object']).columns.tolist()

        num_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        cat_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ])

        return ColumnTransformer(transformers=[
            ('num', num_transformer, num_features),
            ('cat', cat_transformer, cat_features)
        ])

    def train(self, data_path: str = DATA_PATH) -> None:
        df = pd.read_csv(data_path)
        X = df.drop(columns=['Price'])
        y = df['Price']

        self.preprocessor = self.build_preprocessor(X)
        self.pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('model', XGBRegressor(**Config.model_params))
        ])

        self.pipeline.fit(X, y)
        self.save(MODEL_PATH)

    def save(self, path: str) -> None:
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, path)

    @classmethod
    def load(cls, path: str = MODEL_PATH) -> Pipeline:
        return joblib.load(path)
