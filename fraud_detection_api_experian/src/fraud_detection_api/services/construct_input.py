import pandas as pd
import xgboost as xgb

from src.fraud_detection_api.services.utils import get_logger


logger = get_logger(__name__)


def construct_input(input: pd.DataFrame) -> xgb.core.DMatrix:
    """
    Construct input so that we pass only relevant features to the model for predictions.
    xgb.DMatrix is a data structure optimized for use with xgboost.

    Parameters:
        input(pd.DataFrame): Input pandas dataframe
    Returns:
        input_xgb(xgb.core.DMatrix): features to be passed to the model
    """
    # remove the customer ids as that is not a feature for model trained
    input.drop(columns="customer_id", inplace=True)
    input_xgb = xgb.DMatrix(input)
    return input_xgb
