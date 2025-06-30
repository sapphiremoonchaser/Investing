import unittest

from trading_analytics.data.data_model.trade_entry import Brokerage, TradeEntry, SecurityType, TradeAction, TradeStrategy
from trading_analytics.data.data_model.dividend_entry import DividendEntry
from datetime import date
from pydantic import ValidationError


class TestDividendAmount(unittest.TestCase):
    """Unit tests for validating dividend amount in DividendEntry.

    Valid Test Cases:
        positive integers
        positive decimals
        0

    Invalid Test Cases:
        negative integers
        negative decimals
        None
    """
    def test_valid_dividend_amount(self):
        """Tests the validation of dividend amount values for TradeEntry.

        Iterates through a list of valid dividend amounts inputs, positive numbers.

        Args:
            self: The test case instance.
        """
        valid_dividend_amount = [1, 0.51, 0]
        for value in valid_dividend_amount:
            with self.subTest(value=value):
                # dividend_entry = DividendEntry(dividend_amount=value)
                dividend_entry = DividendEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.DIVIDEND],
                    security=SecurityType.DIVIDEND,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.DIVIDEND,
                    quantity=100,
                    fees=0.05,
                    dividend_amount=value
                )
                self.assertEqual(dividend_entry.dividend_amount, value)

    def test_invalid_fees(self):
        """Tests the validation of invalid fees values for TradeEntry.

        Iterates through a list of invalid fees inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the fees is not a positive float.
        """
        invalid_fees = [-1, -0.5, 'a', None]
        for value in invalid_fees:
            with self.assertRaises(ValidationError):
                TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=value,
                    fees=5.0
                )



if __name__ == '__main__':
    unittest.main()