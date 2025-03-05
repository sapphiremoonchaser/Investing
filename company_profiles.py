# Imports
import yfinance as yf
import datetime

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

    return print(basic_info)


def get_company_age(year_founded):
    company_age = datetime.datetime.now().year - year_founded
    return print(f"{company_age} Years")


def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    market_cap = stock.info['marketCap']
    return print(f"Market Cap: ${'{:.2f}'.format(market_cap / 1000000000)}B"), market_cap


def get_ev(ticker):
    stock = yf.Ticker(ticker)
    ev = stock.info['enterpriseValue']
    return print(f"Enterprise Value: ${'{:.2f}'.format(ev / 1000000000)}B"), ev


def get_pe(ticker):
    stock = yf.Ticker(ticker)
    trailing = stock.info['trailingEps']
    forward = stock.info['forwardEps']

    pe = f"""
    Trailing P/E: {trailing}
    Forward P/E: {forward}
    """

    return print(pe), trailing
    

def get_book_value(ticker):
    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet

    market_cap = get_market_cap(ticker)[1]

    # Find Total Current Assets
    total_assets = None
    possible_keys = [
        'Total Current Assets',
        'Total Assets'
    ]
    for key in possible_keys:
        if key in balance_sheet.index:
            total_assets = balance_sheet.loc[key]
            total_assets = total_assets.iloc[0]
            break

    # Find Total Current Liabilities
    total_liabilities = None
    possible_keys = [
        'Total Current Liabilities',
        'Total Liabilities',
        'Current Liabilities'
    ]
    for key in possible_keys:
        if key in balance_sheet.index:
            total_liabilities = balance_sheet.loc[key]
            total_liabilities = total_liabilities.iloc[0] # most recent
            break
    
    book_value = total_assets - total_liabilities
    market_to_book = market_cap / book_value

    book_value_statement = f"""
    Book Value: ${book_value / 1000000000}B
    Market/Book: {'{:.2f}'.format(market_to_book)}
    """

    return print(book_value_statement), book_value

