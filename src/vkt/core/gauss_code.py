import re
from typing import List
from .crossing import Crossing, connect

def parse_gauss_code(gauss_code: str) -> List[Crossing]:
    """
    Parse a signed Gauss code and return a list of connected Crossing objects.
    
    Format: O1+U2+O3+U4+...
    - O/U: over/under strand
    - index: crossing number (starts at 1 in Gauss code)
    - +/-: crossing sign
    
    Convention:
    - sign '+': strand 0 = under, strand 1 = over
    - sign '-': strand 0 = over, strand 1 = under
    
    Returns crossings as 0-indexed list.
    """
    # Parse the Gauss code
    pattern = r'([OU])(\d+)([+-])'
    matches = re.findall(pattern, gauss_code)
    
    if not matches:
        raise ValueError(f"Invalid Gauss code: {gauss_code}")
    
    # Determine number of crossings and max index
    crossing_indices = [int(m[1]) for m in matches]
    max_index = max(crossing_indices)
    min_index = min(crossing_indices)
    
    if min_index != 1:
        raise ValueError(f"Gauss code indices should start at 1, found {min_index}")
    
    num_crossings = max_index
    
    # Verify each crossing appears exactly twice
    crossing_counts = {}
    for _, idx, _ in matches:
        idx = int(idx)
        crossing_counts[idx] = crossing_counts.get(idx, 0) + 1
    
    for idx in range(1, num_crossings + 1):
        count = crossing_counts.get(idx, 0)
        if count != 2:
            raise ValueError(f"Crossing {idx} appears {count} times (expected 2)")
    
    # Extract crossing signs from first occurrence
    crossing_signs = {}
    for ou, idx, sign in matches:
        idx = int(idx)
        if idx not in crossing_signs:
            crossing_signs[idx] = 1 if sign == '+' else -1
    
    # Create crossings (0-indexed array, but use 1-indexed signs)
    crossings = [Crossing(kind="classical", sign=crossing_signs[i+1]) 
                 for i in range(num_crossings)]
    
    # Build sequence of (crossing_obj, strand) pairs
    sequence = []
    for ou, idx, sign in matches:
        gauss_idx = int(idx)  # 1-indexed from Gauss code
        array_idx = gauss_idx - 1  # Convert to 0-indexed for array
        crossing = crossings[array_idx]
        
        # Determine which strand based on O/U and crossing sign
        if crossing.sign == 1:  # + crossing: strand 0 = under, strand 1 = over
            strand = 1 if ou == 'O' else 0
        else:  # - crossing: strand 0 = over, strand 1 = under
            strand = 0 if ou == 'O' else 1
        
        sequence.append((crossing, strand))
    
    # Connect the crossings
    for i in range(len(sequence)):
        current_crossing, current_strand = sequence[i]
        next_crossing, next_strand = sequence[(i + 1) % len(sequence)]
        
        connect(
            current_crossing.ref(current_strand),
            next_crossing.ref(next_strand)
        )
    
    return crossings