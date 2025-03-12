import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define GICS sector ETFs and their corresponding names
sector_etfs = {
    "XLK": "Information Technology",
    "XLV": "Healthcare",
    "XLF": "Financials",
    "XLY": "Consumer Discretionary",
    "XLP": "Consumer Staples",
    "XLI": "Industrials",
    "XLE": "Energy",
    "XLU": "Utilities",
    "XLRE": "Real Estate",
    "XLB": "Materials",
    "XLC": "Communication Services"
}

# Set date range
end_date = datetime.today().date() # Today’s date
start_date = end_date - timedelta(days=30)  # Approx 1 month ago


# Function to fetch and calculate performance
def get_sector_performance(ticker, start, end):
    try:
        # Download historical data
        stock = yf.Ticker(ticker)
        data = stock.history(start=start, end=end)

        # Get adjusted close prices
        if not data.empty and 'Close' in data.columns:
            start_price = data['Close'].iloc[0]  # First price in period
            end_price = data['Close'].iloc[-1]  # Last price in period
            performance = ((end_price - start_price) / start_price) * 100
            return round(performance, 2)  # Return as percentage, rounded to 2 decimals
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


# Fetch and display performance for each sector
print(f"GICS Sector Performance ({start_date} - {end_date}):")
print("-" * 50)
results = {}

for ticker, sector_name in sector_etfs.items():
    perf = get_sector_performance(ticker, start_date, end_date)
    if perf is not None:
        results[sector_name] = perf
        print(f"{sector_name}: {perf}%")
    else:
        print(f"{sector_name}: Data unavailable")

# Optional: Sort and display top/bottom performers
if results:
    print("\nTop Performers:")
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    for sector, perf in sorted_results[:3]:
        print(f"{sector}: {perf}%")

    print("\nBottom Performers:")
    for sector, perf in sorted_results[-3:]:
        print(f"{sector}: {perf}%")