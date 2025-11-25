from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConversionRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

class ConversionResponse(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float
    rate: float
    timestamp: datetime

class ConversionHistory(BaseModel):
    id: int
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float
    rate: float
    timestamp: datetime