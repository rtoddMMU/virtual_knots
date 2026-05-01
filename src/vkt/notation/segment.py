# src/vkt/notation/segment.py

from typing import Tuple

__all__ = ["Segment"]


class Segment:
    """A horizontal or vertical line segment in a rectangular diagram.
    
    Attributes:
        start: (x, y) starting point
        end: (x, y) ending point
    """
    
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float]):
        """Initialize a segment.
        
        Args:
            start: (x, y) starting point
            end: (x, y) ending point
        """
        self.start = start
        self.end = end
    
    def is_horizontal(self) -> bool:
        """Return True if this is a horizontal segment."""
        return self.start[1] == self.end[1]
    
    def is_vertical(self) -> bool:
        """Return True if this is a vertical segment."""
        return self.start[0] == self.end[0]
    
    @property
    def x1(self) -> float:
        return self.start[0]
    
    @property
    def y1(self) -> float:
        return self.start[1]
    
    @property
    def x2(self) -> float:
        return self.end[0]
    
    @property
    def y2(self) -> float:
        return self.end[1]
    
    @property
    def x(self) -> float:
        """X-coordinate (for vertical segments)."""
        if not self.is_vertical():
            raise ValueError("x property only valid for vertical segments")
        return self.start[0]
    
    @property
    def y(self) -> float:
        """Y-coordinate (for horizontal segments)."""
        if not self.is_horizontal():
            raise ValueError("y property only valid for horizontal segments")
        return self.start[1]
    
    def x_range(self) -> Tuple[float, float]:
        """Return (min_x, max_x) for this segment."""
        return (min(self.x1, self.x2), max(self.x1, self.x2))
    
    def y_range(self) -> Tuple[float, float]:
        """Return (min_y, max_y) for this segment."""
        return (min(self.y1, self.y2), max(self.y1, self.y2))
    
    def __str__(self) -> str:
        direction = "H" if self.is_horizontal() else "V"
        return f"Segment[{direction}]({self.start} → {self.end})"
    
    def __repr__(self) -> str:
        return self.__str__()