# src/vkt/notation/routing.py

from typing import Tuple, List
from .arc import Arc

__all__ = ["route_arc"]


def route_arc(
    start_idx: int,
    end_idx: int,
    start_dir: str,
    end_dir: str
) -> Tuple[List[float], List[float]]:
    """Route an arc between two crossings in a rectangular diagram.
    
    Args:
        start_idx: Index of starting crossing
        end_idx: Index of ending crossing
        start_dir: Direction leaving start crossing ('north', 'south', 'east', 'west')
        end_dir: Direction entering end crossing ('north', 'south', 'east', 'west')
    
    Returns:
        (x_coords, y_coords): Lists of coordinates for plotting
    
    Raises:
        ValueError: If the direction combination is invalid
    """
    
    # Forward arcs: start_idx < end_idx
    if start_idx < end_idx:
        j = start_idx
        k = end_idx
        
        if start_dir == 'east' and end_dir == 'south':
            x = [4*j+1, 4*k, 4*k]
            y = [4*j, 4*j, 4*k-1]
        elif start_dir == 'east' and end_dir == 'west':
            x = [4*j+1, 4*k-1, 4*k-1]
            y = [4*j, 4*j, 4*k]
        elif start_dir == 'north' and end_dir == 'south':
            x = [4*j, 4*k, 4*k]
            y = [4*j+1, 4*j+1, 4*k-1]
        elif start_dir == 'north' and end_dir == 'west':
            x = [4*j, 4*k-1, 4*k-1]
            y = [4*j+1, 4*j+1, 4*k]
        else:
            raise ValueError(
                f"Invalid forward arc: {start_dir} → {end_dir}. "
                f"Forward arcs must exit from north/east and enter at south/west."
            )
    
    # Backward arcs: start_idx > end_idx
    elif start_idx > end_idx:
        k = start_idx  # k is the larger index (where we start)
        j = end_idx    # j is the smaller index (where we end)
        
        if start_dir == 'east' and end_dir == 'south':
            x = [4*k+1, 4*k+1, 4*j-2, 4*j-2, 4*j]
            y = [4*k, 4*k+2, 4*k+2, 4*j-1, 4*j-1]
        elif start_dir == 'east' and end_dir == 'west':
            x = [4*k+1, 4*k+1, 4*j-1, 4*j-1]
            y = [4*k, 4*k+2, 4*k+2, 4*j]
        elif start_dir == 'north' and end_dir == 'south':
            x = [4*k, 4*j-2, 4*j-2, 4*j]
            y = [4*k+1, 4*k+1, 4*j-1, 4*j-1]
        elif start_dir == 'north' and end_dir == 'west':
            x = [4*k, 4*j-1, 4*j-1]
            y = [4*k+1, 4*k+1, 4*j]
        else:
            raise ValueError(
                f"Invalid backward arc: {start_dir} → {end_dir}. "
                f"Backward arcs must exit from north/east and enter at south/west."
            )
    else:
        raise ValueError(f"Cannot route arc from crossing {start_idx} to itself")
    
    return x, y


def create_arc_with_routing(
    start_idx: int,
    end_idx: int,
    start_dir: str,
    end_dir: str
) -> Arc:
    """Create an Arc object with segments computed from routing.
    
    Args:
        start_idx: Starting crossing index
        end_idx: Ending crossing index
        start_dir: Direction leaving start crossing
        end_dir: Direction entering end crossing
    
    Returns:
        Arc object with segments populated
    """
    arc = Arc(start_idx, end_idx, start_dir, end_dir)
    
    # Get the route coordinates
    x_coords, y_coords = route_arc(start_idx, end_idx, start_dir, end_dir)
    
    # Convert to segments
    for i in range(len(x_coords) - 1):
        start_point = (x_coords[i], y_coords[i])
        end_point = (x_coords[i+1], y_coords[i+1])
        arc.add_segment(start_point, end_point)
    
    return arc