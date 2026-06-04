from .crossing import StrandRef
from typing import List


def route_arc_from_strandref(strand_ref: StrandRef) -> tuple[list[float], list[float]]:
    """
    Route an outgoing arc from a StrandRef in a rectangular diagram.
    
    Classical crossings are positioned at (4n, 4n).
    
    Convention:
    - strand 0 exits North, enters South
    - strand 1 exits East, enters West
    
    Args:
        strand_ref: Starting StrandRef (outgoing from its crossing)
    
    Returns:
        (x_coords, y_coords): Lists of coordinates for plotting
    """
    


    start_crossing = strand_ref.crossing
    j = start_crossing.id
    
    # Follow to the next crossing
    end_ref = strand_ref.next()
    k = end_ref.crossing.id
    
    end_crossing = end_ref.crossing

    # Check that both crossings are classical
    if not start_crossing.is_classical():
        raise ValueError(f"Start crossing (id={start_crossing.id}) must be classical, got {start_crossing.kind}")
    
    if not end_crossing.is_classical():
        raise ValueError(f"End crossing (id={end_crossing.id}) must be classical, got {end_crossing.kind}")


    # Determine arc type based on strand numbers
    start_strand = strand_ref.strand
    end_strand = end_ref.strand
    
    # Forward arcs: j < k
    if j < k:
        if start_strand == 1 and end_strand == 0:  # East → South
            x = [4*j+1, 4*k, 4*k]
            y = [4*j, 4*j, 4*k-1]
        elif start_strand == 1 and end_strand == 1:  # East → West
            x = [4*j+1, 4*k-1, 4*k-1]
            y = [4*j, 4*j, 4*k]
        elif start_strand == 0 and end_strand == 0:  # North → South
            x = [4*j, 4*k, 4*k]
            y = [4*j+1, 4*j+1, 4*k-1]
        elif start_strand == 0 and end_strand == 1:  # North → West
            x = [4*j, 4*k-1, 4*k-1]
            y = [4*j+1, 4*j+1, 4*k]
        else:
            raise ValueError(f"Invalid forward arc: strand {start_strand} → strand {end_strand}")
    
    # Backward arcs: j > k
    elif j > k:
        if start_strand == 1 and end_strand == 0:  # East → South
            x = [4*j+1, 4*j+1, 4*k-2, 4*k-2, 4*k]
            y = [4*j, 4*j+2, 4*j+2, 4*k-1, 4*k-1]
        elif start_strand == 1 and end_strand == 1:  # East → West
            x = [4*j+1, 4*j+1, 4*k-1, 4*k-1]
            y = [4*j, 4*j+2, 4*j+2, 4*k]
        elif start_strand == 0 and end_strand == 0:  # North → South
            x = [4*j, 4*k-2, 4*k-2, 4*k]
            y = [4*j+1, 4*j+1, 4*k-1, 4*k-1]
        elif start_strand == 0 and end_strand == 1:  # North → West
            x = [4*j, 4*k-1, 4*k-1]
            y = [4*j+1, 4*j+1, 4*k]
        else:
            raise ValueError(f"Invalid backward arc: strand {start_strand} → strand {end_strand}")
    else:
        raise ValueError(f"Cannot route arc from crossing {j} to itself") # This will need to be fixed. 
    
    return x, y