# src/vkt/notation/arc.py

from typing import List, Tuple, Any
from .segment import Segment

__all__ = ["Arc"]


class Arc:
    """An arc connecting two crossings in a rectangular diagram.
    
    An arc consists of horizontal and vertical segments that connect
    two crossings at specific cardinal directions.
    
    Attributes:
        start_crossing: Starting crossing (or index)
        end_crossing: Ending crossing (or index)
        start_direction: 'north', 'south', 'east', or 'west'
        end_direction: 'north', 'south', 'east', or 'west'
        segments: List of Segment objects forming this arc
    """
    
    def __init__(
        self,
        start_crossing: Any,
        end_crossing: Any,
        start_direction: str,
        end_direction: str
    ):
        """Initialize an arc.
        
        Args:
            start_crossing: Starting crossing (or index)
            end_crossing: Ending crossing (or index)
            start_direction: Direction leaving start crossing
            end_direction: Direction entering end crossing
        """
        self.start_crossing = start_crossing
        self.end_crossing = end_crossing
        self.start_direction = start_direction
        self.end_direction = end_direction
        self.segments: List[Segment] = []
    
    def is_forward(self) -> bool:
        """Return True if this is a forward arc (start < end)."""
        return self.start_crossing < self.end_crossing
    
    def is_backward(self) -> bool:
        """Return True if this is a backward arc (start > end)."""
        return self.start_crossing > self.end_crossing
    
    def add_segment(self, start: Tuple[float, float], end: Tuple[float, float]):
        """Add a segment to this arc."""
        self.segments.append(Segment(start, end))
    
    def __str__(self) -> str:
        direction = "→" if self.is_forward() else "←"
        return (f"Arc({self.start_crossing}.{self.start_direction} {direction} "
                f"{self.end_crossing}.{self.end_direction}, {len(self.segments)} segments)")
    
    def __repr__(self) -> str:
        return self.__str__()