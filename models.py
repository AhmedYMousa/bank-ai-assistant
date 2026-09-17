from pydantic import BaseModel

class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    
    
class AccountBalance(BaseModel):
    currency: str
    amount: float