import os

import xgboost as xgb
from fastapi import FastAPI

from src.fraud_detection_api.configuration import get_config
from src.fraud_detection_api.routes import fraud_detection, healthcheck


config = get_config()


def create_app():
    app = FastAPI()

    @app.on_event("startup")
    async def app_startup():
        model_path = os.path.join(
            config["BasePath"], config["ModelBasePath"], config["ModelName"]
        )
        print(f"model path is {model_path}")
        try:
            model = xgb.Booster()
            model.load_model(model_path)
            app.state.model = model
        except xgb.core.XGBoostError as e:
            raise Exception(f"Failed to load xgboost model from path {model_path}: {e}")

    @app.middleware("http")
    async def state_injector(request, call_next):
        request.state.model = app.state.model
        return await call_next(request)

    app.include_router(healthcheck.router)
    app.include_router(fraud_detection.router)

    return app


app = create_app()
