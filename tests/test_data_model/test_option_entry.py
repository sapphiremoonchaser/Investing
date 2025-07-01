import unittest

from trading_analytics.data.data_model.trade_entry import Brokerage, TradeEntry, SecurityType, TradeAction, TradeStrategy
from trading_analytics.data.data_model.option_entry import OptionEntry, OptionType
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


class TestStrike(unittest.TestCase):
    """Unit tests for validating strike price in OptionEntry.

    Valid Test Cases:
        positive integers
        positive decimals

    Invalid Test Cases:
        negative integers
        negative decimals
        non-numeric strings
        None
        0
    """
    def test_valid_strike(self):
        """Tests the validation of strike values for TradeEntry.

        Iterates through a list of valid strike inputs, positive numbers.

        Args:
            self: The test case instance.
        """
        valid_strike = [1, 0.51]
        for value in valid_strike:
            with self.subTest(value=value):
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
                    expiration_date=date(2025, 1, 30),
                    strike=value,
                    premium=1,
                    subtype=OptionType.CALL
                )
                self.assertEqual(option_entry.strike, value)

    def test_invalid_strike(self):
        """Tests the validation of invalid strike values for TradeEntry.

        Iterates through a list of invalid strike inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the strike is not a positive float.
        """
        invalid_strikes = [-1, -0.5, 0, 'a', None]
        for value in invalid_strikes:
            with self.assertRaises(ValidationError):
                OptionEntry(
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
                    expiration_date=date(2025, 1, 30),
                    strike=value,
                    premium=1,
                    subtype=OptionType.CALL
                )


# ToDo: Test Premium


# ToDo: Test Subtype



if __name__ == '__main__':
    unittest.main()