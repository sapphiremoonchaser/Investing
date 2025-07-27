# Imports
import unittest
from datetime import date
from trading_analytics.data.enum.security_type import SecurityType
from trading_analytics.data.enum.trade_action import TradeAction
from trading_analytics.data.enum import OptionType
from trading_analytics.data.data_model.entry.stock_entry import StockEntry
from trading_analytics.data.data_model import DividendEntry
from trading_analytics.data.data_model.entry.option_entry import OptionEntry
from trading_analytics.journal.core.calculate_profit import calculate_qty_and_profit

class TestCalculateProfit(unittest.TestCase):
    def setUp(self):
        """Create test situations"""
        self.trades = [
            # Test 1: buy, sell, receive dividend, covered call
            # Stock buy: increases stock_qty, negative profit
            StockEntry(
                trade_id=1,
                strategy_id=1,
                brokerage='etrade',
                account="TEST1234",
                strategy=['basic trade'],
                security=SecurityType.STOCK,
                trade_date=date(2023, 10, 15),
                symbol="AAPL",
                action=TradeAction.BOUGHT,
                quantity=100,
                fees=5.0,
                price_per_share=150.0
            ),
            # Stock sell: decreases stock_qty, positive profit
            StockEntry(
                trade_id=2,
                strategy_id=2,
                brokerage='etrade',
                account="TEST1234",
                strategy=['basic trade'],
                security=SecurityType.STOCK,
                trade_date=date(2023, 10, 16),
                symbol="AAPL",
                action=TradeAction.SOLD,
                quantity=50,
                fees=3.0,
                price_per_share=160.0
            ),
            # Dividend: no quantity change, positive profit
            DividendEntry(
                trade_id=3,
                strategy_id=3,
                brokerage='etrade',
                account="TEST1234",
                strategy=['dividend'],
                security=SecurityType.DIVIDEND,
                trade_date=date(2023, 10, 16),
                symbol="AAPL",
                action=TradeAction.DIVIDEND,
                quantity=100,
                fees=0.0,
                dividend_amount=0.5
            ),
            # Option sell (call): decreases option_qty, positive profit
            OptionEntry(
                trade_id=4,
                strategy_id=4,
                brokerage='etrade',
                account="TEST1234",
                strategy=['covered call'],
                security=SecurityType.OPTION,
                trade_date=date(2023, 10, 17),
                symbol="AAPL",
                action=TradeAction.SOLD_SHORT,
                quantity=1,
                fees=1.0,
                expiration_date=date(2023, 11, 17),
                strike=150.0,
                premium=2.0,
                option_type=OptionType.CALL
            ),

            # Test 2
            # buy put, put ASSIGNED
            # Option buy (put): increases option_qty, negative profit
            OptionEntry(
                trade_id=5,
                strategy_id=5,
                brokerage='etrade',
                account="TEST1234",
                strategy=['basic option'],
                security=SecurityType.OPTION,
                trade_date=date(2023, 10, 18),
                symbol="MSFT",
                action=TradeAction.BOUGHT_OPEN,
                quantity=2,
                fees=2.0,
                expiration_date=date(2023, 11, 17),
                strike=300.0,
                premium=3.0,
                option_type=OptionType.PUT
            ),
            # Option assigned (put): increases stock_qty, decreases option_qty, negative profit
            OptionEntry(
                trade_id=6,
                strategy_id=6,
                brokerage='etrade',
                account="TEST1234",
                strategy=['basic option'],
                security=SecurityType.OPTION,
                trade_date=date(2023, 10, 19),
                symbol="MSFT",
                action=TradeAction.OPTION_ASSIGNED,
                quantity=1,
                fees=1.0,
                expiration_date=date(2023, 11, 19),
                strike=300.0,
                premium=10,
                option_type=OptionType.PUT
            ),
            # # Multiple strategies (for future-proofing): should log warning
            # StockEntry(
            #     trade_id=8,
            #     strategy_id=8,
            #     brokerage='etrade',
            #     account="TEST1234",
            #     strategy=['dividend', 'covered call'],
            #     security=SecurityType.STOCK,
            #     trade_date=date(2023, 10, 21),
            #     symbol="AAPL",
            #     action=TradeAction.BOUGHT,
            #     quantity=10,
            #     fees=1.0,
            #     price_per_share=170.0
            # )
        ]

    def test_aggregate_by_symbol_and_strategy(self):
        results = calculate_qty_and_profit(self.trades)

        # Buy Symbol
        # Verify buy STOCK, sell STOCK, receive DIVIDEND, buy CALL (by symbol)
        # AAPL
        # Profit: -100(150) -5 + 100(50) - 3 + 0.5 -1 + 2(100)= -6808.5
        # Stock_qty: +100 - 50 = 50
        # Option_qty: -1
        self.assertAlmostEqual(results["by_symbol"]["AAPL"]["profit"], -6808.5)
        self.assertAlmostEqual(results["by_symbol"]["AAPL"]["stock_qty"], 50.0)
        self.assertAlmostEqual(results["by_symbol"]["AAPL"]["option_qty"], 1)

        # By Symbol
        # Verify buy PUT, put assigned
        # MFST
        # Profit: -2(3)(100) - 2 = -602
        # Stock_qty: 0
        # Option_qty: +2
        self.assertAlmostEqual(results["by_symbol"]["MSFT"]["profit"], -30603.0)
        self.assertAlmostEqual(results["by_symbol"]["MSFT"]["stock_qty"], 100)
        self.assertAlmostEqual(results["by_symbol"]["MSFT"]["option_qty"], 1)

        # # by Strategy = DIVIDEND
        # # symbol = AAPL
        # # Profit: 0.5
        # # Stock_qty: 0
        # # Option_qty: 0
        # self.assertAlmostEqual(results["by_strategy"]["DIVIDEND"]["AAPL"]["profit"], 0.5)
        # self.assertAlmostEqual(results["by_strategy"]["DIVIDEND"]["AAPL"]["stock_qty"], 0)
        # self.assertAlmostEqual(results["by_strategy"]["DIVIDEND"]["AAPL"]["option_qty"], 0.0)
        #
        # # by strategy = BASIC_TRADE
        # # symbol = AAPL
        # # Profit: -100(150) - 5 + 50(160) - 3 = -7008
        # # Stock_qty: -50 (sell) = -50
        # # Option_qty: 0 (sell) = 0
        # self.assertAlmostEqual(results["by_strategy"]["BASIC TRADE"]["AAPL"]["profit"], -7008)
        # self.assertAlmostEqual(results["by_strategy"]["BASIC TRADE"]["AAPL"]["stock_qty"], 50.0)
        # self.assertAlmostEqual(results["by_strategy"]["BASIC TRADE"]["AAPL"]["option_qty"], 0.0)

        # # Verify by_strategy for COVERED_CALL
        # # Profit: 199 (call sold) = 199
        # # Stock_qty: 0 (call sold) = 0
        # # Option_qty: -1 (call sold) = -1
        # self.assertAlmostEqual(results["by_strategy"]["COVERED_CALL"]["profit"], 199.0)
        # self.assertAlmostEqual(results["by_strategy"]["COVERED_CALL"]["stock_qty"], 0.0)
        # self.assertAlmostEqual(results["by_strategy"]["COVERED_CALL"]["option_qty"], -1.0)
        #
        # # Verify by_strategy for PUT
        # # Profit: -602 (put bought) - 30001 (put assigned) = -30603
        # # Stock_qty: 0 (put bought) + 100 (put assigned) = 100
        # # Option_qty: +2 (put bought) - 1 (put assigned) = 1
        # self.assertAlmostEqual(results["by_strategy"]["PUT"]["profit"], -30603.0)
        # self.assertAlmostEqual(results["by_strategy"]["PUT"]["stock_qty"], 100.0)
        # self.assertAlmostEqual(results["by_strategy"]["PUT"]["option_qty"], 1.0)
        #
        # # Verify that invalid action and multi-strategy trades are skipped
        # self.assertNotIn("COVERED_CALL", results["by_strategy"])  # From multi-strategy trade

if __name__ == "__main__":
    unittest.main()

