import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from src.fraud_detection_api.services.utils import get_logger


logger = get_logger(__name__)


class FraudModel:
    def __init__(self, model_params=None):
        # Default model parameters for XGBoost
        if model_params is None:
            self.model_params = {
                "objective": "binary:logistic",
                "eval_metric": "logloss",
            }
        else:
            self.model_params = model_params

        self.model = None

    def train(self, data: pd.DataFrame, target, test_size=0.2, random_state=42):
        """
        Main training function for training the model and evaluation

        Parameters:
            data(pd.DataFrame): dataframe with all the features
            target(list): list of target labels
            test_size(float): train test split defined here
            random_state(int): randome state
        """
        X_train, X_test, y_train, y_test = train_test_split(
            data, target, test_size=test_size, random_state=random_state
        )

        dtrain = xgb.DMatrix(X_train, label=y_train)
        dtest = xgb.DMatrix(X_test, label=y_test)

        self.model = xgb.train(
            self.model_params,
            dtrain,
            num_boost_round=100,
            evals=[(dtest, "test")],
            early_stopping_rounds=10,
        )

        train_pred_proba = self.get_predictions(X_train)
        train_pred = [1 if prob > 0.5 else 0 for prob in train_pred_proba]

        test_pred_prob = self.get_predictions(X_test)
        test_pred = [1 if prob > 0.5 else 0 for prob in test_pred_prob]

        self.evaluate_model(y_true=y_train, y_pred=train_pred)
        self.evaluate_model(y_true=y_test, y_pred=test_pred)

    def evaluate_model(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """
        Model evaluation calculation for accuracy, precision, recall and f1 score

        Parameters:
            y_true(np.ndarray): array of true labels
            y_pred(np.ndarray): array of predicted labels
        """
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        logger.info(f"Test Accuracy: {accuracy:.4f}")
        logger.info(f"Test Precision: {precision:.4f}")
        logger.info(f"Test Recall: {recall:.4f}")
        logger.info(f"Test F1 Score: {f1:.4f}")

    def get_predictions(self, data: pd.DataFrame) -> np.ndarray:
        """
        Model evaluation calculation for accuracy, precision, recall and f1 score

        Parameters:
            data(pd.DataFrame): Pandas dataframe with features
        Returns:
            returns a numpy ndarray of prediction
        """
        if self.model is None:
            raise Exception(
                "Model is not trained yet. Please train the model before predicting."
            )

        ddata = xgb.DMatrix(data)
        return self.model.predict(ddata)

    def save_model(self, path: str) -> None:
        """
        Save model in a json format

        Parameters:
            path(str): full path location for model saving
        """
        if self.model is None:
            raise Exception(
                "Model is not trained yet. Please train the model before saving."
            )

        self.model.save_model(path)
        logger.info(f"Model saved to {path}")

    def load_model(self, path: str):
        """
        Load model using path

        Parameters:
            path(str): full path location for model saving
        """
        self.model = xgb.Booster()
        self.model.load_model(path)
        logger.info(f"Model loaded from {type(self.model)}")
