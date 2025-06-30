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

class TestSecurity(unittest.TestCase):
    """Unit tests for validating security types in TradeEntry.

    This class contains test cases to verify the behavior of security type validation,
    ensuring valid security types (STOCK, INDEX, DIVIDEND, OPTION) are correctly normalized
    and invalid inputs raise appropriate ValidationError exceptions.

    Attributes:
        None
    """
    def test_valid_stock_index(self):
        """Tests the validation of stock and index security types for TradeEntry.

        Iterates through a list of valid security inputs, including SecurityType enum values
        and their string equivalents (case-insensitive), to ensure they are correctly
        validated and normalized to the SecurityType enum.

        Args:
            self: The test case instance.
        """
        valid_securities = [SecurityType.STOCK, SecurityType.INDEX, 'STOCK', 'index']
        for value in valid_securities:
            with self.subTest(value=value):
                # Create a valid TradeEntry instance to test security validate
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=value,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )
                self.assertIn(trade_entry.security, list(SecurityType))

    def test_invalid_stock_index(self):
        """Tests the validation of invalid security types for TradeEntry.

        Iterates through a list of invalid security inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the security type is invalid.
        """
        """Tests the validation of invalid brokerage values for TradeEntry.

        Iterates through a list of invalid brokerage inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the brokerage value is invalid.
        """
        invalid_brokerages = [SecurityType.DIVIDEND, SecurityType.OPTION, "Heather", "", None]
        for value in invalid_brokerages:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage=Brokerage.ETRADE,
                        account="TEST1234",
                        strategy=[TradeStrategy.BASIC_TRADE],
                        security=value,
                        trade_date=date(2023, 10, 15),
                        symbol="AAPL",
                        action=TradeAction.BOUGHT,
                        quantity=100,
                        fees=5.0
                    )

    def test_valid_dividend(self):
        """Tests the validation of dividend security types for TradeEntry.

        Iterates through a list of valid dividend security inputs, including SecurityType enum values
        and their string equivalents (case-insensitive), to ensure they are correctly
        validated and normalized to the SecurityType enum.

        Args:
            self: The test case instance.
        """
        valid_securities = [SecurityType.DIVIDEND, 'DIVIDEND', 'dividend']
        for value in valid_securities:
            with self.subTest(value=value):
                # Create a valid TradeEntry instance to test security validate
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=value,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.DIVIDEND,
                    quantity=100,
                    fees=5.0
                )
                self.assertIn(trade_entry.security, list(SecurityType))

    def test_invalid_dividend(self):
        """Tests the validation of invalid security types for dividend TradeEntry.

        Iterates through a list of invalid security inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance with a dividend action.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the security type is invalid for a dividend action.
        """
        invalid_securities = [SecurityType.OPTION, SecurityType.INDEX, SecurityType.STOCK, "Heather", "", None]
        for value in invalid_securities:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage=Brokerage.ETRADE,
                        account="TEST1234",
                        strategy=[TradeStrategy.BASIC_TRADE],
                        security=value,
                        trade_date=date(2023, 10, 15),
                        symbol="AAPL",
                        action=TradeAction.DIVIDEND,
                        quantity=100,
                        fees=5.0
                    )

    def test_valid_option(self):
        """Tests the validation of option security types for TradeEntry.

        Iterates through a list of valid option security inputs, including SecurityType enum values
        and their string equivalents (case-insensitive), to ensure they are correctly
        validated and normalized to the SecurityType enum.

        Args:
            self: The test case instance.
        """
        valid_securities = [SecurityType.OPTION, 'OPTION', 'option']
        for value in valid_securities:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=value,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.OPTION_ASSIGNED,
                    quantity=100,
                    fees=5.0
                )
                self.assertIn(trade_entry.security, list(SecurityType))

    def test_invalid_option(self):
        """Tests the validation of invalid security types for option TradeEntry.

        Iterates through a list of invalid security inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance with an option-related action.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the security type is invalid for an option action.
        """
        invalid_securities = [SecurityType.DIVIDEND, SecurityType.INDEX, SecurityType.STOCK, "Heather", "", None]
        for value in invalid_securities:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage=Brokerage.ETRADE,
                        account="TEST1234",
                        strategy=[TradeStrategy.BASIC_TRADE],
                        security=value,
                        trade_date=date(2023, 10, 15),
                        symbol="AAPL",
                        action=TradeAction.OPTION_ASSIGNED,
                        quantity=100,
                        fees=5.0
                    )

if __name__ == '__main__':
    unittest.main()

