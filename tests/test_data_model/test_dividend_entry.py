# Imports
import unittest
from datetime import date
from pydantic import ValidationError

from trading_analytics.data.data_model.entry.dividend_entry import DividendEntry
from trading_analytics.data.enum.security_type import SecurityType
from trading_analytics.data.enum.trade_action import TradeAction



class TestDividendAmount(unittest.TestCase):
    """Unit tests for validating dividend amount in DividendEntry.

    Valid Test Cases:
        positive integers
        positive decimals
        0

    Invalid Test Cases:
        negative integers
        negative decimals
        non-numeric strings
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
                    brokerage='ETRADE',
                    account="TEST1234",
                    strategy=['dividend'],
                    security=SecurityType.DIVIDEND,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.DIVIDEND,
                    quantity=100,
                    fees=0.05,
                    dividend_amount=value
                )
                self.assertEqual(dividend_entry.dividend_amount, value)

    def test_invalid_dividend_amount(self):
        """Tests the validation of invalid dividend amount values for TradeEntry.

        Iterates through a list of invalid dividend amount inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the dividend amount is not a positive float.
        """
        invalid_dividend_amounts = [-1, -0.5, 'a', None]
        for value in invalid_dividend_amounts:
            with self.assertRaises(ValidationError):
                DividendEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='ETRADE',
                    account="TEST1234",
                    strategy=['basic trade'],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0,
                    dividend_amount=value
                )



if __name__ == '__main__':
    unittest.main()