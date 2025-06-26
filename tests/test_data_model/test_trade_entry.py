import pytest
from datetime import date
from pydantic import ValidationError
from src.trading_analytics.data.data_model.trade_entry import TradeEntry, SecurityType, TradeAction, TradeStrategy, Brokerage

@pytest.fixture
def valid_trade_data():
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
        "fees": 0.0
    }

def test_valid_trade_entry():
    trade = TradeEntry(**valid_trade_data())
    assert trade.trade_id == 1
    assert trade.security == SecurityType.STOCK
    assert trade.strategy == [TradeStrategy.BASIC_TRADE]
    assert trade.trade_date == date(2025, 6, 25)
    assert trade.brokerage == Brokerage.ETRADE
    assert trade.action == TradeAction.BOUGHT

def test_valid_multiple_strategies():
    data = valid_trade_data()
    data["strategy"] = ["BASIC TRADE", "ETF"]
    trade = TradeEntry(**data)
    assert trade.strategy == [TradeStrategy.BASIC_TRADE, TradeStrategy.ETF]

def test_invalid_trade_id():
    data = valid_trade_data()
    data["trade_id"] = 0
    with pytest.raises(ValidationError, match="greater than 0"):
        TradeEntry(**data)

def test_invalid_brokerage():
    data = valid_trade_data()
    data["brokerage"] = "INVALID"
    with pytest.raises(ValidationError, match="not a valid brokerage name"):
        TradeEntry(**data)

def test_invalid_security():
    data = valid_trade_data()
    data["security"] = "INVALID"
    with pytest.raises(ValidationError, match="invalid"):
        TradeEntry(**data)

def test_invalid_action_for_security():
    data = valid_trade_data()
    data["security"] = "STOCK"
    data["action"] = "DIVIDEND"
    with pytest.raises(ValidationError, match="not valid for security type"):
        TradeEntry(**data)

def test_invalid_date_format():
    data = valid_trade_data()
    data["trade_date"] = "2025/06/25"
    with pytest.raises(ValidationError, match="Yo mama needs to get tha time"):
        TradeEntry(**data)

def test_invalid_quantity():
    data = valid_trade_data()
    data["quantity"] = -100
    with pytest.raises(ValidationError, match="greater than or equal to 0"):
        TradeEntry(**data)

def test_invalid_fees():
    data = valid_trade_data()
    data["fees"] = -10.0
    with pytest.raises(ValidationError, match="greater than or equal to 0"):
        TradeEntry(**data)

def test_invalid_account_length():
    data = valid_trade_data()
    data["account"] = "123"
    with pytest.raises(ValidationError, match="at least 4 characters"):
        TradeEntry(**data)

def test_immutability():
    trade = TradeEntry(**valid_trade_data())
    with pytest.raises(Exception, match="Cannot change a frozen field"):
        trade.trade_id = 2