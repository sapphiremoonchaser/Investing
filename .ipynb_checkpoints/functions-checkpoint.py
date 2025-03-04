# Imports
import yfinance as yf


def get_basic_info(ticker):
    stock = yf.Ticker(ticker)
    short_name = stock.info['shortName']
    sector = stock.info['sector']
    industry = stock.info['industry']
    price = stock.info['currentPrice']
    volume = stock.info['volume']
    next_earnings = stock.calendar['Earnings Date'][0]

    basic_info = f"""
    Name: {short_name}
    Sector: {sector}
    Industry: {industry}

    Price: ${price}
    Volume: {'{:,}'.format(volume)}

    Next Earnings: {next_earnings}
    """

    return basic_info