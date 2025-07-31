"""BuyInData class for representing everything necessary to calculate the original or adjusted buy-in.

This module defines the `BuyInData` class, a Pydantic model that includes everything necessary for
calculating original buy-in or adjusted buy-in.

Classes:
    BuyInData: A model for values necessary to calculate original or adjusted buy-in.
"""
from pydantic import (
    BaseModel,
    Field,
)

class BuyInData(BaseModel):
    total_cost: float = Field(default=0.0)
    total_quantity: float = Field(default=0.0)
    net_option_premiums: float = Field(default=0.0)
    total_dividends: float = Field(default=0.0)