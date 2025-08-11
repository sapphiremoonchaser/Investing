"""SymbolResult class for representing profit, stock quantity, and option quantity.

This module defines the `SymbolResult` class, a Pydantic model that represents profit,
option quantity, and option quantity. It is used to determine whether or not an asset
is currently owned.

Classes:
    SymbolResult: represents profit, stock quantity, and option quantity.
"""
from pydantic import (
    BaseModel,
    Field,
)

class SymbolResult(BaseModel):
    profit: float = Field(default=0.0)
    stock_qty: float = Field(default=0.0)
    option_qty: float = Field(default=0.0)