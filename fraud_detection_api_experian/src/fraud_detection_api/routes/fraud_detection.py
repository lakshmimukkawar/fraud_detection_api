from typing import List

import pandas as pd
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.requests import Request

from src.fraud_detection_api.routes.data_model import InputCreditData, ResponseOutput
from src.fraud_detection_api.routes.get_structured_response import get_response
from src.fraud_detection_api.services.get_predictions import get_predictions
from src.fraud_detection_api.services.utils import get_logger


router = APIRouter()
logger = get_logger(__name__)


@router.post("/fraud_detection", response_model=List[ResponseOutput])
async def fraud_detection(request: Request, input_credit_data: List[InputCreditData]):
    """
    This is the main function for fraduster detection post endpoint,
    which needs credit data and returns back the fraud probability.

    Parameters:
        request(Request): request passed to fastapi web app
        input_credit_data(List[InputCreditData]): List of credit data for different customers
    Returns:
        response(List[ResponseOutput]): Returns a list of customerids and fraud probability

    """
    try:
        input_credit_data_list = [input.dict() for input in input_credit_data]
        input_credit_data = pd.DataFrame(input_credit_data_list)

        predictions = get_predictions(request=request, input=input_credit_data)

        # create final response object to return
        response = get_response(
            predictions=predictions, input_dict=input_credit_data_list
        )
        logger.info("Finished processing predictions!")
        return response

    except Exception as e:
        logger.error(f"Error message is {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
