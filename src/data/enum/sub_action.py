# Imports
from enum import Enum

# Enum for valid trade actions
class TradeSubAction(str, Enum):
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
