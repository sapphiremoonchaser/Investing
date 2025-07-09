# Imports
import unittest
from datetime import date
from pydantic import ValidationError

from data.enum.security_type import SecurityType
from data.enum.trade_strategy import TradeStrategy
from data.enum.trade_action import TradeAction
from data.data_model.entry.stock_entry import StockEntry

class TestPricePerShare(unittest.TestCase):
    """Unit tests for validating stock/index price per share in StockEntry.

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
    def test_valid_price_per_share(self):
        """Tests the validation of price per share values for TradeEntry.

        Iterates through a list of valid price per share inputs, positive numbers.

        Args:
            self: The test case instance.
        """
        valid_price_per_share = [1, 0.51, 0]
        for value in valid_price_per_share:
            with self.subTest(value=value):
                stock_entry = StockEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='ETRADE',
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=0.05,
                    price_per_share=value
                )
                self.assertEqual(stock_entry.price_per_share, value)

    def test_invalid_price_per_share(self):
        """Tests the validation of invalid price per share values for TradeEntry.

        Iterates through a list of invalid price per share inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the price per share is not a positive float.
        """
        invalid_price_per_share = [-1, -0.5, 'a', None]
        for value in invalid_price_per_share:
            with self.assertRaises(ValidationError):
                StockEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='ETRADE',
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0,
                    price_per_share=value
                )



if __name__ == '__main__':
    unittest.main()