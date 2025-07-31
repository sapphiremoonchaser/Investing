"""SecurityType enumeration for valid option subtypes.

This module defines the `SecurityType` enumeration, which specifies valid types for securities
using Python's `Enum` class. It ensures that only predefined option subtypes (STOCK, ETF, OPTION, DIVIDEND)
are used.

Classes:
    SecurityType: A string-based enumeration for security types (STOCK, ETF, OPTION, DIVIDEND).
"""
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
