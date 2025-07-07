# Imports
from enum import Enum

# Enum for valid strategies
class TradeStrategy(str, Enum):
    """Enum class for valid trading strategies.

    This class defines a set of valid trading strategies as string enumerations.
    Each strategy represents a specific type of trading approach.

    Attributes:
        DIVIDEND (str): Dividend-based trading strategy.
        ETF (str): Exchange-traded fund trading strategy.
        BASIC_TRADE (str): Standard stock trading strategy.
        BASIC_OPTION (str): Basic options trading strategy.
        COVERED_CALL (str): Covered call options trading strategy.
        SPREAD (str): Spread-based options trading strategy.
    """
    DIVIDEND = 'DIVIDEND'
    ETF = 'ETF'
    BASIC_TRADE = 'BASIC TRADE'
    BASIC_OPTION = 'BASIC OPTION'
    COVERED_CALL = 'COVERED CALL'
    SPREAD = 'SPREAD'
