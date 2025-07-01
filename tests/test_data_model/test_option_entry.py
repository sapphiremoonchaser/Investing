import unittest

from trading_analytics.data.data_model.trade_entry import Brokerage, TradeEntry, SecurityType, TradeAction, TradeStrategy
from trading_analytics.data.data_model.option_entry import OptionEntry, OptionType

OptionType
from datetime import date
from pydantic import ValidationError

class TestExpirationDate(unittest.TestCase):
    """Unit tests for validating expiration date values in TradeEntry.

    Valid Test Cases:
        date object (date(2025,1,23))

    Invalid Test Cases:
        wrong format (year at end)
        wrong format (date in middle)
        empty string
        random string
        None

    ToDo (More tests):
        string with format "YYYY-MM-dd" (valid)

    """
    def test_valid_expiration_date(self):
        # valid_expiration_dates = [date(2025,1,23), "2025-01-23"]
        valid_expiration_dates = [date(2025, 2, 20),]
        for value in valid_expiration_dates:
            with self.subTest(value=value):
                # Create a valid OptionEntry instance to test brokerage validation
                option_entry = OptionEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.COVERED_CALL],
                    security=SecurityType.OPTION,
                    trade_date=date(2025, 1, 23),
                    symbol="AAPL",
                    action=TradeAction.OPTION_EXPIRED,
                    quantity=100,
                    fees=5.0,
                    expiration_date=value,
                    strike=5,
                    premium=1,
                    subtype=OptionType.CALL
                )
                self.assertEqual(option_entry.expiration_date, value)


    def test_invalid_expiration_date(self):
        """Tests the validation of invalid expiration date values for TradeEntry.

        Iterates through a list of invalid expiration date inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the expiration date value is invalid.
        """
        invalid_expiration_dates = ["14-10-2025", "2025-14-09", "Heather", "", None]
        for value in invalid_expiration_dates:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    OptionEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage=Brokerage.ETRADE,
                        account="TEST1234",
                        strategy=[TradeStrategy.BASIC_TRADE],
                        security=SecurityType.STOCK,
                        trade_date=date(2025, 1, 23),
                        symbol="AAPL",
                        action=TradeAction.BOUGHT,
                        quantity=100,
                        fees=5.0,
                        expiration_date=value,
                        strike=5,
                        premium=1,
                        subtype=OptionType.CALL
                    )

