"""TradeEntry class for representing trading transactions.

This module defines the `TradeEntry` class, a Pydantic model that encapsulates the details of a trading transaction.
It includes fields for trade identification, strategy, security type, and other relevant details, with validators to
ensure data integrity and normalization. The class supports various security types (e.g., STOCK, ETF, DIVIDEND, OPTION)
and trade actions, with specific validation logic to enforce valid combinations.

Classes:
    TradeEntry: A Pydantic model representing a trade entry with validation for fields like brokerage, account, strategy,
                security type, trade date, symbol, action, sub-action, quantity, and fees.
"""
from datetime import (
    date,
    datetime,
)
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)
from typing import (
    Union,
    List,
    Optional,
)

from trading_analytics.data.enum.security_type import SecurityType
from trading_analytics.data.enum.trade_action import Action
from trading_analytics.data.enum.sub_action import SubAction
from trading_analytics.data.data_model.market.stock_data import CurrentStockData


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
    action: Action = Field(frozen=True)
    sub_action: SubAction = Field(frozen=True)
    quantity: float = Field(ge=0, frozen=True)
    fees: float = Field(ge=0, frozen=True)

    # Process STOCK or ETF trades with BUY action
    @property
    def is_bought_stock_etf(self) -> bool:
        """Whether the trade is bought stock or not."""
        if (
            self.security in [SecurityType.STOCK, SecurityType.ETF] and
            self.action == Action.BUY
        ):
            return True

        return False

    # Process Options sold to open
    @property
    def is_sold_open_option(self) -> bool:
        """Option trades that were sold open (call or put)"""
        if (
            self.security == [SecurityType.OPTION] and
            self.action == Action.SELL and
            self.sub_action == SubAction.OPEN
        ):
            return True

        return False


    # Process Options sold to close
    @property
    def is_sold_close_option(self) -> bool:
        """Option trades that were sold close (call or put)"""
        if(
            self.security == [SecurityType.OPTION] and
            self.action == Action.SELL and
            self.sub_action == SubAction.CLOSE
        ):
            return True

        return False


    # Process Options bought to open
    @property
    def is_bought_open_option(self) -> bool:
        """Option trades that were bought open (call or put)"""
        if(
            self.security == [SecurityType.OPTION] and
            self.action == Action.BUY and
            self.sub_action == SubAction.OPEN
        ):
            return True

        return False


    # Process Options bought to close
    @property
    def is_bought_close_option(self) -> bool:
        if(
            self.security == [SecurityType.OPTION] and
            self.action == Action.BUY and
            self.sub_action == SubAction.CLOSE
        ):
            return True

        return False


    # Process Expired Options
    @property
    def is_expired_option(self) -> bool:
        if (
            self.security == [SecurityType.OPTION] and
            self.action == Action.OPTION_EXPIRED
        ):
            return True

        return False


    # ToDo: is_assigned_call_or_exercised_put


    # ToDo: is_exercised_call_or_assigned_put

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
            raise ValueError(f"Did you enter the account as a string or an integer with length >= 4? Exception: {e}")

    # comma-separated string to a list of strings
    @field_validator(
        'strategy',
        mode='before'
    )
    def parse_and_normalize_strategy(
            cls,
            value: Union[List[str], str]
    ) -> Optional[List[str]]:
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

        raise ValueError(f"Strategy '{value}' is not a valid data type for strategy description.")

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

        raise ValueError(f"Security type {value} is invalid type, not string or SecurityType.")

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
            raise ValueError(f"Did you enter the symbol as a string or integer with length >= 1? Exception: {e}")

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
            cls: The class calling this method (used in class method context).
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
            raise ValueError(f"Invalid date format: {value}. Use 'YYYY-MM-DD' format. Exception: {e}")

    # Normalize 'action' to uppercase
    @field_validator(
        'action',
        mode='before'
    )
    def normalize_action(
            cls,
            value: Union[str, Action]
    ) -> Action:
        """Normalizes and validates the trade action.

            Args:
                cls: The class being validated.
                value (str): The trade action value to validate.

            Returns:
                str: The normalized (uppercase) trade action value.

            Raises:
                ValueError: If the trade action is not one of the valid types.
            """
        if isinstance(value, Action):
            return value

        # This is the case for my csv file
        if isinstance(value, str):
            try:
                return Action(value.upper())
            except Exception:
                raise ValueError(f"Trade action '{value}' is invalid.")

        raise ValueError(f"Trade action '{value}' is and invalid data type for trade action.")

    # Normalize 'sub_action' to uppercase
    @field_validator(
        'sub_action',
        mode='before'
    )
    def normalize_sub_action(
            cls,
            value: Union[str, SubAction]
    ) -> SubAction:
        """Normalizes and validates the trade sub action.

            Args:
                cls: The class being validated.
                value (str): The trade sub action value to validate.

            Returns:
                str: The normalized (uppercase) trade sub action value.

            Raises:
                ValueError: If the trade sub action is not one of the valid types.
            """
        if isinstance(value, SubAction):
            return value

        if isinstance(value, str):
            try:
                return SubAction(value.upper())
            except Exception:
                raise ValueError(f"Trade sub action '{value}' is invalid.")

        raise ValueError(f"Trade sub action '{value}' is and invalid data type for trade sub action.")

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
            SecurityType.STOCK: {Action.BUY, Action.SELL},
            SecurityType.ETF: {Action.BUY, Action.SELL},
            SecurityType.DIVIDEND: {Action.DIVIDEND},
            SecurityType.OPTION: {Action.BUY,
                                  Action.OPTION_ASSIGNED, Action.OPTION_EXPIRED, Action.OPTION_EXERCISED,
                                  Action.SELL}
        }

        valid_actions = valid_action_map.get(security, set())
        if action not in valid_actions:
            raise ValueError(f"Action '{action}' is not valid for security type, '{security}'. Valid actions: {valid_actions}")

        return self

