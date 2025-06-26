# Dataclass for Stocks

# Imports
from pydantic import Field
from src.trading_analytics.data.data_model.trade_entry import TradeEntry

class StockEntry(TradeEntry):
    price_per_share: float = Field(ge=0, frozen=True)
