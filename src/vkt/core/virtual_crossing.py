# src/vkt/core/virtual_crossing.py

from .crossing import Crossing
from typing import Any #for future additions and consistency.

__all__ = ["VirtualCrossing"]


class VirtualCrossing(Crossing):
    """Virtual crossing (no over/under information, no sign).
    
    A virtual crossing is a bookkeeping device in virtual knot theory
    that represents a crossing that is "not really there" in the classical sense.
    It has no sign and no over/under strand distinction.
    """
    
    def is_virtual(self) -> bool:
        """Return True (this is a virtual crossing)."""
        return True
    
    def is_classical(self) -> bool:
        """Return False (this is not a classical crossing)."""
        return False
    
    def __str__(self) -> str:
        """String representation."""
        arc_str = f"S:{self.south} N:{self.north} W:{self.west} E:{self.east}"
        attr_str = " ".join(f"{k}={v}" for k, v in self.attr.items())
        return f"VirtualCrossing({arc_str}){' ' + attr_str if attr_str else ''}"