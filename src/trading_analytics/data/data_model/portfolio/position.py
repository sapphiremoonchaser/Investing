# Imports
from pydantic import (
    BaseModel,
    ConfigDict,
)
from typing import Optional

class Position(BaseModel):
    """Model for a current position in the portfolio."""
    model_config = ConfigDict(
        validate_assignment=True, # Ensures updates to instances are validated
    )

    symbol: str
    current_price: Optional[float] = None
    original_buy_in: Optional[float] = None
    adjusted_buy_in: Optional[float] = None
    stock_qty: float = 0.0
    option_qty: float = 0.0
    profit: Optional[float] = None
