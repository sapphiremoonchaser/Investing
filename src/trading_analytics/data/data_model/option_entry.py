# Dataclass for Options

# Imports
from datetime import date, datetime
from pydantic import field_validator
from src.trading_analytics.data.data_model.trade_entry import TradeEntry

class StockEntry(TradeEntry):
    expiration: date
    strike: float
    premium: float
    subtype: str # call, put

    @field_validator("expiration", mode="before")
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception as e:
            raise ValueError("Yo mama needs to get tha time, fool")

