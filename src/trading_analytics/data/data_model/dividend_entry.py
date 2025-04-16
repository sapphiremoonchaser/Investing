# Dataclass for entering dividend payments

# Imports
from src.trading_analytics.data.data_model.trade_entry import TradeEntry

class DividendEntry(TradeEntry):
    interest_paid: float