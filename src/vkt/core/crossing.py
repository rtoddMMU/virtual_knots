# src/vkt/core/crossing.py

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Literal

__all__ = ["Crossing"]
__version__ = "0.1.0"
__author__ = "Robert Todd"


class Crossing(ABC):
    """Abstract base class for crossings in virtual knot diagrams.
    
    A crossing is represented as a vertex with four incident arcs in cardinal directions:
    - south: incoming arc from below
    - north: outgoing arc to above
    - west: incoming arc from left
    - east: outgoing arc to right
    
    The crossing can be smoothed in two ways:
    - Oriented smoothing (A-smoothing): [[south, east], [west, north]]
    - Disoriented smoothing (B-smoothing): [[south, west], [east, north]]
    
    Attributes:
        south (Any): Arc entering from below
        north (Any): Arc exiting to above
        west (Any): Arc entering from left
        east (Any): Arc exiting to right
        attr (dict[str, Any]): Additional attributes (e.g., label, color)
    """
    
    def __init__(
        self,
        south: Any = None,
        north: Any = None,
        west: Any = None,
        east: Any = None,
        **attr: Any
    ) -> None:
        """Initialize a crossing with four cardinal direction arcs.
        
        Args:
            south: Arc entering from below
            north: Arc exiting to above
            west: Arc entering from left
            east: Arc exiting to right
            **attr: Additional attributes for the crossing
        """
        self.south = south
        self.north = north
        self.west = west
        self.east = east
        self.attr = dict(attr)
    
    @property
    def arcs(self) -> dict[str, Any]:
        """Return all arcs as a dictionary."""
        return {
            'south': self.south,
            'north': self.north,
            'west': self.west,
            'east': self.east
        }
    
    def oriented_smoothing(self) -> list[list[Any]]:
        """Perform oriented smoothing (A-smoothing).
        
        Connects arcs that preserve orientation:
        - South connects to East
        - West connects to North
        
        Returns:
            List of two arc pairs: [[south, east], [west, north]]
        """
        return [[self.south, self.east], [self.west, self.north]]
    
    def disoriented_smoothing(self) -> list[list[Any]]:
        """Perform disoriented smoothing (B-smoothing).
        
        Connects arcs that reverse orientation:
        - South connects to West
        - East connects to North
        
        Returns:
            List of two arc pairs: [[south, west], [east, north]]
        """
        return [[self.south, self.west], [self.east, self.north]]
    
    @abstractmethod
    def is_virtual(self) -> bool:
        """Return True if this is a virtual crossing."""
        pass
    
    @abstractmethod
    def is_classical(self) -> bool:
        """Return True if this is a classical crossing."""
        pass
    
    def __str__(self) -> str:
        """String representation of the crossing."""
        arc_str = f"S:{self.south} N:{self.north} W:{self.west} E:{self.east}"
        attr_str = " ".join(f"{k}={v}" for k, v in self.attr.items())
        type_name = type(self).__name__
        return f"{type_name}({arc_str}){' ' + attr_str if attr_str else ''}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        """Hash based on type and arcs."""
        return hash((type(self).__name__, self.south, self.north, self.west, self.east))
    
    def __eq__(self, other: Any) -> bool:
        """Check equality based on type and arcs."""
        if not isinstance(other, Crossing):
            return False
        return (type(self) == type(other) and 
                self.south == other.south and
                self.north == other.north and
                self.west == other.west and
                self.east == other.east)