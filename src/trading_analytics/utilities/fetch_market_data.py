import yfinance as yf
from typing import (
    Dict,
    List
)

from trading_analytics.data.data_model.market.stock_data import CurrentStockData

def fetch_current_stock_price(
        symbol: str
) -> CurrentStockData:
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


def fetch_options_data(
        symbol: str
) -> List[Dict]:
    """Fetches options data for a given symbol.

    :param symbol: The stock symbol
    :return: List of dictionaries containing options data (strike, last price, expiration)
    """
    try:
        ticker = yf.Ticker(symbol.upper())
        # Get the first available expiration date
        expiration = ticker.options[0] if ticker.options else None
        if not expiration:
            raise ValueError(f"No options data available for {symbol}")
        # Fetch options chain for the first expiration
        options = ticker.option_chain(expiration)
        # Return calls data with relevant fields
        calls = options.calls[['strike', 'lastPrice', 'expiration']].to_dict('records')
        return [{'strike': c['strike'], 'lastPrice': c['lastPrice'], 'expiration': expiration} for c in calls]
    except Exception as e:
        raise ValueError(f"Failed to fetch options data for {symbol}: {str(e)}")