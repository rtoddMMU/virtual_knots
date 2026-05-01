# src/vkt/core/virtual_crossing.py

from .crossing import Crossing

__all__ = ["VirtualCrossing"]


class VirtualCrossing(Crossing):
    """Virtual crossing (no over/under information, no sign)."""
    
    def is_virtual(self) -> bool:
        """Return True (this is a virtual crossing)."""
        return True
    
    def is_classical(self) -> bool:
        """Return False (this is not a classical crossing)."""
        return False
    
    def __str__(self) -> str:
        """String representation."""
        return f"VirtualCrossing(id={self.id})"