# Dataclass for Stocks

# Imports
from src.trading_analytics.data.data_model.trade_entry import TradeEntry

class StockEntry(TradeEntry):
    price: float

