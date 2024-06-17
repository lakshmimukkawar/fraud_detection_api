import argparse
import datetime as dt
import os

import pandas as pd

from src.fraud_detection_api.configuration import get_config
from src.fraud_detection_api.services.utils import get_logger
from src.fraud_detection_api.training.train_xgboost import FraudModel


logger = get_logger(__name__)


def gather_training_data(start_date: dt.date, end_date: dt.date):
    """
    This is a tmp function to gather the data. here I am using a test dataframe for training.
    With start and end date param you can load data from the snowflake
    """
    data = pd.DataFrame(
        {
            "number_of_open_accounts": [1, 2, 3, 4, 5],
            "total_credit_limit": [1000, 2000, 3000, 4000, 5000],
            "total_balance": [100, 200, 300, 400, 500],
            "number_of_accounts_in_arrears": [0, 1, 0, 1, 0],
        }
    )

    target = [0, 1, 0, 1, 0]
    return data, target


def main(
    start_date: dt.date,
    end_date: dt.date,
    model_name: str = None,
    model_path_to_save: str = None,
) -> None:
    """
    Main functin for training a fraud detection model

    Parameters:
        start_date(dt.date): request passed to fastapi web app
        end_date(dt.date): List of credit data for different customers
    Returns:
        response(List[ResponseOutput]): Returns a list of customerids and fraud probability
    """
    config = get_config()

    data, target = gather_training_data(start_date, end_date)

    fraud_model = FraudModel()
    fraud_model.train(data, target)

    predictions = fraud_model.get_predictions(data)
    logger.info("Predicted probabilities:", predictions)

    model_name = config["ModelName"] if model_name is None else model_name
    model_path_to_save = (
        os.path.join(config["BasePath"], config["ModelBasePath"])
        if model_path_to_save is None
        else model_path_to_save
    )
    fraud_model.save_model(os.path.join(model_path_to_save, model_name))

    logger.info("Model training finished.")


def to_date(raw_string: str) -> dt.date:
    """Parse YYYYmmdd string as a date"""
    return dt.datetime.strptime(raw_string, "%Y%m%d").date()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start_date",
        type=lambda s: dt.datetime.strptime(s, "%Y%m%d").date(),
        required=True,
        help="Start date for training data",
    )
    parser.add_argument(
        "--end_date",
        type=lambda s: dt.datetime.strptime(s, "%Y%m%d").date(),
        required=True,
        help="End date for training data",
    )
    parser.add_argument(
        "--model_name",
        help="Name of the model while saving it",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--model_path_to_save",
        required=False,
        help="Name of the model while saving it",
        type=str,
    )
    args = parser.parse_args()
    main(
        start_date=args.start_date,
        end_date=args.end_date,
        model_name=args.model_name,
        model_path_to_save=args.model_path_to_save,
    )
