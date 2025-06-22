from dataclasses import Field
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, field_validator
from typing import Optional

# Enum for valid security types
# Enum is used to define a set of named constant values
# Advantages: readability, type safe, maintainable, iterability, immutable
class TradeType(str, Enum):
    STOCK = 'STOCK'
    INDEX = 'INDEX'
    OPTION = 'OPTION'
    DIVIDEND = 'DIVIDEND'

class TradeEntry(BaseModel):
    """A model representing a trade entry with relevant details.

    Args:
        trade_id (int): The unique identifier of the trade.
        strategy_id (int): The unique identifier of the strategy.
        brokerage (str): The name of the brokerage where the trade is executed.
        account (str): The account identifier for the trade.
        strategy (str): The trading strategy used (e.g., 'swing', 'day').
        type (str): Type of security (STOCK, DIVIDEND, OPTION).
        trade_date (date): The date the trade was executed.
        symbol (str): The stock or asset symbol (e.g., AAPL).
        action (str): The trade action (e.g., 'buy' or 'sell').
        quantity (int): The number of shares or units traded.
        fees (float): The transaction fees associated with the trade.
    """
    trade_id: int
    strategy_id: int
    brokerage: str
    account: str
    strategy: str
    type: str
    trade_date: date
    symbol: str
    action: str
    quantity: int
    fees: float

    # Convert date to format YYYY-mm-dd
    @field_validator("trade_date", mode="before")
    def parse_date(cls, value):
        """Parses a date from a string or returns an existing date object.

        Args:
            cls: The class calling this method (used in classmethod context).
            value: A date object or a string in 'YYYY-MM-DD' format.

        Returns:
            date: A date object parsed from the input string or the input date object.

        Raises:
            ValueError: If the input string is not in 'YYYY-MM-DD' format or cannot be parsed.
        """
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception as e:
            raise ValueError("Yo mama needs to get tha time, fool")

    # Make sure trade type is in a specific set
    @field_validator('type')
    def validate_type(cls, value: str) -> str:
        """Validates that the trade type is one of the allowed values.

        Args:
            cls: The class calling this method (used in classmethod context).
            value (str): The trade type to validate.

        Returns:
            str: The validated trade type.

        Raises:
            ValueError: If the trade type is not one of 'STOCK', 'INDEX', 'OPTION', or 'DIVIDEND'.
        """
        valid_types = {
            TradeType.STOCK,
            TradeType.INDEX,
            TradeType.OPTION,
            TradeType.DIVIDEND
        }
        if value not in valid_types:
            raise ValueError(f"Trade type must be one of {valid_types}, got {value}")
        return value
