# Dataclass for Options

# Imports
from enum import Enum
from datetime import date, datetime
from typing import Union

from pydantic import Field, field_validator
from src.trading_analytics.data.data_model.trade_entry import TradeEntry

# Enum for valid option subtypes
class OptionType(str, Enum):
    """Enum class for valid option subtypes.

    This class defines a set of valid option subtypes as string enumerations.
    Each subtype represents a specific type of option contract.

    Attributes:
        CALL (str): Call option subtype.
        PUT (str): Put option subtype.
    """
    CALL = 'CALL'
    PUT = 'PUT'

class OptionEntry(TradeEntry):
    expiration: date
    strike: float = Field(gt=0, frozen=True)
    premium: float = Field(gt=0, frozen=True)
    subtype: str # call, put

    @field_validator("expiration", mode="before")
    def parse_expiration_date(cls, value):
        """Parses and validates the expiration date.

        Args:
            cls: The class being validated.
            value: The expiration date value, either a date object or a string in 'YYYY-MM-DD' format.

        Returns:
            date: The validated date object.

        Raises:
            ValueError: If the date string is not in the correct format or cannot be parsed.
        """
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception as e:
            raise ValueError("Yo mama needs to get tha time, fool")

    # Normalize option type to uppercase
    @field_validator('subtype', mode='before')
    def validate_option_type(cls, value: Union[str, OptionType]) -> OptionType:

        # Don't need this if using my csv file but might need later
        if isinstance(value, OptionType):
            return value
        # This is case for csv file
        if isinstance(value, str):
            try:
                return OptionType(value.upper())
            except Exception:
                raise ValueError(f"Option type '{value}' is not a valid option type.")