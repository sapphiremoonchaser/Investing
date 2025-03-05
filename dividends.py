import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

# Open csv with tickers and put all tickers into a list
# list from Kaggle updated daily
# ToDo: Automate downloading list

# Open file and save as dataframe
filepath = 'C:/dev/Investing/sp500_companies.csv'
tickers = pd.read_csv(filepath)

# Add all tickers to a list
sp500_tickers = []
for i in tickers['Symbol']:
    i = i.lower()
    sp500_tickers.append(i)

# Get ex dividend date
# Investors only get dividends if stock is purchased before ex-dividend date
dividend_stocks = {}

# Get ticker
for ticker in sp500_tickers:
    stock = yf.Ticker(ticker)

    # Get info from ticker if dividend is not empty
    if not stock.dividends.empty:
        info = stock.info

        # Get ex dividend date and make sure it's in the future
        ex_dividend_date = info.get('exDividendDate')
        if ex_dividend_date:
            # Convert to datetime
            ex_dividend_date = datetime.utcfromtimestamp(ex_dividend_date)

            # Check that ex dividend date is in the future
            if ex_dividend_date > datetime.utcnow():
                # Default to 0
                dividend_yield = info.get('dividendYield', 0)

                # Store in dictionary
                dividend_stocks[ticker] = {
                    "Ex Dividend Date": ex_dividend_date.strftime("%Y-%m-%d"),
                    "Dividend Yield": dividend_yield
                }




