# Imports
from typing import List
from datetime import date, timedelta
from trading_analytics.data.data_model.trade_entry import TradeEntry, SecurityType, TradeAction
from trading_analytics.data.data_model.stock_entry import StockEntry
from trading_analytics.data.data_model.dividend_entry import DividendEntry
from trading_analytics.data.data_model.option_entry import OptionEntry, OptionType
import logging

# Configure logging for error handling
logging.basicConfig(level=logging.WARNING)


def calculate_qty_and_profit(trades: List[TradeEntry]) -> dict:
    # Initialize a dict to store aggregated profit/loss results
    results = {
        "by_symbol": {}, # {symbol: {"profit": float, "stock_qty": float, "option_qty": float}}
        "by_strategy": {} # {strategy: {"profit": float, "stock_qty": float, "option_qty": float}}
    }

    # Iterate through each trade to calculate and aggregate profit/loss
    for trade in trades:
        # Assign symbol and strategies
        symbol = trade.symbol
        strategies = [s for s in trade.strategies]

        # Initialize Dictionaries for new strategies and symbols
        # If the symbol isn't in the results yet, add it to results
        if symbol not in results["by_symbol"]:
            results["by_symbol"][symbol] = 0
        # For each strategy in the trade, add it to the results if not present
        for strategy in strategies:
            if strategy not in results["by_strategy"]:
                results["by_strategy"][strategy] = 0

        # Calculate profit/loss based on teh trade type
        # Stock
        if isinstance(trade, StockEntry):
            # For stock trades, profit/loss depends on the action
            if trade.action == TradeAction.BOUGHT:
                stock_qty = trade.quantity
                option_qty = 0
                profit = -trade.price_per_share * trade.quantity - trade.fees
            elif trade.action == TradeAction.SOLD:
                stock_qty = -trade.quantity
                option_qty = 0
                profit = trade.price_per_share * trade.quantity - trade.fees
            else:
                # Log warning for unexpected actions and treat as no impact
                logging.warning(f"Unexpected action {trade.action} for StockEntry trade_id {trade.trade_id}")
                stock_qty = 0
                option_qty = 0
                profit = 0

        # Dividend
        elif isinstance(trade, DividendEntry):
            # For dividends, profit is the dividend amount, minus fees
            stock_qty = 0
            option_qty = 0
            profit = trade.dividend_amount - trade.fees

        # Options
        elif isinstance(trade, OptionEntry):
            # Sold Calls
            if trade.option_type == OptionType.CALL:
                if trade.action in [TradeAction.SOLD_SHORT, TradeAction.SOLD_CLOSE]:
                    stock_qty = 0
                    option_qty = -trade.quantity
                    profit = trade.premium * trade.quantity * 100 - trade.fees
                elif trade.action in [TradeAction.BOUGHT_OPEN, TradeAction.BOUGHT_COVER]:
                    stock_qty = 0
                    option_qty = trade.quantity
                    profit = -trade.premium * trade.quantity * 100 - trade.fees
                elif trade.action == TradeAction.OPTION_EXPIRED:
                    stock_qty = 0
                    option_qty = -trade.quantity
                    profit = 0
                elif trade.action == TradeAction.OPTION_ASSIGNED:
                    stock_qty = -trade.quantity * 100
                    option_qty = -trade.quantity
                    profit = trade.quantity * trade.strike * 100 - trade.fees
                else:
                    # Log warning for unexpected actions
                    logging.warning(f"Unexpected action {trade.action} for OptionEntry trade_id {trade.trade_id}")
                    stock_qty = 0
                    option_qty = 0
                    profit = 0

            elif trade.option_type == OptionType.PUT:
                if trade.action == TradeAction.BOUGHT_OPEN:
                    stock_qty = 0
                    option_qty = trade.quantity
                    profit = -trade.premium * trade.quantity * 100 - trade.fees
                elif trade.action == TradeAction.SOLD_CLOSE:
                    stock_qty = 0
                    option_qty = -trade.quantity
                    profit = trade.premium * trade.quantity * 100 - trade.fees
                elif trade.action == TradeAction.OPTION_EXPIRED:
                    stock_qty = 0
                    option_qty = -trade.quantity
                    profit = 0
                else:
                    # Log warning for unexpected actions
                    logging.warning(f"Unexpected action {trade.action} for OptionEntry trade_id {trade.trade_id}")
                    stock_qty = 0
                    stock_qty = 0
                    option_qty = 0

        # Aggregate the quantities and profits at symbol and strategy levels
        results["by_symbol"][symbol] += profit
        for strategy in strategies:
            results["by_strategy"][strategy] += profit

    return results






