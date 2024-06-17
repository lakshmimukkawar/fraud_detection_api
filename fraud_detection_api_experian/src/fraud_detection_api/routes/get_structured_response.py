from typing import List

from src.fraud_detection_api.routes.data_model import ResponseOutput


def get_response(input_dict: dict, predictions: List[float]) -> List[ResponseOutput]:
    """
    Restructure predictions to pass as final output

    Parameters:
        input_dict(dict): input passed through the post endpoint request
        predictions( List[float]): List of fraud probabilities from model prediction
    Returns:
        responseee(List[ResponseOutput]): List of response output with customer id and fraud probability
    """
    responseee = []
    for index, input in enumerate(input_dict):
        responseee.append(
            ResponseOutput(
                customer_id=input["customer_id"], fraud_probability=predictions[index]
            )
        )

    return responseee
