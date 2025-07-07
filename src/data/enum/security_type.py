# Imports
from enum import Enum

# Enum for valid security types
# Enum is used to define a set of named constant values
# Advantages: readability, type safe, maintainable, iterability, immutable
class SecurityType(str, Enum):
    """An enumeration of valid trade types.

    Attributes:
        STOCK (str): Represents a stock trade.
        ETF (str): Represents an index trade.
        OPTION (str): Represents an option trade.
        DIVIDEND (str): Represents a dividend trade.
    """
    STOCK = 'STOCK'
    ETF = 'ETF'
    OPTION = 'OPTION'
    DIVIDEND = 'DIVIDEND'
