# Imports
import logging

from trading_analytics.journal.core.calculate_profit import calculate_qty_and_profit, get_current_positions
from trading_analytics.utilities.csv.load_trades import load_trades_from_excel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('view_profit_by_symbol.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def _test(file_path: str = "C:/Users/viole/dev/Investing-data/trades/trades.xlsx"):
    """Loads trades from an Excel file and tests the get_current_assets function."""
    # Load trades from Excel
    try:
        trades = load_trades_from_excel(file_path)
        logger.info(f"Loaded {len(trades)} trades from {file_path}")
    except Exception as e:
        logger.error(f"Error loading trades: {e}")
        raise

    # Calculate quantities and profits
    try:
        results = calculate_qty_and_profit(trades)
        logger.info("Calculated quantities and profits")
    except Exception as e:
        logger.error(f"Error calculating quantities and profits: {e}")
        raise

    # Get non-zero positions
    try:
        positions = get_current_positions(results)
        logger.info("\n=== Non-Zero Positions ===")
        for symbol, data in positions.items():
            print(f"Symbol: {symbol}")
            print(f"  Profit: ${data.profit:.2f}")
            print(f"  Stock Quantity: {data.stock_qty}")
            print(f"  Option Quantity: {data.option_qty}")
            print()
    except Exception as e:
        logger.error(f"Error getting current assets: {e}")
        raise

    x = 1

if __name__ == '__main__':
    _test()