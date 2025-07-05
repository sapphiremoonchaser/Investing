# Imports
from enum import Enum

# Enum for valid trade actions
class TradeAction(str, Enum):
    """Enum class for valid trade actions.

    This class defines a set of valid trade actions as string enumerations.
    Each action represents a specific type of trading activity.

    Attributes:
        BOUGHT (str): Standard purchase of a security.
        BOUGHT_COVER (str): Purchase to cover a short position.
        BOUGHT_OPEN (str): Purchase to open a position, typically for options.
        DIVIDEND (str): Dividend payment received.
        OPTION_EXPIRED (str): Option contract expired.
        OPTION_ASSIGNED (str): Option contract assigned.
        OPTION_EXERCISED (str): Option contract exercised.
        SOLD (str): Standard sale of a security.
        SOLD_SHORT (str): Sale to open a short position.
        SOLD_CLOSE (str): Sale to close a position, typically for options.
    """
    BOUGHT = 'BOUGHT'
    BOUGHT_COVER = 'BOUGHT COVER'
    BOUGHT_OPEN = 'BOUGHT OPEN'
    DIVIDEND = 'DIVIDEND'
    OPTION_EXPIRED = 'OPTION EXPIRED'
    OPTION_ASSIGNED = 'OPTION ASSIGNED'
    OPTION_EXERCISED = 'OPTION EXERCISED'
    SOLD = 'SOLD'
    SOLD_SHORT = 'SOLD SHORT'
    SOLD_CLOSE = 'SOLD CLOSE'
    