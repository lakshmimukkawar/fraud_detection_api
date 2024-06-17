from pydantic import BaseModel


class InputCreditData(BaseModel):
    customer_id: int
    number_of_open_accounts: int
    total_credit_limit: float
    total_balance: float
    number_of_accounts_in_arrears: int


class ResponseOutput(BaseModel):
    customer_id: int
    fraud_probability: float
