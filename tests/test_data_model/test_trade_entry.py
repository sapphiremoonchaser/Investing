# Imports
import unittest
from datetime import date
from pydantic import ValidationError

from data.enum.trade_strategy import TradeStrategy
from data.enum.security_type import SecurityType
from data.enum.trade_action import TradeAction
from data.data_model.entry.trade_entry import TradeEntry


class TestTradeId(unittest.TestCase):
    """Unit tests for validating trade_id values in TradeEntry.

    Valid Test Cases:
        positive integers

    Invalid Test Cases:
        0
        negative integers
        decimals
        None
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
                    brokerage='ETRADE',
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
        invalid_trade_ids = [-1, 0.5, 0, None]
        for value in invalid_trade_ids:
            with self.assertRaises(ValidationError):
                TradeEntry(
                    trade_id=value,
                    strategy_id=1,
                    brokerage='etrade',
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
        None
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
                    brokerage='ETRADE',
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
        invalid_strategy_ids = [-1, 0.5, 0, None]
        for value in invalid_strategy_ids:
            with self.assertRaises(ValidationError):
                TradeEntry(
                    trade_id=1,
                    strategy_id=value,
                    brokerage='etrade',
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
    """
    def test_valid_brokerage(self):
        """Tests the validation of brokerage values for TradeEntry.

        Iterates through a list of valid brokerage inputs, including Brokerage enum values
        and their string equivalents (case-insensitive), to ensure they are correctly
        validated and normalized to the Brokerage enum.

        Args:
            self: The test case instance.
        """
        valid_brokerages = ["ETRADE", "vanguard"]
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
                self.assertEqual(trade_entry.brokerage, value.upper())

    def test_invalid_brokerage(self):
        """Tests the validation of invalid brokerage values for TradeEntry.

        Iterates through a list of invalid brokerage inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the brokerage value is invalid.
        """
        invalid_brokerages = ["", None]
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
        None (bc validator can handle this)

    Invalid Test Cases:
        string less than length 4
        integer less than length 4
    """
    def test_valid_account(self):
        """Tests the validation of account values for TradeEntry.

        Args:
            self: The test case instance.
        """
        valid_accounts = ['1234', 12345, None]
        for value in valid_accounts:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='etrade',
                    account=value,
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )
                self.assertEqual(trade_entry.account, str(value))

    def test_invalid_account(self):
        """Tests the validation of invalid account values for TradeEntry.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the account is not a positive integer.
        """
        invalid_accounts = ['123', 123]
        for value in invalid_accounts:
            with self.assertRaises(ValidationError):
                TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='etrade',
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
        valid_securities = [SecurityType.STOCK, SecurityType.ETF, 'STOCK', 'ETF']
        for value in valid_securities:
            with self.subTest(value=value):
                # Create a valid TradeEntry instance to test security validate
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='etrade',
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
        invalid_securities = [SecurityType.DIVIDEND, SecurityType.OPTION, "Heather", "", None]
        for value in invalid_securities:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage='etrade',
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
                    brokerage='etrade',
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
        invalid_securities = [SecurityType.OPTION, SecurityType.ETF, SecurityType.STOCK, "Heather", "", None]
        for value in invalid_securities:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage='etrade',
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
                    brokerage='etrade',
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
        invalid_securities = [SecurityType.DIVIDEND, SecurityType.ETF, SecurityType.STOCK, "Heather", "", None]
        for value in invalid_securities:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage='etrade',
                        account="TEST1234",
                        strategy=[TradeStrategy.BASIC_TRADE],
                        security=value,
                        trade_date=date(2023, 10, 15),
                        symbol="AAPL",
                        action=TradeAction.OPTION_ASSIGNED,
                        quantity=100,
                        fees=5.0
                    )


class TestTradeDate(unittest.TestCase):
    """Unit tests for validating trade date values in TradeEntry.

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
    def test_valid_trade_date(self):
        # valid_trade_dates = [date(2025,1,23), "2025-01-23"]
        valid_trade_dates = [date(2025, 1, 23),]
        for value in valid_trade_dates:
            with self.subTest(value=value):
                # Create a valid TradeEntry instance to test brokerage validation
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='etrade',
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=value,
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )
                self.assertEqual(trade_entry.trade_date, value)


    def test_invalid_trade_date(self):
        """Tests the validation of invalid trade date values for TradeEntry.

        Iterates through a list of invalid trade_date inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the trade_date value is invalid.
        """
        invalid_trade_dates = ["14-10-2014", "2022-14-09", "Heather", "", None]
        for value in invalid_trade_dates:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage='ETRADE',
                        account="TEST1234",
                        strategy=[TradeStrategy.BASIC_TRADE],
                        security=SecurityType.STOCK,
                        trade_date=value,
                        symbol="AAPL",
                        action=TradeAction.BOUGHT,
                        quantity=100,
                        fees=5.0
                    )


class TestSymbol(unittest.TestCase):
    """Unit tests for validating symbol values in TradeEntry.

    Valid Test Cases:
        string with a length of at least 1

    Invalid Test Cases:
        empty string
    """
    def test_valid_symbol(self):
        """Tests the validation of symbol values for TradeEntry.

        Args:
            self: The test case instance.
        """
        valid_symbols = ['A', 'DSX']
        for value in valid_symbols:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='etrade',
                    account='1234',
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol=value,
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )
                self.assertEqual(trade_entry.symbol, value)

    def test_invalid_symbol(self):
        """Tests the validation of invalid symbol values for TradeEntry.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the symbol is not a positive integer.
        """
        invalid_symbols = ['']
        for value in invalid_symbols:
            with self.assertRaises(ValidationError):
                TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='ETRADE',
                    account='1234',
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol=value,
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=5.0
                )


class TestAction(unittest.TestCase):
    """Unit tests for validating action types in TradeEntry.

    Valid Test Cases:
        - everything from enum class TradeAction
        - UPPERCASE valid strings
        - lowercase valid strings

    Invalid Test Cases:
        - string that is not the equivalent of something in SecurityType enum class
        - empty string
        - None

    ToDo (other tests):
        - lower cases for everything
    """
    def test_valid_action_dividend(self):
        """Tests the validation of action types where security type is 'dividend' for TradeEntry.

        Iterates through a list of valid action inputs, including TradeAction enum values
        and their string equivalents (case-insensitive), to ensure they are correctly
        validated and normalized to the TradeAction enum.

        Args:
            self: The test case instance.
        """
        valid_actions = [TradeAction.DIVIDEND, "DIVIDEND"]
        for value in valid_actions:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=2,
                    brokerage='etrade',
                    account="TEST1234",
                    strategy=[TradeStrategy.DIVIDEND],
                    security=SecurityType.DIVIDEND,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=value,
                    quantity=100,
                    fees=5.0
                )
                self.assertEqual(trade_entry.action, value)

    def test_invalid_action_dividend(self):
        """Tests the validation of invalid action types when security type is 'dividend' for TradeEntry.

        Iterates through a list of invalid action inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the action type is invalid.
        """
        invalid_actions = ["Heather", "", None]
        for value in invalid_actions:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage='etrade',
                        account="TEST1234",
                        strategy=[TradeStrategy.DIVIDEND],
                        security=SecurityType.DIVIDEND,
                        trade_date=date(2023, 10, 15),
                        symbol="AAPL",
                        action=value,
                        quantity=100,
                        fees=5.0
                    )

    def test_valid_action_stock_index(self):
        """Tests the validation of action types where security type is 'stock' or 'index' for TradeEntry.

        Iterates through a list of valid action inputs, including TradeAction enum values
        and their string equivalents (case-insensitive), to ensure they are correctly
        validated and normalized to the TradeAction enum.

        Args:
            self: The test case instance.
        """
        valid_actions = [TradeAction.BOUGHT, TradeAction.SOLD, "BOUGHT", "SOLD"]
        for value in valid_actions:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=2,
                    brokerage='etrade',
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=value,
                    quantity=100,
                    fees=5.0
                )
                self.assertEqual(trade_entry.action, value)

    def test_invalid_action_stock_index(self):
        """Tests the validation of invalid action types when security type is 'option' for TradeEntry.

        Iterates through a list of invalid action inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the action type is invalid.
        """
        invalid_actions = ["Heather", "", None]
        for value in invalid_actions:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage='etrade',
                        account="TEST1234",
                        strategy=[TradeStrategy.BASIC_TRADE],
                        security=SecurityType.ETF,
                        trade_date=date(2023, 10, 15),
                        symbol="AAPL",
                        action=value,
                        quantity=100,
                        fees=5.0
                    )

    def test_valid_action_option(self):
        """Tests the validation of action types where security type is 'option' for TradeEntry.

        Iterates through a list of valid action inputs, including TradeAction enum values
        and their string equivalents (case-insensitive), to ensure they are correctly
        validated and normalized to the TradeAction enum.

        Args:
            self: The test case instance.
        """
        valid_actions = [TradeAction.BOUGHT_COVER, TradeAction.OPTION_EXERCISED, TradeAction.SOLD_SHORT,
                         "BOUGHT COVER", "OPTION ASSIGNED", "OPTION EXPIRED"]
        for value in valid_actions:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=2,
                    brokerage='etrade',
                    account="TEST1234",
                    strategy=[TradeStrategy.COVERED_CALL],
                    security=SecurityType.OPTION,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=value,
                    quantity=100,
                    fees=5.0
                )
                self.assertEqual(trade_entry.action, value)

    def test_invalid_action_option(self):
        """Tests the validation of invalid action types when security type is 'option' for TradeEntry.

        Iterates through a list of invalid action inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the action type is invalid.
        """
        invalid_actions = ["Heather", "", None]
        for value in invalid_actions:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    TradeEntry(
                        trade_id=1,
                        strategy_id=1,
                        brokerage='etrade',
                        account="TEST1234",
                        strategy=[TradeStrategy.COVERED_CALL],
                        security=SecurityType.OPTION,
                        trade_date=date(2023, 10, 15),
                        symbol="AAPL",
                        action=value,
                        quantity=100,
                        fees=5.0
                    )


class TestQuantity(unittest.TestCase):
    """Unit tests for validating quantity values in TradeEntry.

    Valid Test Cases:
        positive integers
        decimals
        0

    Invalid Test Cases:
        negative integers
        negative decimals
        None
    """
    def test_valid_quantity(self):
        """Tests the validation of quantity values for TradeEntry.

        Iterates through a list of valid quantity inputs, positive numbers.

        Args:
            self: The test case instance.
        """
        valid_quantities = [100, 1.4, 0]
        for value in valid_quantities:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='etrade',
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=value,
                    fees=5.0
                )
                self.assertEqual(trade_entry.quantity, value)

    def test_invalid_quantity(self):
        """Tests the validation of invalid quantity values for TradeEntry.

        Iterates through a list of invalid quantity inputs to ensure they raise a ValidationError
        when used in a TradeEntry instance.

        Args:
            self: The test case instance.

        Raises:
            ValidationError: If the quantity is not a positive float.
        """
        invalid_quantities = [-1, -0.5, 'a', None]
        for value in invalid_quantities:
            with self.assertRaises(ValidationError):
                TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='etrade',
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=value,
                    fees=5.0
                )


class TestFees(unittest.TestCase):
    """Unit tests for validating fees values in TradeEntry.

    Valid Test Cases:
        positive integers
        decimals
        0

    Invalid Test Cases:
        negative integers
        negative decimals
        None
    """
    def test_valid_fees(self):
        """Tests the validation of fees values for TradeEntry.

        Iterates through a list of valid fees inputs, positive numbers.

        Args:
            self: The test case instance.
        """
        valid_fees = [1, 0.51, 0]
        for value in valid_fees:
            with self.subTest(value=value):
                trade_entry = TradeEntry(
                    trade_id=1,
                    strategy_id=1,
                    brokerage='etrade',
                    account="TEST1234",
                    strategy=[TradeStrategy.BASIC_TRADE],
                    security=SecurityType.STOCK,
                    trade_date=date(2023, 10, 15),
                    symbol="AAPL",
                    action=TradeAction.BOUGHT,
                    quantity=100,
                    fees=value
                )
                self.assertEqual(trade_entry.fees, value)

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
                    brokerage='etrade',
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

