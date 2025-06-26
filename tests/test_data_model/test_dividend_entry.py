import pytest
from pydantic import ValidationError
from src.trading_analytics.data.data_model.dividend_entry import DividendEntry
from src.trading_analytics.data.data_model.trade_entry import SecurityType, TradeAction, TradeStrategy, Brokerage

@pytest.fixture
def valid_dividend_data():
    return {
        "trade_id": 2,
        "strategy_id": 102,
        "brokerage": "ETRADE",
        "account": "12345",
        "strategy": ["DIVIDEND"],
        "security": "DIVIDEND",
        "trade_date": "2025-06-25",
        "symbol": "AAPL",
        "action": "DIVIDEND",
        "quantity": 100,
        "fees": 0.0,
        "interest_paid": 0.82
    }

def test_valid_dividend_entry(valid_dividend_data):
    dividend = DividendEntry(**valid_dividend_data)
    assert dividend.interest_paid == 0.82
    assert dividend.security == SecurityType.DIVIDEND
    assert dividend.action == TradeAction.DIVIDEND

def test_invalid_interest_paid():
    data = valid_dividend_data()
    data["interest_paid"] = -0.82
    with pytest.raises(ValidationError, match="greater than or equal to 0"):
        DividendEntry(**data)

def test_invalid_security_type():
    data = valid_dividend_data()
    data["security"] = "STOCK"
    with pytest.raises(ValidationError, match="not valid for security type"):
        DividendEntry(**data)

def test_immutability(valid_dividend_data):
    dividend = DividendEntry(**valid_dividend_data)
    with pytest.raises(Exception, match="Cannot change a frozen field"):
        dividend.interest_paid = 1.0