# Imports
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Union, List

from src.data.enum.security_type import SecurityType
from src.data.enum.trade_action import TradeAction
from src.data.enum.sub_action import TradeSubAction
from src.data.data_model.market.stock_data import CurrentStockData


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
        symbol (Union[str, CurrentStockData]): The stock or asset symbol (e.g., AAPL) or a CurrentStockData instance.
        action (str): The trade action (e.g., 'buy' or 'sell').
        quantity (int): The number of shares or units traded.
        fees (float): The transaction fees associated with the trade.
    """
    trade_id: int = Field(gt=0, frozen=True)
    strategy_id: int = Field(gt=0, frozen=True)
    brokerage: str = Field(min_length=1, frozen=True)
    account: str = Field(min_length=4, frozen=True)
    strategy: List[str] = Field(frozen=True)
    security: SecurityType = Field(frozen=True)
    trade_date: date = Field(frozen=True)
    symbol: str = Field(min_length=1, frozen=True)
    action: TradeAction = Field(frozen=True)
    sub_action: TradeSubAction = Field(frozen=True)
    quantity: float = Field(ge=0, frozen=True)
    fees: float = Field(ge=0, frozen=True)

    # Normalize brokerage to uppercase
    @field_validator(
        'brokerage',
        mode='before'
    )
    def normalize_brokerage(
            cls,
            value: str
    ) -> str:
        """Validates and normalizes the brokerage name.

            Args:
                cls: The class being validated.
                value (str): The brokerage value to validate.

            Returns:
                Brokerage: The validated string value for brokerage name.

            Raises:
                ValueError: If the provided brokerage name is not valid.
            """
        if isinstance(value, str):
            try:
                return value.upper()
            except Exception:
                raise ValueError(f"Brokerage '{value}' is not a valid brokerage name.")

    # Convert account to string
    @field_validator(
        'account',
        mode='before'
    )
    def convert_account_to_string(
            cls,
            value: Union[str, int]
    ) -> str:
        """Converts and validates the account field to a string.

        Args:
            cls: The class being validated.
            value: The account value to validate and convert.

        Returns:
            str: The validated account value as a string.

        Raises:
            ValueError: If the account value cannot be converted to a string.
        """
        if isinstance(value, str):
            return value
        try:
            return f"{value}"
        except Exception as e:
            raise ValueError(f"Did you enter the account as a string or an integer with length >= 4?")

    # comma-separated string to a list of strings
    @field_validator(
        'strategy',
        mode='before'
    )
    def parse_and_normalize_strategy(
            cls,
            value: Union[List[str], str]
    ) -> List[str]:
        """Parse the string into a list of strategies and normalizes the strategies to lowercase.

            Args:
                cls: The class being validated.
                value (Union[List[str], str]): The strategy description value to validate.

            Returns:
                Brokerage: The validated string value for the strategy.

            Raises:
                ValueError: If the provided strategy description is not valid.
            """
        if isinstance(value, str):
            try:
                # Split comma-separated string and strip whitespace
                # Filter out empty strings
                return [strategy.strip() for strategy in value.lower().split(",") if strategy.strip()]
            except Exception:
                raise ValueError(f"Strategy '{value}' is not a valid strategy description.")

        elif isinstance(value, list):
            try:
                # Make sure all elements are strings and strip whitespace
                return [str(strategy.strip()) for strategy in value if strategy.strip()]
            except Exception:
                raise ValueError(f"Strategy '{value}' is not a valid strategy description.")

    # Normalize 'security' to uppercase
    @field_validator(
        'security',
        mode='before'
    )
    def normalize_security(
            cls,
            value: Union[str, SecurityType]
    ) -> SecurityType:
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

    # Convert symbol to a string
    @field_validator(
        'symbol',
        mode='before'
    )
    def validate_symbol(
            cls,
            value: Union[str, int, CurrentStockData]
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
        if isinstance(value, CurrentStockData):
            return value.symbol # Extract symbol from CurrentStockData
        if isinstance(value, str):
            return value
        try:
            return f"{value}"
        except Exception as e:
            raise ValueError(f"Did you enter the symbol as a string or integer with length >= 1?")

    # Convert date to format YYYY-mm-dd
    @field_validator(
        "trade_date",
        mode="before"
    )
    def parse_trade_date(
            cls,
            value
    ) -> date:
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
            raise ValueError(f"Invalid date format: {value}. Use 'YYYY-MM-DD' format.")

    # Normalize 'action' to uppercase
    @field_validator(
        'action',
        mode='before'
    )
    def normalize_action(
            cls,
            value: Union[str, TradeAction]
    ) -> TradeAction:
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

    # Normalize 'sub_action' to uppercase
    @field_validator(
        'sub_action',
        mode='before'
    )
    def normalize_sub_action(
            cls,
            value: Union[str, TradeSubAction]
    ) -> TradeSubAction:
        """Normalizes and validates the trade sub action.

            Args:
                cls: The class being validated.
                value (str): The trade sub action value to validate.

            Returns:
                str: The normalized (uppercase) trade sub action value.

            Raises:
                ValueError: If the trade sub action is not one of the valid types.
            """
        if isinstance(value, TradeSubAction):
            return value
        if isinstance(value, str):
            try:
                return TradeSubAction(value.upper())
            except Exception:
                raise ValueError(f"Trade sub action '{value}' is invalid.")

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
            SecurityType.STOCK: {TradeAction.BUY, TradeAction.SELL},
            SecurityType.ETF: {TradeAction.BUY, TradeAction.SELL},
            SecurityType.DIVIDEND: {TradeAction.DIVIDEND},
            SecurityType.OPTION: {TradeAction.BUY,
                                  TradeAction.OPTION_ASSIGNED, TradeAction.OPTION_EXPIRED, TradeAction.OPTION_EXERCISED,
                                  TradeAction.SELL}
        }

        valid_actions = valid_action_map.get(security, set())
        if action not in valid_actions:
            raise ValueError(f"Action '{action}' is not valid for security type, '{security}'. Valid actions: {valid_actions}")

        return self

