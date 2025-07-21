# Imports
from typing import List
import pandas as pd
from src.data.data_model.entry.trade_entry import TradeEntry
from src.utilities.csv.load_trades import load_trades_from_excel
from src.utilities.fetch_market_data import fetch_current_stock_price
from src.journal.core.calculate_profit import (
    get_current_positions,
    calculate_qty_and_profit,
    calculate_adjusted_buy_in,
    calculate_original_buy_in,
    iterate_current_position_types
)
from src.data.data_model.market.stock_data import CurrentStockData
from src.data.data_model.portfolio.position import Position

def load_and_process_portfolio_data(file_path: str) -> List[Position]:
    """Load trades and return processed positions."""
    try:
        # Load raw trades from Excel
        raw_trades = load_trades_from_excel(file_path)
        print(f"Loaded {len(raw_trades)} raw trades from {file_path}")

        # Validate and convert raw trades to TradeEntry objects
        trades = [TradeEntry(**trade) for trade in raw_trades]
        print(f"Validated {len(trades)} trades")

        # Calculate quantities and profits
        quantity_dict = calculate_qty_and_profit(trades)
        print("Calculated quantities and profits")

        # Get current positions
        current_positions = get_current_positions(quantity_dict)
        if not current_positions or (isinstance(current_positions, (pd.DataFrame, pd.Series)) and current_positions.empty):
            return []

        # Process each position
        positions = []
        current_symbols = list(current_positions.keys())
        current_trades = [trade for trade in trades if trade.symbol in current_symbols]

        for symbol, stock_data in iterate_current_position_types(current_positions):
            current_price = None
            if symbol != 'N/A' and isinstance(symbol, str):
                current_stock_data = fetch_current_stock_price(symbol)
                current_price = current_stock_data.current_price if current_stock_data else None

            original_buy_in_dict = calculate_original_buy_in(current_trades)
            adjusted_buy_in_dict = calculate_adjusted_buy_in(current_trades)
            original_buy_in = original_buy_in_dict.get(symbol)
            adjusted_buy_in = adjusted_buy_in_dict.get(symbol)

            profit = (current_price - adjusted_buy_in) * stock_data.stock_qty if current_price and adjusted_buy_in else 0.0

            position = Position(
                brokerage=stock_data.brokerage,
                account=stock_data.account,
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

    except FileNotFoundError:
        print(f"Excel file {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error processing portfolio data: {e}")
        return []
