from dataclasses import Field
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Union


# Enum for valid security types
# Enum is used to define a set of named constant values
# Advantages: readability, type safe, maintainable, iterability, immutable
class SecurityType(str, Enum):
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

# Enum for brokerage
class Brokerage(str, Enum):
    """Enum class for valid brokerage names.

        This class defines a set of valid brokerage names as string enumerations.
        Each value represents a specific brokerage platform.

        Attributes:
            ETRADE (str): E*TRADE brokerage platform.
        """
    ETRADE = 'ETRADE'

class TradeEntry(BaseModel):
    """A model representing a trade entry with relevant details.

    Args:
        trade_id (int): The unique identifier of the trade.
        strategy_id (int): The unique identifier of the strategy.
        brokerage (str): The name of the brokerage where the trade is executed.
        account (str): The account identifier for the trade.
        strategy (str): The trading strategy used (e.g., 'swing', 'day').
        security (str): Type of security (STOCK, DIVIDEND, OPTION).
        trade_date (date): The date the trade was executed.
        symbol (str): The stock or asset symbol (e.g., AAPL).
        action (str): The trade action (e.g., 'buy' or 'sell').
        quantity (int): The number of shares or units traded.
        fees (float): The transaction fees associated with the trade.
    """
    trade_id: int = Field(gt=0, frozen=True)
    strategy_id: int = Field(gt=0, frozen=True)
    brokerage: Brokerage = Field(frozen=True) # Do I even need to validate this?
    account: str = Field(min_length=4, frozen=True)
    strategy: TradeStrategy = Field(frozen=True) # Do I even need to validate this?
    security: SecurityType = Field(frozen=True) # Do I even need to validate this?
    trade_date: date = Field(frozen=True)
    symbol: str = Field(min_length=3, frozen=True)
    action: TradeAction = Field(frozen=True) # Do I even need to validate this?
    quantity: int = Field(ge=0, frozen=True)
    fees: float = Field(ge=0, frozen=True)

    # Validator to make sure brokerage in Enum class Brokerage
    @field_validator('brokerage')
    def validate_brokerage(cls, value: Union[str, Brokerage]) -> Brokerage:
        """Validates and normalizes the brokerage name.

            Args:
                cls: The class being validated.
                value (Union[str, Brokerage]): The brokerage value to validate, either a string or Brokerage enum.

            Returns:
                Brokerage: The validated Brokerage enum value.

            Raises:
                ValueError: If the provided brokerage name is not valid.
            """
        # Don't need this if using my csv file but might need later
        if isinstance(value, Brokerage):
            return value
        # This is case for csv file
        if isinstance(value, str):
            try:
                return Brokerage(values.upper())
            except Exception:
                raise ValueError(f"Brokerage '{value}' is not a valid brokerage name.")


    # ToDo: validator for strategy
    # make type a list?

    # Normalize 'type' to uppercase
    @field_validator('security', mode='before')
    def validate_security(cls, value: Union[str, SecurityType]) -> SecurityType:
        """Normalizes and validates the trade type.

            Args:
                cls: The class being validated.
                value (str): The trade type value to validate.

            Returns:
                str: The normalized (uppercase) trade type value.

            Raises:
                ValueError: If the trade type is not one of the valid types.
            """
        # Don't need this if for my csv file but might need it later
        if isinstance(value, SecurityType):
            return value
        # This is the case for my csv file
        if isinstance(value, str):
            try:
                return SecurityType(value.upper())
            except Exception:
                raise ValueError(f"Security type {value} is invalid.")

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

    # Normalize 'action' to uppercase
    @field_validator('action')
    def validate_action(cls, value: Union[str, TradeAction]) -> TradeAction:
        """Normalizes and validates the trade action.

            Args:
                cls: The class being validated.
                value (str): The trade action value to validate.

            Returns:
                str: The normalized (uppercase) trade action value.

            Raises:
                ValueError: If the trade action is not one of the valid types.
            """
        if isinstance(value, TradeAction):
            return value
        # This is the case for my csv file
        if isinstance(value, str):
            try:
                return TradeAction(value.upper())
            except Exception:
                raise ValueError(f"Trade action '{value}' is invalid.")

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
        security = self.security

        # Define mapping of actions to type
        valid_action_map = {
            SecurityType.STOCK: {TradeAction.BOUGHT, TradeAction.SOLD},
            SecurityType.INDEX: {TradeAction.BOUGHT, TradeAction.SOLD},
            SecurityType.DIVIDEND: {TradeAction.DIVIDEND},
            SecurityType.OPTION: {TradeAction.BOUGHT_COVER, TradeAction.BOUGHT_OPEN,
                                  TradeAction.OPTION_ASSIGNED, TradeAction.OPTION_EXPIRED, TradeAction.OPTION_EXERCISED,
                                  TradeAction.SOLD_CLOSE, TradeAction.SOLD_SHORT}
        }

        valid_actions = valid_action_map.get(security, set())
        if action not in valid_actions:
            raise ValueError(f"Action '{action}' is not valid for security type, '{security}'. Valid actions: {valid_actions}")

        return self

    # Validate that quantity is not negative
    @field_validator('quantity', mode="after")
    def validate_quantity(cls, value: int) -> int:
        """Validates that the quantity is not negative.

            Args:
                cls: The class being validated.
                value (int): The quantity value to validate.

            Returns:
                int: The validated quantity value.

            Raises:
                ValueError: If the quantity is negative.
            """
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        return value

    # Validate that fees are 0 or positive
    @field_validator('fees', mode="after")
    def validate_fees(cls, value: float) -> float:
        """Validates that the fees are zero or positive.

        Args:
            cls: The class being validated.
            value (int): The fees value to validate.

        Returns:
            float: The validated fees value.

        Raises:
            ValueError: If the fees are negative.
        """
        if value < 0:
            raise ValueError("Fees cannot be negative")
        return value
