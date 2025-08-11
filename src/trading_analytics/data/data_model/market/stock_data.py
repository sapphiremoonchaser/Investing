"""CurrentStockData class for representing live data about stock.

This module defines the `CurrentStockData` class, a Pydantic model,
to represent live data about a stock. Currently, this includes symbol and price.
'symbol' is validated to make sure it has a minimum length of 1.

Classes:
    CurrentStockData: A model for live stock data, symbol and price
"""
from pydantic import (
    BaseModel,
    Field,
    field_validator,
)
from typing import Union

class CurrentStockData(BaseModel):
    """A model representing current stock info

    Args:
        symbol (str): The stock or asset symbol (e.g., AAPL).
        current_price (float): The current price of the stock.
    """
    symbol: str = Field(min_length=1, frozen=True)
    current_price: float = Field(ge=0)

    # Convert symbol to a string
    @field_validator(
        'symbol',
        mode='before'
    )
    def validate_symbol(
            cls,
            value: Union[str, int]
    ) -> str:
        """Converts and validates the symbol field to a string.

        Args:
            cls: The class being validated.
            value: The account value to validate and convert.

        Returns:
            str: The validated symbol value as a string.

        Raises:
            ValueError: If the symbol value cannot be converted to a string.
        """
        if isinstance(value, str):
            return value
        try:
            return f"{value}"
        except Exception as e:
            raise ValueError(f"Did you enter the symbol as a string or integer with length >= 1? Exception: {e}")