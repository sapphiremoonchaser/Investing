# Imports
from pydantic import (
    Field,
    model_validator,
)
from trading_analytics.data.data_model.entry.trade_entry import TradeEntry
from trading_analytics.data.enum.security_type import SecurityType

class DividendEntry(TradeEntry):
    """A model representing a dividend entry with relevant details.

    Attributes:
        dividend_amount (float): The amount received from the dividend.
    """
    dividend_amount: float = Field(ge=0, frozen=True)

    # Add a model validator to ensure security is 'DIVIDEND'
    @model_validator(mode='after')
    def check_dividend_security(self):
        """Validates that the security type is 'DIVIDEND.

        We already validated the action in TradeEntry.

        Args:
            self: The model instance being validated.

        Returns:
            self: The validated model instance.

        Raises:
            ValueError: If the security type is not 'DIVIDEND'.
        """
        valid_securities = {SecurityType.DIVIDEND}
        if self.security not in valid_securities:
            raise ValueError(f"StockEntry must have security type in {valid_securities}. Got {type(self.security)}")

        return self
