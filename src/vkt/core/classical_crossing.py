# src/vkt/core/classical_crossing.py

from .crossing import Crossing
from typing import Any

__all__ = ["ClassicalCrossing"]


class ClassicalCrossing(Crossing):
    """Classical crossing with a sign (+1 or -1).
    
    Attributes:
        sign: +1 for positive crossing, -1 for negative crossing
    """
    
    def __init__(
        self,
        sign: int,
        south: Any = None,
        north: Any = None,
        west: Any = None,
        east: Any = None,
        **attr: Any
    ) -> None:
        """Initialize a classical crossing with a sign.
        
        Args:
            sign: Must be +1 (positive) or -1 (negative)
            south, north, west, east: Cardinal endpoints
            **attr: Additional attributes
            
        Raises:
            ValueError: If sign is not +1 or -1
        """
        if sign not in (1, -1):
            raise ValueError(f"Classical crossing sign must be +1 or -1, got {sign}")
        
        super().__init__(south=south, north=north, west=west, east=east, **attr)
        self._sign = sign
    
    @property
    def sign(self) -> int:
        """Get the sign of the crossing."""
        return self._sign
    
    @sign.setter
    def sign(self, value: int) -> None:
        """Set the sign of the crossing.
        
        Args:
            value: Must be +1 or -1
            
        Raises:
            ValueError: If value is not +1 or -1
        """
        if value not in (1, -1):
            raise ValueError(f"Classical crossing sign must be +1 or -1, got {value}")
        self._sign = value
    
    def flip_sign(self) -> None:
        """Flip the sign of the crossing (useful for Reidemeister moves)."""
        self._sign *= -1
    
    def is_positive(self) -> bool:
        """Return True if this is a positive crossing."""
        return self._sign == 1
    
    def is_negative(self) -> bool:
        """Return True if this is a negative crossing."""
        return self._sign == -1
    
    def is_virtual(self) -> bool:
        """Return False (this is a classical crossing)."""
        return False
    
    def is_classical(self) -> bool:
        """Return True (this is a classical crossing)."""
        return True
    
    def __str__(self) -> str:
        """String representation including sign."""
        sign_str = "+" if self._sign == 1 else "-"
        return f"ClassicalCrossing(id={self.id}, sign={sign_str})"