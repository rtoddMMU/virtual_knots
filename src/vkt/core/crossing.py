# src/vkt/core/crossing.py

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple

__all__ = ["Crossing"]
__version__ = "0.2.0"
__author__ = "Robert Todd"


class Crossing(ABC):
    """Abstract base class for crossings in virtual knot diagrams.
    
    A crossing has 4 cardinal direction endpoints with directional constraints:
    - EXIT points (can have successors): north, east
    - ENTRY points (can have predecessors): south, west
    
    Each crossing is a vertex in the knot graph with a fixed cyclic order.
    Arcs connect exit points to entry points of other crossings.
    
    Attributes:
        south, north, west, east: Cardinal direction endpoints (for geometric info)
        north_successor: (crossing, direction) tuple - where north exits to
        east_successor: (crossing, direction) tuple - where east exits to
        south_predecessor: (crossing, direction) tuple - where south enters from
        west_predecessor: (crossing, direction) tuple - where west enters from
        id: Unique identifier for this crossing
        attr: Additional attributes dictionary
    """
    
    _id_counter = 0  # Class variable for unique IDs
    
    def __init__(
        self,
        south: Any = None,
        north: Any = None,
        west: Any = None,
        east: Any = None,
        **attr: Any
    ) -> None:
        """Initialize a crossing with four cardinal direction endpoints.
        
        Args:
            south, north, west, east: Cardinal endpoints (for geometric info)
            **attr: Additional attributes for the crossing
        """
        # Geometric endpoints (can store coordinates, etc.)
        self.south = south
        self.north = north
        self.west = west
        self.east = east
        
        # Topological connections (successors and predecessors)
        self.north_successor: Optional[Tuple[Crossing, str]] = None
        self.east_successor: Optional[Tuple[Crossing, str]] = None
        self.south_predecessor: Optional[Tuple[Crossing, str]] = None
        self.west_predecessor: Optional[Tuple[Crossing, str]] = None
        
        # Unique ID
        self.id = Crossing._id_counter
        Crossing._id_counter += 1
        
        # Additional attributes
        self.attr = dict(attr)
    
    def set_successor(self, my_direction: str, other_crossing: Crossing, other_direction: str) -> None:
        """Set where an exit direction leads to.
        
        Automatically sets the corresponding predecessor on the other crossing.
        
        Args:
            my_direction: Exit direction ('north' or 'east')
            other_crossing: Target crossing
            other_direction: Entry direction on target ('south' or 'west')
            
        Raises:
            ValueError: If directions are invalid
        """
        # Validate directions
        if my_direction not in ['north', 'east']:
            raise ValueError(f"Can only set successor for 'north' or 'east', not '{my_direction}'")
        if other_direction not in ['south', 'west']:
            raise ValueError(f"Successor must connect to 'south' or 'west', not '{other_direction}'")
        
        # Set successor
        setattr(self, f"{my_direction}_successor", (other_crossing, other_direction))
        
        # Automatically set the reverse predecessor
        setattr(other_crossing, f"{other_direction}_predecessor", (self, my_direction))
    
    def get_successor(self, direction: str) -> Optional[Tuple[Crossing, str]]:
        """Get successor for an exit direction.
        
        Args:
            direction: Exit direction ('north' or 'east')
            
        Returns:
            (crossing, direction) tuple or None
            
        Raises:
            ValueError: If direction is not an exit direction
        """
        if direction not in ['north', 'east']:
            raise ValueError(f"Only 'north' and 'east' have successors, not '{direction}'")
        return getattr(self, f"{direction}_successor")
    
    def get_predecessor(self, direction: str) -> Optional[Tuple[Crossing, str]]:
        """Get predecessor for an entry direction.
        
        Args:
            direction: Entry direction ('south' or 'west')
            
        Returns:
            (crossing, direction) tuple or None
            
        Raises:
            ValueError: If direction is not an entry direction
        """
        if direction not in ['south', 'west']:
            raise ValueError(f"Only 'south' and 'west' have predecessors, not '{direction}'")
        return getattr(self, f"{direction}_predecessor")
    
    def disconnect_successor(self, direction: str) -> None:
        """Remove a successor connection.
        
        Args:
            direction: Exit direction ('north' or 'east')
        """
        if direction not in ['north', 'east']:
            raise ValueError(f"Can only disconnect 'north' or 'east', not '{direction}'")
        
        # Get the current successor
        successor = getattr(self, f"{direction}_successor")
        
        if successor is not None:
            other_crossing, other_direction = successor
            # Remove the corresponding predecessor
            setattr(other_crossing, f"{other_direction}_predecessor", None)
        
        # Remove the successor
        setattr(self, f"{direction}_successor", None)
    
    def disconnect_predecessor(self, direction: str) -> None:
        """Remove a predecessor connection.
        
        Args:
            direction: Entry direction ('south' or 'west')
        """
        if direction not in ['south', 'west']:
            raise ValueError(f"Can only disconnect 'south' or 'west', not '{direction}'")
        
        # Get the current predecessor
        predecessor = getattr(self, f"{direction}_predecessor")
        
        if predecessor is not None:
            other_crossing, other_direction = predecessor
            # Remove the corresponding successor
            setattr(other_crossing, f"{other_direction}_successor", None)
        
        # Remove the predecessor
        setattr(self, f"{direction}_predecessor", None)
    
    @property
    def arcs(self) -> dict[str, Any]:
        """Return all geometric endpoints as a dictionary."""
        return {
            'south': self.south,
            'north': self.north,
            'west': self.west,
            'east': self.east
        }
    
    @property
    def connections(self) -> dict[str, Optional[Tuple[Crossing, str]]]:
        """Return all topological connections."""
        return {
            'north_successor': self.north_successor,
            'east_successor': self.east_successor,
            'south_predecessor': self.south_predecessor,
            'west_predecessor': self.west_predecessor
        }
    
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
        type_name = type(self).__name__
        return f"{type_name}(id={self.id})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        """Hash based on unique ID."""
        return hash((type(self).__name__, self.id))
    
    def __eq__(self, other: Any) -> bool:
        """Check equality based on ID."""
        if not isinstance(other, Crossing):
            return False
        return self.id == other.id