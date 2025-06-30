import unittest

from trading_analytics.data.data_model.trade_entry import Brokerage, TradeEntry, SecurityType, TradeAction, TradeStrategy
from datetime import date
from pydantic import ValidationError


class TestTradeId(unittest.TestCase):
    """Unit tests for validating trade_id values in TradeEntry.

    Valid Test Cases:
        positive integers

    Invalid Test Cases:
        0
        negative integers
        decimals
    """
    def test_valid_trade_id(self):
        """Tests the validation of trade_id values for TradeEntry.

        Iterates through a list of valid trade_id inputs, positive numbers.

        Args:
            self: The test case instance.
        """
        valid_trade_ids = [1, 10, 100]
        for value in valid_trade_ids:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=value,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )
                self.assertEqual(trade_entry.trade_id, value)

    def test_invalid_trade_id(self):
        """Tests the validation of invalid trade_id values for TradeEntry.

        Iterates through a list of invalid trade_id inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the trade_id is not a positive integer.
        """
        invalid_trade_ids = [-1, 0.5, 0]
        for value in invalid_trade_ids:
            with self.assertRaises(ValidationError):
                TradeEntry(
                    trade_id=value,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )


class TestStrategyId(unittest.TestCase):
    """Unit tests for validating strategy_id values in TradeEntry.

    Valid Test Cases:
        positive integers

    Invalid Test Cases:
        0
        negative integers
        decimals
    """
    def test_valid_strategy_id(self):
        """Tests the validation of strategy_id values for TradeEntry.

        Iterates through a list of valid strategy_id inputs, positive numbers.

        Args:
            self: The test case instance.
        """
        valid_strategy_ids = [1, 10, 100]
        for value in valid_strategy_ids:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=value,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )
                self.assertEqual(trade_entry.strategy_id, value)

    def test_invalid_strategy_id(self):
        """Tests the validation of invalid strategy_id values for TradeEntry.

        Iterates through a list of invalid strategy_id inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the trade_id is not a positive integer.
        """
        invalid_strategy_ids = [-1, 0.5, 0]
        for value in invalid_strategy_ids:
            with self.assertRaises(ValidationError):
                TradeEntry(
                    trade_id=1,
                    strategy_id=value,
                    brokerage=Brokerage.ETRADE,
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )


class TestBrokerage(unittest.TestCase):
    """Unit tests for validating brokerage values in TradeEntry.

    Valid Test Cases:
        UPPERCASE valid brokerage name, (ETRADE)
        lowercase valid brokerage name (etrade)

    Invalid Test Cases:
        None,
        invalid string

    ToDo:
        Enum Bokerage?

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


class TestAccount(unittest.TestCase):
    """Unit tests for validating account values in TradeEntry.

    Valid Test Cases:
        string with a length of at least 4

    Invalid Test Cases:
        string less than length 4
        integer instead of string (ToDo: Fix this so that convert to str before applying field constraints)
    """
    def test_valid_account(self):
        """Tests the validation of account values for TradeEntry.

        Args:
            self: The test case instance.
        """
        valid_accounts = ['1234']
        for value in valid_accounts:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account=value,
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )
                self.assertEqual(trade_entry.account, value)

    def test_invalid_account(self):
        """Tests the validation of invalid trade_id values for TradeEntry.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the trade_id is not a positive integer.
        """
        invalid_accounts = [1234, '123']
        for value in invalid_accounts:
            with self.assertRaises(ValidationError):
                TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage=Brokerage.ETRADE,
                    account=value,
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )



# ToDo: test strategy

class TestSecurity(unittest.TestCase):
    """Unit tests for validating security types in TradeEntry.

    This is split into stock/index, dividend, and option since action would be distinctly different among each set.

    Valid Test Cases:
        - everything from enum class SecurityType
        - UPPERCASE valid strings
        - lowercase valid strings

    Invalid Test Cases:
        - string that is not the equivalent of something in SecurityType enum class
        - empty string
        - None

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
        invalid_securities = [SecurityType.DIVIDEND, SecurityType.OPTION, "Heather", "", None]
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

# ToDo: test trade date

# ToDo: test symbol

# ToDo: test action

# ToDo: test quantity

# ToDo: test fees

if __name__ == '__main__':
    unittest.main()

