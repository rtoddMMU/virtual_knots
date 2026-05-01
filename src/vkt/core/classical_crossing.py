# src/vkt/core/classical_crossing.py

from .crossing import Crossing
from typing import Any

__all__ = ["ClassicalCrossing"]


class ClassicalCrossing(Crossing):
    """Classical crossing with a sign (+1 or -1).
    
    A classical crossing has an over-strand and under-strand, with the sign
    indicating the handedness of the crossing:
    - sign = +1: positive (right-handed) crossing
      - over-strand: [west, east]
      - under-strand: [south, north]
    - sign = -1: negative (left-handed) crossing
      - over-strand: [south, north]
      - under-strand: [west, east]
    
    Attributes:
        sign (int): +1 for positive crossing, -1 for negative crossing
        south, north, west, east: Incident arcs in cardinal directions
        attr (dict): Additional attributes
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
            south: Arc entering from below
            north: Arc exiting to above
            west: Arc entering from left
            east: Arc exiting to right
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
    
    @property
    def over_strand(self) -> list[Any]:
        """Get the over-crossing arc based on sign.
        
        Returns:
            [west, east] if positive crossing
            [south, north] if negative crossing
        """
        if self._sign == 1:
            return [self.west, self.east]
        else:  # self._sign == -1
            return [self.south, self.north]
    
    @property
    def under_strand(self) -> list[Any]:
        """Get the under-crossing arc based on sign.
        
        Returns:
            [south, north] if positive crossing
            [west, east] if negative crossing
        """
        if self._sign == 1:
            return [self.south, self.north]
        else:  # self._sign == -1
            return [self.west, self.east]
    
    def flip_sign(self) -> None:
        """Flip the sign of the crossing (useful for Reidemeister moves).
        
        Note: This also swaps which arcs are over/under.
        """
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
        """String representation including sign. This tells you what happens when you call print()"""
        sign_str = "+" if self._sign == 1 else "-"
        arc_str = f"S:{self.south} N:{self.north} W:{self.west} E:{self.east}"
        attr_str = " ".join(f"{k}={v}" for k, v in self.attr.items())
        return f"ClassicalCrossing({sign_str}, {arc_str}){' ' + attr_str if attr_str else ''}"
    
    def __hash__(self) -> int:
        """Hash including sign. This allows you to put objects into sets and dictionaries"""
        return hash((type(self).__name__, self._sign, self.south, self.north, self.west, self.east))
    
    def __eq__(self, other: Any) -> bool:
        """Check equality including sign. This tells you what should happen when you ask a == b """
        if not isinstance(other, ClassicalCrossing):
            return False
        return (self._sign == other._sign and
                self.south == other.south and
                self.north == other.north and
                self.west == other.west and
                self.east == other.east)