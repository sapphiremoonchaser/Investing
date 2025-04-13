
from datetime import date, datetime
from pydantic import BaseModel, field_validator


class TradeEntry(BaseModel):
    brokerage: str
    account: str
    symbol: str
    action: str
    quantity: int
    fees: float
    strategy: str
    trade_date: date

    @field_validator("trade_date", mode="before")
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception as e:
            raise ValueError("Yo mama needs to get tha time, fool")
