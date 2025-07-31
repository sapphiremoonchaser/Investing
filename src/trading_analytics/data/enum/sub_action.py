"""SubAction enumeration for valid option subtypes.

This module defines the `SubAction` enumeration, which specifies valid open/close actions for trades
using Python's `Enum` class. It ensures that only predefined sub-actions (OPEN, CLOSE, DIVIDEND)
are used.

Classes:
    SubAction: A string-based enumeration for trade sub actions (OPEN, CLOSE, DIVIDEND).
"""
from enum import Enum

# Enum for valid trade actions
class SubAction(str, Enum):
    """Enum class for valid trade sub actions.

    This class defines a set of valid trade sub actions (opening and closing positions) as string enumerations.
    Each action represents a specific type of trading activity.

    Attributes:
        OPEN (str): Position is opened.
        CLOSE (str): Position is closed.
        DIVIDEND (str): Position is divided.
    """
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    DIVIDEND = 'DIVIDEND'
