# Imports
import pandas as pd

from utilities.csv.load_trades import load_trades_from_excel
from journal.core.calculate_profit import calculate_qty_and_profit

file_path = "C:/Users/viole/dev/Investing-data/trades/trades.xlsx"

# Load trades from excel
try:
    trades = load_trades_from_excel(file_path)
    print(f"Loaded {len(trades)} trade from {file_path}.")
except Exception as e:
    print(f"Error loading trades: {e}")
    exit(1)

# Calculate profit and quantities
results = calculate_qty_and_profit(trades)

# Save results to excel file for manual inspection
by_symbol_df = pd.DataFrame(results).from_dict(results['by_symbol'], orient='index')
save_to_file_path = "C:/Users/viole/dev/Investing-data/trades/profit_by_symbol.xlsx"
by_symbol_df.to_excel(save_to_file_path)
print(f"\nSaved results as {save_to_file_path}.")
