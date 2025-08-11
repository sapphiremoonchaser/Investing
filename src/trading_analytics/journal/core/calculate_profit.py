"""Utilities for calculating trading profits and positions.

This module provides functions to get current positions and basic information about them
such as profit, quantity, original buy-in, and adjusted buy-in. It has a helper function
that processes stock or etf security types where the action is 'buy' to update total_cost
and total_quantity.

Functions:
    _process_stock_etf_buy_trades: initializes and updates values for BuyInData (cost and quantity)
    calculate_qty_and_profit: calculate profit, stock quantity, and option quantity
    get_current_positions: returns a dict with securities and quantities if stock or option quantity != 0
    calculate_original_buy_in: calculates buy-in based only on total cost and total quantity
    calculate_adjusted_buy_in: calculates buy-in with option premiums and dividends factored in
"""
from typing import (
    List,
    Dict,
    Union,
)
import logging

from trading_analytics.data.data_model.entry.dividend_entry import DividendEntry
from trading_analytics.data.data_model.entry.trade_entry import TradeEntry
from trading_analytics.data.data_model.entry.stock_entry import StockEntry
from trading_analytics.data.data_model.entry.option_entry import OptionEntry
from trading_analytics.data.enum.option_type import OptionType
from trading_analytics.data.enum.security_type import SecurityType
from trading_analytics.data.enum.sub_action import SubAction
from trading_analytics.data.enum.trade_action import Action
from trading_analytics.data.portfolio.buy_in_data import BuyInData
from trading_analytics.data.portfolio.symbol_result import SymbolResult

# Configure logging to a file
logger = logging.getLogger(__name__)

def _process_stock_etf_buy_trades(
    trades: List[TradeEntry],
    data_dict: dict
) -> None:
    """Helper function to process trades where SecurityType is STOCK or ETF
        and action is BUY. If all of that is true update cost and quantity.

    Args:
        trades (List[TradeEntry]): List of trade entries to process.
        data_dict (dict): Dictionary to store total_cost and total_quantity by symbol.

    Modifies:
        data_dict: Updates with total_cost and total_quantity for STOCK/ETF buy trades.
    """
    for trade in trades:
        symbol = trade.symbol

        # Initialize dict for new symbol is not already there
        if symbol not in data_dict:
            data_dict[symbol] = BuyInData() # Class with variables need for calculating original or adjusted buy-in

        # If bought stock/etf update cost and quantity
        if trade.is_bought_stock_etf:
            total_cost = trade.price_per_share * trade.quantity + trade.fees
            data_dict[symbol].total_cost += total_cost
            data_dict[symbol].total_quantity += trade.quantity


def calculate_qty_and_profit(
    trades: List[Union[StockEntry, DividendEntry, OptionEntry]],
) -> Dict[str, SymbolResult]:
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
    results: Dict[str, SymbolResult] = {}

    # Iterate through each trade to calculate and aggregate profit/loss
    trade: Union[StockEntry, DividendEntry, OptionEntry]
    for trade in trades:
        symbol = trade.symbol

        # Initialize dict for new symbol
        if symbol not in results.keys():
            results[symbol] = SymbolResult()

        # Initialize quantities and profit
        stock_qty = 0.0
        option_qty = 0.0
        profit = 0.0

        # Assign quantities and profit for stock/etf
        # Bought stock/etf
        if trade.is_bought_stock_etf:
            stock_qty = trade.quantity  # Positive for buying shares
            profit = -trade.quantity * getattr(trade, 'price_per_share', 0.0) - trade.fees  # Cash outflow

        # Sold stock/etf
        elif trade.is_stock_etf:
            stock_qty = -trade.quantity  # Negative for selling shares
            profit = trade.quantity * getattr(trade, 'price_per_share', 0.0) - trade.fees  # Cash inflow

        # Stock/ETF trade should only be bought or sold
        else:
            logger.warning(f"Unexpected action {trade.action} for trade_id {trade.trade_id}")
            stock_qty = 0.0
            profit = 0.0

        # Assign profit for Dividends
        if trade.security == SecurityType.DIVIDEND:
            profit = getattr(trade, 'dividend_amount', 0.0) - trade.fees
            stock_qty = 0.0

        # Assign quantity and profit for Options
        elif trade.security == SecurityType.OPTION:
            # Get option type (call or put)
            option_type = getattr(trade, 'option_type', None)

            # Assign quantity and profit for Calls
            if option_type == OptionType.CALL:
                # Calls sold open
                if trade.action == Action.SELL and trade.sub_action == SubAction.OPEN:
                    option_qty = trade.quantity
                    profit = trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees

                # Calls sold close
                elif trade.action == Action.SELL and trade.sub_action == SubAction.CLOSE:
                    option_qty = -trade.quantity
                    profit = trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees

                # Calls bought open
                elif trade.action == Action.BUY and trade.sub_action == SubAction.OPEN:
                    option_qty = trade.quantity
                    profit = -trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees

                # Calls bought close
                elif trade.action == Action.BUY and trade.sub_action == SubAction.CLOSE:
                    option_qty = -trade.quantity
                    profit = -trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees

                # Calls expired
                elif trade.action == Action.OPTION_EXPIRED:
                    option_qty = -trade.quantity
                    profit = 0.0

                # Calls assigned
                elif trade.action == Action.OPTION_ASSIGNED:
                    stock_qty = -trade.quantity * 100
                    option_qty = -trade.quantity
                    profit = trade.quantity * getattr(trade, 'strike', 0.0) * 100 - trade.fees

                # Calls exercised
                elif trade.action == Action.OPTION_EXERCISED:
                    stock_qty = trade.quantity * 100
                    option_qty = -trade.quantity
                    profit = -trade.quantity * getattr(trade, 'strike', 0.0) * 100 - trade.fees

                # Wrong action for calls
                else:
                    logger.warning(f"Unexpected action {trade.action} for trade_id {trade.trade_id}")
                    option_qty = 0.0
                    profit = 0.0

            # Assign quantity and profit for Puts
            elif option_type == OptionType.PUT:
                # Puts bought open
                if trade.action == Action.BUY and trade.sub_action == SubAction.OPEN:
                    option_qty = trade.quantity
                    profit = -trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees

                # Puts sold close
                elif trade.action == Action.SELL and trade.sub_action == SubAction.CLOSE:
                    option_qty = -trade.quantity
                    profit = trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees

                # Puts expired
                elif trade.action == Action.OPTION_EXPIRED:
                    option_qty = -trade.quantity
                    profit = 0.0

                # Puts assigned
                elif trade.action == Action.OPTION_ASSIGNED:
                    stock_qty = trade.quantity * 100
                    option_qty = -trade.quantity
                    profit = -trade.quantity * getattr(trade, 'strike', 0.0) * 100 - trade.fees

                # Invalid action for puts
                else:
                    logger.warning(f"Unexpected action {trade.action} for trade_id {trade.trade_id}")
                    option_qty = 0.0
                    profit = 0.0

        # Unexpected security type
        else:
            logger.warning(f"Unexpected security type {trade.security} for trade_id {trade.trade_id}")
            stock_qty = 0.0
            option_qty = 0.0
            profit = 0.0

        # Aggregate profit, stock_qty, and option_qty for symbol
        results[symbol].profit += profit
        results[symbol].stock_qty += stock_qty
        results[symbol].option_qty += option_qty

    return results


def get_current_positions(
    results: dict
) -> dict:
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
        if data.stock_qty != 0 or data.option_qty != 0
    }

    return active_positions


def calculate_original_buy_in(
    trades: List[TradeEntry]
) -> dict:
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
    buy_in_data: Dict[str, BuyInData] = {}

    # Stock/ETF trades bought
    _process_stock_etf_buy_trades(trades, buy_in_data)

    # print(f"Buy-in data: {[(symbol, data.total_cost, data.total_quantity) for symbol, data in buy_in_data.items()]}")

    # Calculate average buy-in price per share by symbol
    result = {}
    for symbol, data in buy_in_data.items():
        if data.total_quantity > 0:
            result[symbol] = data.total_cost / data.total_quantity
        else:
            logger.warning(f"No valid buy quantity {data.total_quantity} for {symbol}")

    return result


def calculate_adjusted_buy_in(
    trades: List[TradeEntry]
) -> dict:
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
    adjusted_data: Dict[str, BuyInData] = {}

    # Stock/ETF trade that were bought
    _process_stock_etf_buy_trades(trades, adjusted_data)

    # Add/subtract premiums and dividends
    for trade in trades:
        symbol = trade.symbol

        # Initialize dict for new symbols
        if symbol not in adjusted_data:
            adjusted_data[symbol] = BuyInData()

        try:
            # Option Trades (premiums)
            if isinstance(trade, OptionEntry):
                if trade.option_type in [OptionType.CALL, OptionType.PUT]:

                    # Sold option, add premium
                    if (
                        trade.action == Action.SELL
                        and trade.sub_action in [SubAction.OPEN, SubAction.CLOSE]
                    ):
                        premium = trade.premium  * trade.quantity * 100 - trade.fees
                        adjusted_data[symbol].net_option_premiums += premium

                    # Bought option, subtract premium
                    elif (
                            trade.action == Action.BUY
                            and trade.sub_action in [SubAction.OPEN, SubAction.CLOSE]
                    ):
                        premium = -trade.premium * trade.quantity * 100 - trade.fees
                        adjusted_data[symbol].net_option_premiums += premium

            # Dividend Trades, add dividend
            elif isinstance(trade, DividendEntry):
                dividend = trade.dividend_amount - trade.fees
                adjusted_data[symbol].total_dividends += dividend

        except ValueError as e:
            logger.error(f"Validation error for trade_id {trade.trade_id}: {e}")

    # Calculate adjusted buy-in price per share buy symbol
    result = {}
    for symbol, data in adjusted_data.items():
        if data.total_quantity > 0:
            adjusted_cost = (
                data.total_cost
                - data.net_option_premiums
                - data.total_dividends
            )
            result[symbol] = adjusted_cost / data.total_quantity

    return result
