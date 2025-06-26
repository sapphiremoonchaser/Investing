import pytest
from pydantic import ValidationError
from src.trading_analytics.data.data_model.stock_entry import StockEntry
from src.trading_analytics.data.data_model.trade_entry import SecurityType, TradeAction, TradeStrategy, Brokerage

@pytest.fixture
def valid_stock_data():
    return {
        "trade_id": 1,
        "strategy_id": 101,
        "brokerage": "ETRADE",
        "account": "12345",
        "strategy": ["BASIC TRADE"],
        "security": "STOCK",
        "trade_date": "2025-06-25",
        "symbol": "AAPL",
        "action": "BOUGHT",
        "quantity": 100,
        "fees": 0.0,
        "price": 150.0
    }

def test_valid_stock_entry():
    stock = StockEntry(**valid_stock_data())
    assert stock.price == 150.0
    assert stock.security == SecurityType.STOCK
    assert stock.action == TradeAction.BOUGHT

def test_invalid_price():
    data = valid_stock_data()
    data["price"] = -150.0
    with pytest.raises(ValidationError, match="greater than or equal to 0"):
        StockEntry(**data)

def test_invalid_security_type():
    data = valid_stock_data()
    data["security"] = "DIVIDEND"
    with pytest.raises(ValidationError, match="not valid for security type"):
        StockEntry(**data)

def test_immutability():
    stock = StockEntry(**valid_stock_data())
    with pytest.raises(Exception, match="Cannot change a frozen field"):
        stock.price = 200.0