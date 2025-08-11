"""OptionType enumeration for valid option subtypes.

This module defines the `OptionType` enumeration, which specifies valid subtypes for option contracts
using Python's `Enum` class. It ensures that only predefined option subtypes (CALL and PUT) are used
in trading-related applications.

Classes:
    OptionType: A string-based enumeration for option contract subtypes (CALL, PUT).
"""
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