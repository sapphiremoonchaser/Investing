# Imports
from typing import List
import logging
import pandas as pd
from pycparser.ply.yacc import resultlimit

from data.data_model.entry.trade_entry import TradeEntry
from data.data_model.entry.dividend_entry import DividendEntry
from data.data_model.entry.stock_entry import StockEntry
from data.data_model.entry.option_entry import OptionEntry
from data.enum.option_type import OptionType
from data.enum.trade_action import TradeAction
from data.enum.sub_action import TradeSubAction

# Configure logging to a file
logger = logging.getLogger(__name__)

def _process_stock_etf_buy_trades(trades: List[TradeEntry], data_dict: dict) -> None:
    """Helper function to process STOCK and ETF buy trades and update the data dictionary.

    Args:
        trades (List[TradeEntry]): List of trade entries to process.
        data_dict (dict): Dictionary to store total_cost and total_quantity by symbol.

    Modifies:
        data_dict: Updates with total_cost and total_quantity for STOCK/ETF buy trades.
    """
    for trade in trades:
        symbol = trade.symbol

        # Initialize dit for new symbol is not already there
        if symbol not in data_dict:
            data_dict[symbol] = {"total_cost": 0.0, "total_quantity": 0.0}

        # Process STOCK or ETF trades with BUY action
        if (
            hasattr(trade, "security_type")
            and trade.security_type in ["STOCK", "ETF"]
            and trade.action == TradeAction.BUY
            and isinstance(trade, StockEntry)
        ):
            total_cost = trade.price_per_share * trade.quantity + trade.fees
            data_dict[symbol]["total_cost"] += total_cost
            data_dict[symbol]["total_quantity"] += trade.quantity


def calculate_qty_and_profit(trades: List[TradeEntry]) -> dict:
    """Calculates aggregated profit/loss, stock quantity, and option quantity for a list of trades.

    Processes a list of TradeEntry instances, categorizing results by symbol and strategy.
    Handles stock, dividend, and option trades, the quantity of shares, options contracts,
    and the current profit by symbol.

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
    """
    # Initialize aggregated profit/loss, stock quantity, and option quantity by symbol
    results = {}

    # Iterate through each trade to calculate and aggregate profit/loss
    for trade in trades:
        symbol = trade.symbol

        # Initialize dict for new symbol
        if symbol not in results.keys():
            results[symbol] = {"profit": 0.0, "stock_qty": 0.0, "option_qty": 0.0}

        # Calculate profit/loss based on teh trade type
        # Stock
        if isinstance(trade, StockEntry):
            # For stock trades, profit/loss depends on the action
            if trade.action == TradeAction.BUY:
                stock_qty = trade.quantity # Positive for buying shares
                option_qty = 0
                profit = -trade.price_per_share * trade.quantity - trade.fees # Cash Outflow
            elif trade.action == TradeAction.SELL:
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
                if trade.action == TradeAction.SELL and trade.sub_action == TradeSubAction.OPEN:
                    stock_qty = 0
                    option_qty = trade.quantity # Positive for contract added to portfolio
                    profit = trade.premium * trade.quantity * 100 - trade.fees # Premium received
                elif trade.action == TradeAction.SELL and trade.sub_action == TradeSubAction.CLOSE:
                    stock_qty = 0
                    option_qty = -trade.quantity # Negative because closing position
                    profit = trade.premium * trade.quantity * 100 - trade.fees # Premium received
                elif trade.action == TradeAction.BUY and trade.sub_action == TradeSubAction.OPEN:
                    stock_qty = 0
                    option_qty = trade.quantity # Positive for contract added to portfolio
                    profit = -trade.premium * trade.quantity * 100 - trade.fees # Premium Paid
                elif trade.action == TradeAction.BUY and trade.sub_action == TradeSubAction.CLOSE:
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
                if trade.action == TradeAction.BUY and trade.sub_action == TradeSubAction.OPEN:
                    stock_qty = 0
                    option_qty = trade.quantity # Positive for buying contracts
                    profit = -trade.premium * trade.quantity * 100 - trade.fees # Premium Paid
                elif trade.action == TradeAction.SELL and trade.sub_action == TradeSubAction.CLOSE:
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
        results[symbol]["profit"] += profit
        results[symbol]["stock_qty"] += stock_qty
        results[symbol]["option_qty"] += option_qty

    return results


def get_current_positions(results: dict) -> dict:
    """Filters symbols with non-zero stock or option quantities from the results dictionary.

    Args:
        results (dict): Dictionary from calculate_qty_and_profit_by_symbol, with symbols as keys
                       and sub-dictionaries containing 'profit', 'stock_qty', and 'option_qty'.

    Returns:
        dict: A filtered dictionary containing only symbols where stock_qty or option_qty is not zero.
    """
    active_positions = {
        symbol: data
        for symbol, data in results.items()
        if data['stock_qty'] != 0 or data['option_qty'] != 0
    }

    return active_positions


def calculate_original_buy_in(trades: List[TradeEntry]) -> dict:
    """Calculates the average buy-in price per share for STOCK and ETF trades by symbol.

    Processes a list of TradeEntry instances, considering only buy trades (TradeAction.BUY)
    for securities with type 'STOCK' or 'ETF'. Computes the average price per share by
    dividing the total cost (price_per_share * quantity + fees) by the total quantity
    of shares purchased.

    Args:
        trades (List[TradeEntry]): List of trade entries to process.

    Returns:
        dict: A dictionary with symbols as keys and the average buy-in price per share (float)
              as values. Symbols with no buy trades or zero total quantity are excluded.

    Raises:
        None: Logs warnings for unexpected trade types, actions, or zero quantities without
              raising exceptions.
    """
    buy_in_data = {}
    # _process_stock_etf_buy_trades(trades, buy_in_data)

    for trade in trades:
        symbol = trade.symbol
        if symbol not in buy_in_data:
            buy_in_data[symbol] = {"total_cost": 0.0, "total_quantity": 0.0}

        # Log trade details
        logger.info(f"Trade: symbol={symbol}, type={type(trade).__name__}, "
                    f"security_type={getattr(trade, 'security_type', None)}, "
                    f"action={getattr(trade, 'action', None)}, "
                    f"action_type={type(getattr(trade, 'action', None)).__name__}, "
                    f"quantity={getattr(trade, 'quantity', None)}")

        # Check conditions
        if not isinstance(trade, StockEntry):
            logger.warning(f"Trade {trade.trade_id} skipped: not a StockEntry, type={type(trade).__name__}")
            continue
        # Fallback: Assume STOCK if  security_type is None
        security_type = getattr(trade, 'security_type', 'STOCK')
        if security_type not in ["STOCK", "ETF"]:
            logger.warning(f"Trade {trade.trade_id} skipped: invalid security_type={security_type}")
            continue
        if trade.action != TradeAction.BUY:
            logger.warning(f"Trade {trade.trade_id} skipped: action={trade.action} is not BUY")
            continue

        total_cost = trade.price_per_share * trade.quantity + trade.fees
        buy_in_data[symbol]["total_cost"] += total_cost
        buy_in_data[symbol]["total_quantity"] += trade.quantity
        logger.info(f"Trade {trade.trade_id} processed: cost={total_cost}, qty={trade.quantity}")

    # Calculate average buy-in price per share by symbol
    result = {}
    for symbol, data in buy_in_data.items():
        if data["total_quantity"] > 0:
            avg_price = data["total_cost"] / data["total_quantity"]
            result[symbol] = avg_price
        else:
            logger.warning(f"No valid buy quantity {data['total_quantity']} for {symbol}")

    return result


def calculate_adjusted_buy_in(trades: List[TradeEntry]) -> dict:
    """Calculates the adjusted buy-in price per share for STOCK and ETF trades by symbol.

    Processes a list of TradeEntry instances, considering buy trades (TradeAction.BUY) for
    securities with type 'STOCK' or 'ETF', option trades (premiums bought or sold), and
    dividend trades. The adjusted buy-in price accounts for the total cost of stock/ETF buys,
    net option premiums (received minus paid), and dividends received, divided by the total
    quantity of shares purchased.

    Args:
        trades (List[TradeEntry]): List of trade entries to process.

    Returns:
        dict: A dictionary with symbols as keys and the adjusted buy-in price per share (float)
              as values. Symbols with no buy trades or zero total quantity are excluded.

    Raises:
        None: Logs warnings for unexpected trade types, actions, or zero quantities without
              raising exceptions.
    """
    adjusted_data = {}
    _process_stock_etf_buy_trades(trades, adjusted_data)

    for trade in trades:
        symbol = trade.symbol

        # Initialize dict for new symbols
        if symbol not in adjusted_data:
            adjusted_data[symbol] = {
                "total_cost": 0.0,
                "total_quantity": 0.0,
                "net_option_premiums": 0.0,
                "total_dividends": 0.0
            }

        # Option Trades (premiums)
        if isinstance(trade, OptionEntry):
            if trade.option_type in [OptionType.CALL, OptionType.PUT]:
                if (
                    trade.action == TradeAction.SELL
                    and trade.sub_action in [TradeSubAction.OPEN, TradeSubAction.CLOSE]
                ):
                    premium = trade.premium  * trade.quantity * 100 - trade.fees
                    adjusted_data[symbol]["net_option_premiums"] += premium

                elif (
                        trade.action == TradeAction.BUY
                    and trade.sub_action in [TradeSubAction.OPEN, TradeSubAction.CLOSE]
                ):
                    premium = -trade.premium * trade.quantity * 100 - trade.fees
                    adjusted_data[symbol]["net_option_premiums"] += premium

        # Dividend Trades
        elif isinstance(trade, DividendEntry):
            dividend = trade.dividend_amount - trade.fees
            adjusted_data[symbol]["total_dividends"] += dividend

    # Calculate adjusted buy-in price per share buy symbol
    result = {}
    for symbol, data in adjusted_data.items():
        if data["total_quantity"] > 0:
            adjusted_cost = (
                data["total_cost"]
                - data["net_option_premiums"]
                - data["total_dividends"]
            )
            avg_price = adjusted_cost / data["total_quantity"]
            result[symbol] = avg_price

    return result