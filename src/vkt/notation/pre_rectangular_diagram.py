# src/vkt/notation/pre_rectangular_diagram.py

from typing import List, Dict, Any
from ..core import ClassicalCrossing
from .arc import Arc
from .routing import create_arc_with_routing

__all__ = ["PreRectangularDiagram"]


class PreRectangularDiagram:
    """A rectangular diagram before virtual crossings are discovered.
    
    Contains:
    - Classical crossings positioned at (4n, 4n)
    - Routed arcs connecting the crossings
    - Segments within each arc (for line sweep algorithm)
    
    Attributes:
        classical_crossings: List of ClassicalCrossing objects
        arcs: List of Arc objects with routed segments
        num_crossings: Number of classical crossings
    """
    
    def __init__(self):
        """Initialize an empty pre-rectangular diagram."""
        self.classical_crossings: List[ClassicalCrossing] = []
        self.arcs: List[Arc] = []
        self.num_crossings: int = 0
    
    def add_crossing(self, sign: int, **attr) -> int:
        """Add a classical crossing to the diagram.
        
        The crossing is positioned at (4n, 4n) where n is its index.
        
        Args:
            sign: +1 or -1 for positive/negative crossing
            **attr: Additional attributes for the crossing
        
        Returns:
            Index of the newly added crossing
        """
        idx = self.num_crossings
        
        # Position at (4n, 4n)
        center_x = 4 * idx
        center_y = 4 * idx
        
        # Create crossing with cardinal points
        crossing = ClassicalCrossing(
            sign=sign,
            south=None,  # Will be connected by arcs
            north=None,
            west=None,
            east=None,
            index=idx,
            center=(center_x, center_y),
            **attr
        )
        
        self.classical_crossings.append(crossing)
        self.num_crossings += 1
        
        return idx
    
    def add_arc(
        self,
        start_idx: int,
        end_idx: int,
        start_dir: str,
        end_dir: str
    ) -> Arc:
        """Add a routed arc between two crossings.
        
        Args:
            start_idx: Index of starting crossing
            end_idx: Index of ending crossing
            start_dir: Direction leaving start ('north', 'south', 'east', 'west')
            end_dir: Direction entering end ('north', 'south', 'east', 'west')
        
        Returns:
            The created Arc object
        """
        arc = create_arc_with_routing(start_idx, end_idx, start_dir, end_dir)
        self.arcs.append(arc)
        return arc
    
    def get_crossing_position(self, idx: int) -> tuple:
        """Get the center position of a crossing.
        
        Args:
            idx: Crossing index
        
        Returns:
            (x, y) tuple of the crossing center
        """
        return (4 * idx, 4 * idx)
    
    def get_crossing_points(self, idx: int) -> Dict[str, tuple]:
        """Get all cardinal points of a crossing.
        
        Args:
            idx: Crossing index
        
        Returns:
            Dictionary with 'north', 'south', 'east', 'west' points
        """
        center_x = 4 * idx
        center_y = 4 * idx
        
        return {
            'north': (center_x, center_y + 1),
            'south': (center_x, center_y - 1),
            'east': (center_x + 1, center_y),
            'west': (center_x - 1, center_y)
        }
    
    def __str__(self) -> str:
        return (f"PreRectangularDiagram({self.num_crossings} crossings, "
                f"{len(self.arcs)} arcs)")
    
    def __repr__(self) -> str:
        return self.__str__()