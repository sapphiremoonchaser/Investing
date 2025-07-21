# Imports
from pydantic import BaseModel, validator
from typing import Optional, List

class Position(BaseModel):
    """Model for a current position in the portfolio."""
    brokerage: str
    account: str
    symbol: str
    current_price: Optional[float] = None
    original_buy_in: Optional[float] = None
    adjusted_buy_in: Optional[float] = None
    stock_qty: float = 0.0
    option_qty: float = 0.0
    profit: Optional[float] = None

    class Config:
        validate_assignment = True  # Ensures updates to instances are validated