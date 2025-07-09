import yfinance as yf
import logging
from typing import Dict, List, Optional

from data.data_model.market.stock_data import CurrentStockData

def fetch_current_stock_price(symbol: str) -> CurrentStockData:
    """Fetches the current stock price for a given symbol.

    :param symbol: The stock symbol
    :return: CurrentStockData object with symbol and current price
    """
    try:
        # Create a Ticker object for the symbol passed in
        ticker = yf.Ticker(symbol.upper())

        # Fetch the current price (using regularMarketPrice)
        price_data = ticker.info
        current_price = price_data.get('regularMarketPreviousClose')

        if current_price is None:
            raise ValueError(f"No current price data available for {symbol}")

        return CurrentStockData(
            symbol=symbol.upper(),
            current_price=float(current_price)
        )

    except Exception as e:
        raise ValueError(f"Failed to fetch current price for stock '{symbol}': {str(e)}")