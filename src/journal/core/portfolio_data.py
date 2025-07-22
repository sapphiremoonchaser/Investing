# Imports
import logging
from typing import List, Dict, Union
import pandas as pd

from data.data_model.entry.dividend_entry import DividendEntry
from data.data_model.entry.option_entry import OptionEntry
from data.data_model.entry.stock_entry import StockEntry
from data.enum.security_type import SecurityType
from journal.core.calculate_profit import SymbolResult
from src.data.data_model.entry.trade_entry import TradeEntry
from src.utilities.csv.load_trades import load_trades_from_excel
from src.utilities.fetch_market_data import fetch_current_stock_price
from src.journal.core.calculate_profit import (
    get_current_positions,
    calculate_qty_and_profit,
    calculate_adjusted_buy_in,
    calculate_original_buy_in
)
from src.data.data_model.market.stock_data import CurrentStockData
from src.data.data_model.portfolio.position import Position

logger = logging.getLogger(__name__)

def load_and_process_portfolio_data(
        file_path: str
) -> List[Position]:
    """Load trades and return processed positions."""
    try:
        # Load raw trades from Excel
        # Note: StockEntry, DividendEntry, OptionEntry all have the parent class TradeEntry.
        raw_trades: List[Union[StockEntry, DividendEntry, OptionEntry]] = load_trades_from_excel(file_path)
        print(f"Loaded {len(raw_trades)} raw trades from {file_path}")

        # Validate and convert raw trades to TradeEntry objects.
        # Note: Converting from the different sub-children types to the TradeEntry type.
        # Note: Not sure you need to do this, but leave for now.
        # trades: List[TradeEntry] = [TradeEntry(**trade.__dict__) for trade in raw_trades]
        # print(f"Validated {len(trades)} trades")

        # Calculate quantities and profits.
        quantity_dict: Dict[str, SymbolResult] = calculate_qty_and_profit(raw_trades)
        print("Calculated quantities and profits")

        # # list with current assets
        # current_asset_list = [key for key, value in quantity_dict.items() if value.stock_qty != 0 or value.option_qty != 0]

        # Get current positions.
        # Note: It filters down the quantity_dict to only symbols
        # that have non-zero stock or option quantity.
        current_positions: Dict[str, SymbolResult] = get_current_positions(quantity_dict)
        # if (
        #     not current_positions or
        #     (isinstance(current_positions, (pd.DataFrame, pd.Series))
        #     and current_positions.empty)
        # ):
        #     return []
        # if not  current_positions:
        #     print(f"No current positions found for {file_path}")
        #     return []

        # Process each position
        positions = []
        current_symbols: List[str] = list(current_positions.keys())
        current_trades = [trade for trade in raw_trades if trade.symbol in current_symbols]

        # Variables involving current data
        symbol: str
        stock_data: SymbolResult
        for symbol, stock_data in current_positions.items():
            # Fetch the current stock price
            current_price = None
            if symbol != 'N/A' and isinstance(symbol, str):
                current_stock_data = fetch_current_stock_price(symbol)
                current_price = current_stock_data.current_price if current_stock_data else None

            original_buy_in_dict = calculate_original_buy_in(current_trades)
            adjusted_buy_in_dict = calculate_adjusted_buy_in(current_trades)
            original_buy_in = original_buy_in_dict.get(symbol)
            adjusted_buy_in = adjusted_buy_in_dict.get(symbol)

            profit = (current_price - adjusted_buy_in) * stock_data.stock_qty if current_price and adjusted_buy_in else 0.0

            # Note: I don't think you need brokerage or account, because your aggregation by symbol across
            # all brokerages and accounts. You lose traceability because of this, so, no need for this info.
            position = Position(
                symbol=symbol,
                current_price=current_price,
                original_buy_in=original_buy_in,
                adjusted_buy_in=adjusted_buy_in,
                stock_qty=stock_data.stock_qty,
                option_qty=stock_data.option_qty,
                profit=profit
            )
            positions.append(position)

        return positions

    except Exception as e:
        print(f"Error processing portfolio data: {e}")
        return []
