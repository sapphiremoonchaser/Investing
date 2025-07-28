# Imports
from typing import List, Dict, Union
import logging
from pydantic import BaseModel, Field

from trading_analytics.data.data_model.entry.dividend_entry import DividendEntry
from trading_analytics.data.data_model.entry.trade_entry import TradeEntry
from trading_analytics.data.data_model.entry.stock_entry import StockEntry
from trading_analytics.data.data_model.entry.option_entry import OptionEntry
from trading_analytics.data.enum.option_type import OptionType
from trading_analytics.data.enum.security_type import SecurityType
from trading_analytics.data.enum.sub_action import TradeSubAction
from trading_analytics.data.enum.trade_action import TradeAction

# Configure logging to a file
logger = logging.getLogger(__name__)

# Pydantic Models
class SymbolResult(BaseModel):
    profit: float = Field(default=0.0)
    stock_qty: float = Field(default=0.0)
    option_qty: float = Field(default=0.0)


class BuyInData(BaseModel):
    total_cost: float = Field(default=0.0)
    total_quantity: float = Field(default=0.0)
    net_option_premiums: float = Field(default=0.0)
    total_dividends: float = Field(default=0.0)


def _process_stock_etf_buy_trades(
        trades: List[TradeEntry],
        data_dict: dict
) -> None:
    """Helper function to process trades where SecurityType is STOCK or ETF and action is BUY.

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
            data_dict[symbol] = BuyInData()

        # Process STOCK or ETF trades with BUY action
        if (
            hasattr(trade, "security")
            and trade.security in [SecurityType.STOCK, SecurityType.ETF]
            and trade.action == TradeAction.BUY
            and isinstance(trade, StockEntry)
        ):
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

        # Calculate profit/loss based on security type
        stock_qty = 0.0
        option_qty = 0.0
        profit = 0.0

        # Stock or ETF
        if trade.security in [SecurityType.STOCK, SecurityType.ETF]:
            if trade.action == TradeAction.BUY:
                stock_qty = trade.quantity  # Positive for buying shares
                profit = -trade.quantity * getattr(trade, 'price_per_share', 0.0) - trade.fees  # Cash outflow
            elif trade.action == TradeAction.SELL:
                stock_qty = -trade.quantity  # Negative for selling shares
                profit = trade.quantity * getattr(trade, 'price_per_share', 0.0) - trade.fees  # Cash inflow
            else:
                logger.warning(f"Unexpected action {trade.action} for trade_id {trade.trade_id}")
                stock_qty = 0.0
                profit = 0.0

        # Dividend
        elif trade.security == SecurityType.DIVIDEND:
            profit = getattr(trade, 'dividend_amount', 0.0) - trade.fees
            stock_qty = 0.0

        # Options
        elif trade.security == SecurityType.OPTION:
            option_type = getattr(trade, 'option_type', None)
            if option_type == OptionType.CALL:
                if trade.action == TradeAction.SELL and trade.sub_action == TradeSubAction.OPEN:
                    option_qty = trade.quantity
                    profit = trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees
                elif trade.action == TradeAction.SELL and trade.sub_action == TradeSubAction.CLOSE:
                    option_qty = -trade.quantity
                    profit = trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees
                elif trade.action == TradeAction.BUY and trade.sub_action == TradeSubAction.OPEN:
                    option_qty = trade.quantity
                    profit = -trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees
                elif trade.action == TradeAction.BUY and trade.sub_action == TradeSubAction.CLOSE:
                    option_qty = -trade.quantity
                    profit = -trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees
                elif trade.action == TradeAction.OPTION_EXPIRED:
                    option_qty = -trade.quantity
                    profit = 0.0
                elif trade.action == TradeAction.OPTION_ASSIGNED:
                    stock_qty = -trade.quantity * 100
                    option_qty = -trade.quantity
                    profit = trade.quantity * getattr(trade, 'strike', 0.0) * 100 - trade.fees
                elif trade.action == TradeAction.OPTION_EXERCISED:
                    stock_qty = trade.quantity * 100
                    option_qty = -trade.quantity
                    profit = -trade.quantity * getattr(trade, 'strike', 0.0) * 100 - trade.fees
                else:
                    logger.warning(f"Unexpected action {trade.action} for trade_id {trade.trade_id}")
                    option_qty = 0.0
                    profit = 0.0
            elif option_type == OptionType.PUT:
                if trade.action == TradeAction.BUY and trade.sub_action == TradeSubAction.OPEN:
                    option_qty = trade.quantity
                    profit = -trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees
                elif trade.action == TradeAction.SELL and trade.sub_action == TradeSubAction.CLOSE:
                    option_qty = -trade.quantity
                    profit = trade.quantity * getattr(trade, 'premium', 0.0) * 100 - trade.fees
                elif trade.action == TradeAction.OPTION_EXPIRED:
                    option_qty = -trade.quantity
                    profit = 0.0
                elif trade.action == TradeAction.OPTION_ASSIGNED:
                    stock_qty = trade.quantity * 100
                    option_qty = -trade.quantity
                    profit = -trade.quantity * getattr(trade, 'strike', 0.0) * 100 - trade.fees
                else:
                    logger.warning(f"Unexpected action {trade.action} for trade_id {trade.trade_id}")
                    option_qty = 0.0
                    profit = 0.0
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


# def iterate_current_position_types(
#         current_positions: Union[list, dict, pd.DataFrame],
# ) -> None:
#     """Iterate through possible current position types to deal with enumerating current_positions.
#
#     Args:
#         current_positions (UNION[list, dict pd.DataFrame): List of trade entries to process.
#     """
#     if isinstance(current_positions, list):
#         iterable = enumerate(current_positions)
#     elif isinstance(current_positions, dict):
#         iterable = current_positions.items()
#     elif isinstance(current_positions, pd.DataFrame):
#         iterable = current_positions.iterrows()
#     else:
#         raise TypeError(f"Unexpected type {type(current_positions)}")
#
#     for row_idx, row_data in iterable:
#         if isinstance(current_positions, pd.DataFrame):
#             row_data = row_data[1]
#         yield row_idx, row_data


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
    _process_stock_etf_buy_trades(trades, buy_in_data)

    print(f"Buy-in data: {[(symbol, data.total_cost, data.total_quantity) for symbol, data in buy_in_data.items()]}")
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
    _process_stock_etf_buy_trades(trades, adjusted_data)

    for trade in trades:
        symbol = trade.symbol

        # Initialize dict for new symbols
        if symbol not in adjusted_data:
            adjusted_data[symbol] = BuyInData()

        try:
            # Option Trades (premiums)
            if isinstance(trade, OptionEntry):
                if trade.option_type in [OptionType.CALL, OptionType.PUT]:
                    if (
                        trade.action == TradeAction.SELL
                        and trade.sub_action in [TradeSubAction.OPEN, TradeSubAction.CLOSE]
                    ):
                        premium = trade.premium  * trade.quantity * 100 - trade.fees
                        adjusted_data[symbol].net_option_premiums += premium

                    elif (
                            trade.action == TradeAction.BUY
                        and trade.sub_action in [TradeSubAction.OPEN, TradeSubAction.CLOSE]
                    ):
                        premium = -trade.premium * trade.quantity * 100 - trade.fees
                        adjusted_data[symbol].net_option_premiums += premium

            # Dividend Trades
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