# Imports
from enum import Enum
from datetime import date, datetime
from typing import Union

from pydantic import Field, field_validator, model_validator
from data.data_model.trade_entry import TradeEntry
from src.data.enum.security_type import SecurityType
from src.data.enum.option_type import OptionType

class OptionEntry(TradeEntry):
    expiration_date: date
    strike: float = Field(ge=0, frozen=True)
    premium: float = Field(ge=0, frozen=True)
    option_type: OptionType = Field(frozen=True)

    @field_validator("expiration_date", mode="before")
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
    @field_validator('option_type', mode='before')
    def validate_option_type(cls, value: Union[str, OptionType]) -> OptionType:
        """Normalizes and validates the option type.

        Args:
            cls: The class being validated.
            value (Union[str, OptionType]): The option type value, either a string or OptionType enum.

        Returns:
            OptionType: The validated OptionType enum value.

        Raises:
            ValueError: If the provided option type is not valid.
        """
        # Don't need this if using my csv file but might need later
        if isinstance(value, OptionType):
            return value
        # This is case for csv file
        if isinstance(value, str):
            try:
                return OptionType(value.upper())
            except Exception:
                raise ValueError(f"Option type '{value}' is not a valid option type.")

    # Validate that the security type is 'OPTION'
    @model_validator(mode='after')
    def check_option_security(self):
        """Validates that the security type is 'OPTION' and expiration date is after trade date.

        Args:
            self: The model instance being validated.

        Returns:
            self: The validated model instance.

        Raises:
            ValueError: If the security type is not 'OPTION' or if the expiration date is not after the trade date.
        """
        if self.security != SecurityType.OPTION:
            raise ValueError(f"OptionEntry must have security {SecurityType.OPTION}, got {self.security}")
        if self.expiration_date < self.trade_date:
            raise ValueError(f"Expiration date {self.expiration_date} must be after trade date {self.trade_date}.")

        return self


