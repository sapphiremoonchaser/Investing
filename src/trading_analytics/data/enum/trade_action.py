"""Action enumeration for valid option subtypes.

This module defines the `Action` enumeration, which specifies valid actions for trades
using Python's `Enum` class. It ensures that only predefined actions
(BUY, SELL, DIVIDEND, OPTION EXPIRED, OPTION EXERCISED, OPTION ASSIGNED)
are used.

Classes:
    SubAction: A string-based enumeration for trade sub actions (OPEN, CLOSE, DIVIDEND).
"""
from enum import Enum

# Enum for valid trade actions
class Action(str, Enum):
    """Enum class for valid trade actions.

    This class defines a set of valid trade actions as string enumerations.
    Each action represents a specific type of trading activity.

    Attributes:
        BUY (str): Standard purchase of a security.
        DIVIDEND (str): Dividend payment received.
        OPTION_EXPIRED (str): Option contract expired.
        OPTION_ASSIGNED (str): Option contract assigned.
        OPTION_EXERCISED (str): Option contract exercised.
        SELL (str): Standard sale of a security.
    """
    BUY = 'BUY'
    DIVIDEND = 'DIVIDEND'
    OPTION_EXPIRED = 'OPTION EXPIRED'
    OPTION_ASSIGNED = 'OPTION ASSIGNED'
    OPTION_EXERCISED = 'OPTION EXERCISED'
    SELL = 'SELL'
    