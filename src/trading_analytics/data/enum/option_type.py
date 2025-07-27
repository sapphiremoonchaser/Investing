# Imports
from enum import Enum

# Enum for valid option subtypes
class OptionType(str, Enum):
    """Enum class for valid option subtypes.

    This class defines a set of valid option subtypes as string enumerations.
    Each subtype represents a specific type of option contract.

    Attributes:
        CALL (str): Call option subtype.
        PUT (str): Put option subtype.
    """
    CALL = 'CALL'
    PUT = 'PUT'