# Imports
import logging
import pandas as pd

from trading_analytics.utilities.csv import load_trades_from_excel
from trading_analytics.journal.core.calculate_profit import calculate_original_buy_in

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

    # Calculate profit and quantities
    results = calculate_original_buy_in(trades)
    logger.info(f"Results: {results}")

    if not results:
        logger.warning("No buy-in data to save; results dictionary is empty")
        return

    # Save results to excel file for manual inspection
    try:
        df = pd.DataFrame.from_dict(
            results,
            orient='index',
            columns=['avg_buy_in_price']
        )

        save_to_file_path = "C:/Users/viole/dev/Investing-data/trades/org_buy_in_by_symbol.xlsx"

        df.to_excel(
            save_to_file_path,
            index_label='symbol'
        )

        logger.info(f"Saved results to {save_to_file_path}")

    except Exception as e:
        logger.error(f"Error saving to Excel: {e}")
        raise

if __name__ == '__main__':
    _test()