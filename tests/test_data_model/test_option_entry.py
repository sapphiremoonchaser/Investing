import pytest
from datetime import date
from pydantic import ValidationError
from src.trading_analytics.data.data_model.option_entry import OptionEntry, OptionType
from src.trading_analytics.data.data_model.trade_entry import SecurityType, TradeAction, TradeStrategy, Brokerage

@pytest.fixture
def valid_option_data():
    return {
        "trade_id": 3,
        "strategy_id": 103,
        "brokerage": "ETRADE",
        "account": "12345",
        "strategy": ["BASIC OPTION"],
        "security": "OPTION",
        "trade_date": "2025-06-25",
        "symbol": "AAPL",
        "action": "BOUGHT OPEN",
        "quantity": 10,
        "fees": 5.0,
        "expiration": "2025-12-31",
        "strike": 150.0,
        "premium": 100.0,
        "subtype": "CALL"
    }

def test_valid_option_entry():
    option = OptionEntry(**valid_option_data())
    assert option.strike == 150.0
    assert option.premium == 100.0
    assert option.subtype == OptionType.CALL  # Note: Will fail due to validator bug
    assert option.security == SecurityType.OPTION
    assert option.expiration == date(2025, 12, 31)

def test_invalid_strike():
    data = valid_option_data()
    data["strike"] = 0
    with pytest.raises(ValidationError, match="greater than 0"):
        OptionEntry(**data)

def test_invalid_premium():
    data = valid_option_data()
    data["premium"] = 0
    with pytest.raises(ValidationError, match="greater than 0"):
        OptionEntry(**data)

def test_invalid_subtype():
    data = valid_option_data()
    data["subtype"] = "INVALID"
    with pytest.raises(ValidationError, match="not a valid option type"):
        OptionEntry(**data)

def test_invalid_expiration_date():
    data = valid_option_data()
    data["expiration"] = "2025/12/31"
    with pytest.raises(ValidationError, match="Yo mama needs to get tha time"):
        OptionEntry(**data)

def test_invalid_security_type():
    data = valid_option_data()
    data["security"] = "STOCK"
    with pytest.raises(ValidationError, match="not valid for security type"):
        OptionEntry(**data)

def test_immutability():
    option = OptionEntry(**valid_option_data())
    with pytest.raises(Exception, match="Cannot change a frozen field"):
        option.strike = 200.0