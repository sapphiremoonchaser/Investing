# Imports
from pydantic import Field, model_validator
from data.data_model.entry.trade_entry import TradeEntry
from data.enum.security_type import SecurityType

class StockEntry(TradeEntry):
    """A model representing a stock entry with relevant details.

    Attributes:
        price_per_share (float): The price per share of the stock.
    """
    price_per_share: float = Field(ge=0, frozen=True)

    # Add a model validator to ensure security is 'STOCK' or 'INDEX'
    @model_validator(mode='after')
    def check_stock_security(self):
        """Validates that the security type is either 'STOCK' or 'INDEX'.

        We already validated the action in TradeEntry.

        Args:
            self: The model instance being validated.

        Returns:
            self: The validated model instance.

        Raises:
            ValueError: If the security type is not 'STOCK' or 'INDEX'.
        """
        valid_securities = {SecurityType.STOCK, SecurityType.ETF}
        if self.security not in valid_securities:
            raise ValueError(f"StockEntry must have security type in {valid_securities}. Got {type(self.security)}")

        return self
