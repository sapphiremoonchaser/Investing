from dataclasses import Field
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, field_validator, model_validator
from typing import Optional

# Enum for valid security types
# Enum is used to define a set of named constant values
# Advantages: readability, type safe, maintainable, iterability, immutable
class TradeType(str, Enum):
    """An enumeration of valid trade types.

    Attributes:
        STOCK (str): Represents a stock trade.
        INDEX (str): Represents an index trade.
        OPTION (str): Represents an option trade.
        DIVIDEND (str): Represents a dividend trade.
    """
    STOCK = 'STOCK'
    INDEX = 'INDEX'
    OPTION = 'OPTION'
    DIVIDEND = 'DIVIDEND'

# Enum for valid trade actions
class TradeAction(str, Enum):
    BOUGHT = 'BOUGHT'
    BOUGHT_COVER = 'BOUGHT COVER'
    BOUGHT_OPEN = 'BOUGHT OPEN'
    DIVIDEND = 'DIVIDEND'
    OPTION_EXPIRED = 'OPTION EXPIRED'
    OPTION_ASSIGNED = 'OPTION ASSIGNED'
    OPTION_EXERCISED = 'OPTION EXERCISED'
    SOLD = 'SOLD'
    SOLD_SHORT = 'SOLD SHORT'
    SOLD_CLOSE = 'SOLD CLOSE'

# Enum for valid strategies
class TradeStrategy(str, Enum):
    """Enum class for valid trading strategies.

    This class defines a set of valid trading strategies as string enumerations.
    Each strategy represents a specific type of trading approach.

    Attributes:
        DIVIDEND (str): Dividend-based trading strategy.
        ETF (str): Exchange-traded fund trading strategy.
        BASIC_TRADE (str): Standard stock trading strategy.
        BASIC_OPTION (str): Basic options trading strategy.
        COVERED_CALL (str): Covered call options trading strategy.
        SPREAD (str): Spread-based options trading strategy.
    """
    DIVIDEND = 'DIVIDEND'
    ETF = 'ETF'
    BASIC_TRADE = 'BASIC TRADE'
    BASIC_OPTION = 'BASIC OPTION'
    COVERED_CALL = 'COVERED CALL'
    SPREAD = 'SPREAD'

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
    type: TradeType
    trade_date: date
    symbol: str
    action: TradeAction
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

    # Normalize 'type' to uppercase
    @field_validator('type')
    def validate_type(cls, value: str) -> str:
        value = value.upper()
        valid_types = {TradeType.STOCK, TradeType.INDEX, TradeType.OPTION, TradeType.DIVIDEND}
        if value not in valid_types:
            raise ValueError(f"Trade type must be one of {valid_types}, got {value}.")
        return value

    # Normalize 'action' to uppercase
    @field_validator('action')
    def validate_action(cls, value: str) -> str:
        value = value.upper()
        valid_types = {TradeAction.BOUGHT_COVER, TradeAction.BOUGHT_OPEN,
                        TradeAction.OPTION_ASSIGNED, TradeAction.OPTION_EXPIRED, TradeAction.OPTION_EXERCISED,
                        TradeAction.SOLD_CLOSE, TradeAction.SOLD_SHORT}
        if value not in valid_types:
            raise ValueError(f"Trade type must be one of {valid_types}, got {value}.")
        return value

    # Model Validator for mapping type to action
    # Defines a valid_action_map mapping type to action
    @model_validator(mode='after')
    def validate_action_type(self):
        """Ensures trade actions are valid for the specified trade type.

        Validates that the `action` field of the model is allowed for the given `type` field based on a predefined mapping.

        Returns:
            self: The validated model instance.

        Raises:
            ValueError: If the `action` is not valid for the specified `type`. For example, 'BOUGHT' is only allowed for 'STOCK' or 'INDEX' types.
        """
        action = self.action
        type = self.type

        # Define mapping of actions to type
        valid_action_map = {
            TradeType.STOCK: {TradeAction.BOUGHT, TradeAction.SOLD},
            TradeType.INDEX: {TradeAction.BOUGHT, TradeAction.SOLD},
            TradeType.DIVIDEND: {TradeAction.DIVIDEND},
            TradeType.OPTION: {TradeAction.BOUGHT_COVER, TradeAction.BOUGHT_OPEN,
                               TradeAction.OPTION_ASSIGNED, TradeAction.OPTION_EXPIRED, TradeAction.OPTION_EXERCISED,
                               TradeAction.SOLD_CLOSE, TradeAction.SOLD_SHORT}
        }

        valid_actions = valid_action_map.get(type, set())
        if action not in valid_actions:
            raise ValueError(f"Action '{action}' is not valid for trade type, '{type}'. Valid actions: {valid_actions}")

        return self

    # Validate that quantity is not negative
    @field_validator('quantity', mode="after")
    def validate_quantity(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        return value

    # Validate that fees are 0 or positive
    @field_validator('fees', mode="after")
    def validate_fees(cls, value: int) -> float:
        if value < 0:
            raise ValueError("Fees cannot be negative")
        return value

    # ToDo: validator to make sure symbol is non-empty

    # ToDo: validator to make sure trade_id is non-empty, positive, int

    # ToDo: validator to make sure strategy_id is non-empty, positve, int

    # ToDo: validator to make sure brokerage is nonempty

    # ToDo: validator for strategy
    # make type a list?


