from pydantic import BaseModel
from dataclasses import dataclass


class Transaction(BaseModel):
    date: str
    description: str
    amount: float


class AccountBalance(BaseModel):
    currency: str
    amount: float


@dataclass
class UserContext:
    user_id: int



# 
class TransactionServiceError(Exception):
    pass