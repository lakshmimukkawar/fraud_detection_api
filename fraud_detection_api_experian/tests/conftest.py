import pytest
import xgboost as xgb
from fastapi.testclient import TestClient

from src.main import create_app


@pytest.fixture()
def client():
    app = create_app()

    model_path = "src/model/xgboost.json"
    model = xgb.Booster()
    model.load_model(model_path)

    app.state.model = model
    client = TestClient(app)
    return client


@pytest.fixture()
def input_examples():
    return {
        "customer_id": 345435,
        "number_of_open_accounts": 23,
        "total_credit_limit": 12345,
        "total_balance": 200000,
        "number_of_accounts_in_arrears": 2,
    }


@pytest.fixture()
def wrong_input():
    return {
        "customer_idd": 123,
        "total_credit_limitdd": 3000,
        "number_of_accounts_in_arrears": 1024288,
    }
