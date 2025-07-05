# Imports
from enum import Enum

# Enum for brokerage
class Brokerage(str, Enum):
    """Enum class for valid brokerage names.

        This class defines a set of valid brokerage names as string enumerations.
        Each value represents a specific brokerage platform.

        Attributes:
            ETRADE (str): E*TRADE brokerage platform.
        """
    ETRADE = 'ETRADE'
