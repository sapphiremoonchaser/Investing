import unittest

from trading_analytics.data.data_model.trade_entry import Brokerage, TradeEntry, SecurityType, TradeAction, TradeStrategy
from datetime import date
from pydantic import ValidationError


class TestBrokerage(unittest.TestCase):
    """Unit tests for validating brokerage values in TradeEntry.

    This class contains test cases to verify the behavior of brokerage validation,
    ensuring valid inputs are correctly normalized and invalid inputs raise appropriate errors.

    Attributes:
        None
    """
    def test_valid_brokerage(self):
        """Tests the validation of brokerage values for TradeEntry.

        Iterates through a list of valid brokerage inputs, including Brokerage enum values
        and their string equivalents (case-insensitive), to ensure they are correctly
        validated and normalized to the Brokerage enum.

        Args:
            self: The test case instance.
        """
        valid_brokerages = list(Brokerage) + ["ETRADE", "etrade"]
        for value in valid_brokerages:
            with self.subTest(value=value):
                # Create a valid TradeEntry instance to test brokerage validation
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage=value,
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )
                self.assertIn(trade_entry.brokerage, list(Brokerage))

    def test_invalid_brokerage(self):
        """Tests the validation of invalid brokerage values for TradeEntry.

        Iterates through a list of invalid brokerage inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the brokerage value is invalid.
        """
        invalid_brokerages = ["Heather", "", None]
        for value in invalid_brokerages:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage=value,
                        account="TEST1234",
                        strategy=[TradeStrategy.BASIC_TRADE],
                        security=SecurityType.STOCK,
                        trade_date=date(2023, 10, 15),
                        symbol="AAPL",
                        action=TradeAction.BOUGHT,
                        quantity=100,
                        fees=5.0
                    )


if __name__ == '__main__':
    unittest.main()

