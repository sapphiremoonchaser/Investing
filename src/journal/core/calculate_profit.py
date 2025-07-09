# Imports
from typing import List
import logging

from data.data_model.entry.trade_entry import TradeEntry
from data.data_model.entry.dividend_entry import DividendEntry
from data.data_model.entry.stock_entry import StockEntry
from data.data_model.entry.option_entry import OptionEntry
from data.enum.option_type import OptionType
from data.enum.trade_action import TradeAction

# Configure logging to a file
logger = logging.getLogger(__name__)


def calculate_qty_and_profit(trades: List[TradeEntry]) -> dict:
    """Calculates aggregated profit/loss, stock quantity, and option quantity for a list of trades.

    Processes a list of TradeEntry instances, categorizing results by symbol and strategy.
    Handles stock, dividend, and option trades, calculating profit/loss based on trade actions
    and updating quantities accordingly.

    Args:
        trades (List[TradeEntry]): List of trade entries to process.

    Returns:
        dict: A dictionary with two keys:
            - by_symbol (dict): Aggregated results by symbol, with sub-dictionaries containing
                profit (float), stock_qty (float), and option_qty (float).
            - by_strategy (dict): Aggregated results by strategy, with sub-dictionaries containing
                profit (float), stock_qty (float), and option_qty (float).

    Raises:
        None: Logs warnings for unexpected trade types or actions without raising exceptions.

    # ToDo: what should I do with dicts?
    """
    # Initialize a dict to store aggregated profit/loss results
    results = {
        "by_symbol": {}, # {symbol: {"profit": float, "stock_qty": float, "option_qty": float}}
        "by_strategy": {} # {strategy: {symbol: {"profit": float, "stock_qty": float, "option_qty": float}}}
    }

    # Iterate through each trade to calculate and aggregate profit/loss
    for trade in trades:
        # Extract symbol and strategies
        symbol = trade.symbol
        strategy = trade.strategy[0].value

        # Initialize dict for new symbol
        if symbol not in results["by_symbol"]:
            results["by_symbol"][symbol] = {"profit": 0.0, "stock_qty": 0.0, "option_qty": 0.0}

        # Initialize dict for new strategy and symbol
        if strategy not in results["by_strategy"]:
            results["by_strategy"][strategy] = {}
        if symbol not in results["by_strategy"][strategy]:
            results["by_strategy"][strategy][symbol] = {"profit": 0.0, "stock_qty": 0.0, "option_qty": 0.0}

        # Calculate profit/loss based on teh trade type
        # Stock
        if isinstance(trade, StockEntry):
            # For stock trades, profit/loss depends on the action
            if trade.action == TradeAction.BOUGHT:
                stock_qty = trade.quantity # Positive for buying shares
                option_qty = 0
                profit = -trade.price_per_share * trade.quantity - trade.fees # Cash Outflow
            elif trade.action == TradeAction.SOLD:
                stock_qty = -trade.quantity # Negative for selling shares
                option_qty = 0
                profit = trade.price_per_share * trade.quantity - trade.fees # Cash Inflow
            else:
                # Log warning for unexpected actions and treat as no impact
                logger.warning(f"Unexpected action {trade.action} for StockEntry trade_id {trade.trade_id}")
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
                if trade.action == TradeAction.SOLD_SHORT:
                    stock_qty = 0
                    option_qty = trade.quantity # Positive for contract added to portfolio
                    profit = trade.premium * trade.quantity * 100 - trade.fees # Premium received
                elif trade.action == TradeAction.SOLD_CLOSE:
                    stock_qty = 0
                    option_qty = -trade.quantity # Negative because closing position
                    profit = trade.premium * trade.quantity * 100 - trade.fees # Premium received
                elif trade.action == TradeAction.BOUGHT_OPEN:
                    stock_qty = 0
                    option_qty = trade.quantity # Positive for contract added to portfolio
                    profit = -trade.premium * trade.quantity * 100 - trade.fees # Premium Paid
                elif trade.action == TradeAction.BOUGHT_COVER:
                    stock_qty = 0
                    option_qty = -trade.quantity # Negative because closing position
                    profit = -trade.premium * trade.quantity * 100 - trade.fees
                elif trade.action == TradeAction.OPTION_EXPIRED:
                    stock_qty = 0
                    option_qty = -trade.quantity # Remove sold contracts
                    profit = 0 # No profit/loss for expiration
                elif trade.action == TradeAction.OPTION_ASSIGNED:
                    stock_qty = -trade.quantity * 100 # Buying shares to deliver
                    option_qty = -trade.quantity # Remove assigned contract
                    profit = trade.quantity * trade.strike * 100 - trade.fees # Shares sold at strike
                elif trade.action == TradeAction.OPTION_EXERCISED:
                    stock_qty = trade.quantity * 100 # Receive shares
                    option_qty = -trade.quantity # Remove exercised contract
                    profit = -trade.quantity * trade.strike * 100 - trade.fees # Shares bought at strike
                else:
                    # Log warning for unexpected actions
                    logging.warning(f"Unexpected action {trade.action} for OptionEntry trade_id {trade.trade_id}")
                    stock_qty = 0
                    option_qty = 0
                    profit = 0

            elif trade.option_type == OptionType.PUT:
                if trade.action == TradeAction.BOUGHT_OPEN:
                    stock_qty = 0
                    option_qty = trade.quantity # Positive for buying contracts
                    profit = -trade.premium * trade.quantity * 100 - trade.fees # Premium Paid
                elif trade.action == TradeAction.SOLD_CLOSE:
                    stock_qty = 0
                    option_qty = -trade.quantity # Negative for selling contracts
                    profit = trade.premium * trade.quantity * 100 - trade.fees # Premium received
                elif trade.action == TradeAction.OPTION_EXPIRED:
                    stock_qty = 0
                    option_qty = -trade.quantity # Remove sold contacts
                    profit = 0
                elif trade.action == TradeAction.OPTION_ASSIGNED:
                    stock_qty = trade.quantity * 100 # Receive shares (100 per contract)
                    option_qty = -trade.quantity # Remove assigned contracts
                    profit = -trade.quantity * trade.strike * 100 - trade.fees # Shares bought at strike
                else:
                    # Log warning for unexpected actions
                    logger.warning(f"Unexpected action {trade.action} for OptionEntry trade_id {trade.trade_id}")
                    stock_qty = 0
                    stock_qty = 0
                    option_qty = 0

        else:
            # Log warning for unexpected trade types
            logger.warning(f"Unexpected trade type {type(trade)} for trade_id {trade.trade_id}")

        # Aggregate profit, stock_qty, and option_qty for symbol
        results["by_symbol"][symbol]["profit"] += profit
        results["by_symbol"][symbol]["stock_qty"] += stock_qty
        results["by_symbol"][symbol]["option_qty"] += option_qty

        # Aggregate profit, stock_qty, and option_qty for each strategy
        results["by_strategy"][strategy][symbol]["profit"] += profit
        results["by_strategy"][strategy][symbol]["stock_qty"] += stock_qty
        results["by_strategy"][strategy][symbol]["option_qty"] += option_qty

    return results
