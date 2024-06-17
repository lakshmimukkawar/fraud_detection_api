from typing import List

import numpy as np
import pandas as pd
from starlette.requests import Request

from src.fraud_detection_api.services.construct_input import construct_input
from src.fraud_detection_api.services.utils import get_logger


logger = get_logger(__name__)


def get_predictions(request: Request, input: pd.DataFrame) -> np.ndarray:
    """
    Construct input so that we pass only relevant features to the model for predictions.
    xgb.DMatrix is a data structure optimized for use with xgboost.

    Parameters:
        request(Request): Request passed to fastapi web app
        input(pd.DataFrame): Input dataframe with features number_of_open_accounts,
        total_credit_limit, total_balance and number_of_accounts_in_arrears
    Returns:
        predictions(np.ndarray): Array of fraud probabilities
    """
    logger.info("Inside the get predictions service!")
    input = construct_input(input=input)
    predictions = request.state.model.predict(input)
    logger.info("Predictions gathered from model")
    return predictions
