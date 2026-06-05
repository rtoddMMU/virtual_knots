from typing import Tuple, Optional
from .crossing import StrandRef
__all__ = ["Segment"]


class Segment:
    """A horizontal or vertical line segment in a rectangular diagram.

    Attributes:
        start: (x, y) starting point
        end: (x, y) ending point
        strand_ref: the StrandRef this segment belongs to, or None
    """

    def __init__(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        strand_ref: Optional["StrandRef"] = None
    ):
        self.start = start
        self.end = end
        self.strand_ref = strand_ref

    @property
    def is_horizontal(self) -> bool:
        return self.start[1] == self.end[1]

    @property
    def is_vertical(self) -> bool:
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
        if not self.is_vertical:
            raise ValueError("x property only valid for vertical segments")
        return self.start[0]

    @property
    def y(self) -> float:
        """Y-coordinate (for horizontal segments)."""
        if not self.is_horizontal:
            raise ValueError("y property only valid for horizontal segments")
        return self.start[1]

    def x_range(self) -> Tuple[float, float]:
        return (min(self.x1, self.x2), max(self.x1, self.x2))

    def y_range(self) -> Tuple[float, float]:
        return (min(self.y1, self.y2), max(self.y1, self.y2))

    def __str__(self) -> str:
        direction = "H" if self.is_horizontal else "V"
        return f"Segment[{direction}]({self.start} → {self.end})"

    def __repr__(self) -> str:
        return self.__str__()