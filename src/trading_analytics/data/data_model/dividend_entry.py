# Dataclass for entering dividend payments

# Imports
from pydantic import Field
from src.trading_analytics.data.data_model.trade_entry import TradeEntry

class DividendEntry(TradeEntry):
    dividend_amount: float = Field(ge=0, frozen=True)