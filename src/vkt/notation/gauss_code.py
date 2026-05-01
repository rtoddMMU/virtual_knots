# src/vkt/notation/gauss_code.py

import re
from typing import List, Tuple, Dict, Any
from .pre_rectangular_diagram import PreRectangularDiagram

__all__ = ["parse_gauss_code", "GaussCodeParser"]


class GaussCodeParser:
    """Parser for Gauss codes to build rectangular diagrams.
    
    A Gauss code is a sequence like: O1+ U2- O3+ U1- O2+ U3-
    
    Format:
    - O/U: Over or Under
    - number: crossing index (1-based in input, converted to 0-based internally)
    - +/-: sign of the crossing
    """
    
    def __init__(self, gauss_code: str):
        """Initialize parser with a Gauss code string.
        
        Args:
            gauss_code: String like "O1+ U2- O3+ U1- O2+ U3-"
        """
        self.gauss_code = gauss_code.strip()
        self.tokens = self._tokenize()
        self.crossing_signs = self._extract_crossing_signs()
        self.crossing_appearances = self._track_appearances()
    
    def _tokenize(self) -> List[Dict[str, Any]]:
        """Tokenize the Gauss code into structured elements.
        
        Returns:
            List of dictionaries with 'type' (O/U), 'crossing', 'sign'
        """
        # Pattern: (O or U)(digits)(+ or -)
        pattern = r'([OU])(\d+)([+-])'
        matches = re.findall(pattern, self.gauss_code)
        
        tokens = []
        for match in matches:
            over_under, crossing_num, sign = match
            tokens.append({
                'type': over_under,
                'crossing': int(crossing_num) - 1,  # Convert to 0-based
                'sign': 1 if sign == '+' else -1
            })
        
        return tokens
    
    def _extract_crossing_signs(self) -> Dict[int, int]:
        """Extract the sign of each crossing.
        
        Returns:
            Dictionary mapping crossing index to sign
        """
        signs = {}
        for token in self.tokens:
            crossing_idx = token['crossing']
            if crossing_idx not in signs:
                signs[crossing_idx] = token['sign']
        return signs
    
    def _track_appearances(self) -> Dict[int, List[Tuple[int, str]]]:
        """Track where each crossing appears in the code.
        
        Returns:
            Dictionary mapping crossing index to list of (position, type) tuples
        """
        appearances = {}
        for pos, token in enumerate(self.tokens):
            crossing_idx = token['crossing']
            if crossing_idx not in appearances:
                appearances[crossing_idx] = []
            appearances[crossing_idx].append((pos, token['type']))
        return appearances
    
    def _determine_arc_directions(
        self,
        start_token: Dict,
        end_token: Dict,
        start_idx: int,
        end_idx: int
    ) -> Tuple[str, str]:
        """Determine start_dir and end_dir for an arc.
        
        Rules:
        - Can only EXIT from: north, east
        - Can only ENTER to: south, west
        
        For positive crossings (+1):
        - Over strand: [west, east]
        - Under strand: [south, north]
        
        For negative crossings (-1):
        - Over strand: [south, north]
        - Under strand: [west, east]
        
        Args:
            start_token: Token where arc starts
            end_token: Token where arc ends
            start_idx: Index of start crossing
            end_idx: Index of end crossing
        
        Returns:
            (start_dir, end_dir) tuple
        """
        start_crossing = self.classical_crossings[start_idx]
        end_crossing = self.classical_crossings[end_idx]
        
        # Determine start direction
        if start_token['type'] == 'O':  # Over strand
            if start_crossing.sign == 1:  # Positive: over = [west, east]
                start_dir = 'east'  # Exit from east
            else:  # Negative: over = [south, north]
                start_dir = 'north'  # Exit from north
        else:  # Under strand
            if start_crossing.sign == 1:  # Positive: under = [south, north]
                start_dir = 'north'  # Exit from north
            else:  # Negative: under = [west, east]
                start_dir = 'east'  # Exit from east
        
        # Determine end direction
        if end_token['type'] == 'O':  # Over strand
            if end_crossing.sign == 1:  # Positive: over = [west, east]
                end_dir = 'west'  # Enter from west
            else:  # Negative: over = [south, north]
                end_dir = 'south'  # Enter from south
        else:  # Under strand
            if end_crossing.sign == 1:  # Positive: under = [south, north]
                end_dir = 'south'  # Enter from south
            else:  # Negative: under = [west, east]
                end_dir = 'west'  # Enter from west
        
        return start_dir, end_dir
    
    def build_diagram(self) -> PreRectangularDiagram:
        """Build a PreRectangularDiagram from the Gauss code.
        
        Returns:
            PreRectangularDiagram with crossings and arcs
        """
        diagram = PreRectangularDiagram()
        
        # Step 1: Create all classical crossings
        for crossing_idx in sorted(self.crossing_signs.keys()):
            sign = self.crossing_signs[crossing_idx]
            diagram.add_crossing(sign)
        
        # Store reference for direction determination
        self.classical_crossings = diagram.classical_crossings
        
        # Step 2: Create arcs between consecutive tokens
        for i in range(len(self.tokens)):
            start_token = self.tokens[i]
            end_token = self.tokens[(i + 1) % len(self.tokens)]  # Wrap around
            
            start_idx = start_token['crossing']
            end_idx = end_token['crossing']
            
            # Determine directions based on over/under and sign
            start_dir, end_dir = self._determine_arc_directions(
                start_token, end_token, start_idx, end_idx
            )
            
            # Add the arc
            diagram.add_arc(start_idx, end_idx, start_dir, end_dir)
        
        return diagram


def parse_gauss_code(gauss_code: str) -> PreRectangularDiagram:
    """Parse a Gauss code and return a PreRectangularDiagram.
    
    Args:
        gauss_code: String like "O1+ U2- O3+ U1- O2+ U3-"
    
    Returns:
        PreRectangularDiagram object
    """
    parser = GaussCodeParser(gauss_code)
    return parser.build_diagram()