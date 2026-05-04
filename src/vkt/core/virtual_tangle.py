# src/vkt/core/virtual_tangle.py

from __future__ import annotations
from typing import List, Dict, Tuple, Optional, Set, Union
from .crossing import Crossing
from .classical_crossing import ClassicalCrossing
from .virtual_crossing import VirtualCrossing

__all__ = ["VirtualTangle"]
__version__ = "0.1.0"
__author__ = "Robert Todd"


class VirtualTangle:
    """A virtual tangle represented as a graph of crossings.
    
    Crossings are vertices with degree 4 (or less for tangles with open ends).
    Arcs are directed edges connecting exit points to entry points.
    Faces are cycles formed by oriented smoothings.
    
    The tangle can represent:
    - Virtual knots (all crossings fully connected, single component)
    - Virtual links (all crossings fully connected, multiple components)
    - Virtual tangles (some crossings have open ends)
    
    Attributes:
        crossings: List of all Crossing objects (classical and virtual)
    """
    
    def __init__(self):
        """Initialize an empty virtual tangle."""
        self.crossings: List[Crossing] = []
        self._crossing_index: Dict[int, Crossing] = {}  # id -> crossing lookup
    
    # ========== CROSSING MANAGEMENT ==========
    
    def add_crossing(self, crossing: Crossing) -> int:
        """Add a crossing to the tangle.
        
        Args:
            crossing: Crossing object to add
            
        Returns:
            Index of the added crossing in the crossings list
        """
        self.crossings.append(crossing)
        self._crossing_index[crossing.id] = crossing
        return len(self.crossings) - 1
    
    def remove_crossing(self, crossing: Crossing) -> None:
        """Remove a crossing from the tangle.
        
        Disconnects all arcs connected to this crossing.
        
        Args:
            crossing: Crossing to remove
        """
        # Disconnect all connections
        if crossing.north_successor:
            crossing.disconnect_successor('north')
        if crossing.east_successor:
            crossing.disconnect_successor('east')
        if crossing.south_predecessor:
            crossing.disconnect_predecessor('south')
        if crossing.west_predecessor:
            crossing.disconnect_predecessor('west')
        
        # Remove from lists
        self.crossings.remove(crossing)
        del self._crossing_index[crossing.id]
    
    def get_crossing_by_id(self, crossing_id: int) -> Optional[Crossing]:
        """Get a crossing by its ID.
        
        Args:
            crossing_id: Unique ID of the crossing
            
        Returns:
            Crossing object or None if not found
        """
        return self._crossing_index.get(crossing_id)
    
    @property
    def num_crossings(self) -> int:
        """Return the total number of crossings."""
        return len(self.crossings)
    
    @property
    def num_classical_crossings(self) -> int:
        """Return the number of classical crossings."""
        return sum(1 for c in self.crossings if c.is_classical())
    
    @property
    def num_virtual_crossings(self) -> int:
        """Return the number of virtual crossings."""
        return sum(1 for c in self.crossings if c.is_virtual())
    
    # ========== ARC MANAGEMENT (NetworkX-style) ==========
    
    def add_arc(
        self, 
        c1: Union[Crossing, int], 
        exit_dir: str, 
        c2: Union[Crossing, int], 
        entry_dir: str
    ) -> None:
        """Add an arc connecting an exit to an entry.
        
        Args:
            c1: First crossing (object or index)
            exit_dir: Exit direction on first crossing ('north' or 'east')
            c2: Second crossing (object or index)
            entry_dir: Entry direction on second crossing ('south' or 'west')
        """
        # Handle both object and index inputs
        if isinstance(c1, int):
            c1 = self.crossings[c1]
        if isinstance(c2, int):
            c2 = self.crossings[c2]
        
        # Set the connection (this handles validation)
        c1.set_successor(exit_dir, c2, entry_dir)
    
    @property
    def arcs(self) -> List[Dict]:
        """Return all arcs as a list of dictionaries.
        
        Each arc dictionary contains:
            - 'start_crossing': Starting crossing object
            - 'start_direction': Exit direction ('north' or 'east')
            - 'end_crossing': Ending crossing object
            - 'end_direction': Entry direction ('south' or 'west')
        
        Returns:
            List of arc dictionaries
        """
        arc_list = []
        
        for crossing in self.crossings:
            # Check north successor
            if crossing.north_successor:
                end_crossing, end_dir = crossing.north_successor
                arc_list.append({
                    'start_crossing': crossing,
                    'start_direction': 'north',
                    'end_crossing': end_crossing,
                    'end_direction': end_dir
                })
            
            # Check east successor
            if crossing.east_successor:
                end_crossing, end_dir = crossing.east_successor
                arc_list.append({
                    'start_crossing': crossing,
                    'start_direction': 'east',
                    'end_crossing': end_crossing,
                    'end_direction': end_dir
                })
        
        return arc_list
    
    def get_outgoing_arc(self, crossing: Crossing, direction: str) -> Optional[Dict]:
        """Get the arc exiting from a crossing's direction.
        
        Args:
            crossing: Starting crossing
            direction: Exit direction ('north' or 'east')
            
        Returns:
            Arc dictionary with keys:
                - 'start_crossing': Starting crossing object
                - 'start_direction': Exit direction
                - 'end_crossing': Ending crossing object
                - 'end_direction': Entry direction
            Returns None if no arc exists.
            
        Raises:
            ValueError: If direction is not 'north' or 'east'
        """
        if direction not in ('north', 'east'):
            raise ValueError(f"Outgoing arcs must use exit directions ('north' or 'east'), got '{direction}'")
        
        successor = crossing.get_successor(direction)
        if successor is None:
            return None
        
        end_crossing, end_dir = successor
        return {
            'start_crossing': crossing,
            'start_direction': direction,
            'end_crossing': end_crossing,
            'end_direction': end_dir
        }
    
    def get_incoming_arc(self, crossing: Crossing, direction: str) -> Optional[Dict]:
        """Get the arc entering at a crossing's direction.
        
        Args:
            crossing: Ending crossing
            direction: Entry direction ('south' or 'west')
            
        Returns:
            Arc dictionary with keys:
                - 'start_crossing': Starting crossing object
                - 'start_direction': Exit direction
                - 'end_crossing': Ending crossing object
                - 'end_direction': Entry direction
            Returns None if no arc exists.
            
        Raises:
            ValueError: If direction is not 'south' or 'west'
        """
        if direction not in ('south', 'west'):
            raise ValueError(f"Incoming arcs must use entry directions ('south' or 'west'), got '{direction}'")
        
        predecessor = crossing.get_predecessor(direction)
        if predecessor is None:
            return None
        
        start_crossing, start_dir = predecessor
        return {
            'start_crossing': start_crossing,
            'start_direction': start_dir,
            'end_crossing': crossing,
            'end_direction': direction
        }
    
    # ========== TRAVERSAL ==========
    
    def traverse_strand(
        self, 
        start_crossing: Crossing, 
        start_direction: str
    ) -> List[Tuple[Crossing, str]]:
        """Traverse a strand starting from a crossing and direction.
        
        Follows the strand through the tangle until reaching an open end
        or returning to the starting point.
        
        Args:
            start_crossing: Starting crossing
            start_direction: Starting direction (entry: 'south'/'west')
            
        Returns:
            List of (crossing, direction) tuples representing the path
        """
        path = []
        current = start_crossing
        current_dir = start_direction
        
        visited = set()
        
        while True:
            # Determine exit direction based on entry
            if current_dir == 'south':
                exit_dir = 'north'  # Vertical strand
            elif current_dir == 'west':
                exit_dir = 'east'   # Horizontal strand
            else:
                raise ValueError(f"Can only start traversal from entry directions, not '{current_dir}'")
            
            # Record this crossing
            path.append((current, current_dir))
            
            # Check for loops
            state = (id(current), current_dir)
            if state in visited:
                break
            visited.add(state)
            
            # Get successor
            successor = current.get_successor(exit_dir)
            if successor is None:
                # Reached an open end (tangle)
                break
            
            # Move to next crossing
            current, current_dir = successor
            
            # Check if we've returned to start
            if current is start_crossing and current_dir == start_direction:
                break
        
        return path
    
    # ========== FACE DETECTION (TO BE IMPLEMENTED) ==========
    
    def find_oriented_smoothing_cycles(self) -> List[List[Tuple[Crossing, str]]]:
        """Find all cycles formed by the oriented smoothing.
        
        Returns:
            List of cycles, where each cycle is a list of (crossing, direction) tuples
        """
        # TODO: Implement oriented smoothing traversal
        raise NotImplementedError("Oriented smoothing cycle detection not yet implemented")
    
    def find_dual_faces(self) -> List[List[Tuple[Crossing, str]]]:
        """Find all dual faces (regions bounded by the diagram).
        
        Returns:
            List of faces, where each face is a list of (crossing, direction) tuples
        """
        # TODO: Implement dual face detection
        raise NotImplementedError("Dual face detection not yet implemented")
    
    # ========== REIDEMEISTER MOVES (TO BE IMPLEMENTED) ==========
    
    def reidemeister_1_add(self, arc, face, sign):
        """Add a twist (R1 move) on an arc adjacent to a face.
        
        Args:
            arc: Arc to add twist to
            face: Adjacent face
            sign: +1 or -1 for crossing sign
        """
        # TODO: Implement
        raise NotImplementedError("Reidemeister 1 (add) not yet implemented")
    
    def reidemeister_1_remove(self, crossing):
        """Remove a twist (R1 move).
        
        Args:
            crossing: Crossing to remove (must be a twist)
        """
        # TODO: Implement
        raise NotImplementedError("Reidemeister 1 (remove) not yet implemented")
    
    def reidemeister_2_add(self, arc1, arc2, face):
        """Add two crossings (R2 move) between parallel arcs across a face.
        
        Args:
            arc1: First arc
            arc2: Second arc (parallel to first)
            face: Face between the arcs
        """
        # TODO: Implement
        raise NotImplementedError("Reidemeister 2 (add) not yet implemented")
    
    def reidemeister_2_remove(self, crossing1, crossing2):
        """Remove two crossings (R2 move).
        
        Args:
            crossing1: First crossing
            crossing2: Second crossing (must form R2 pair)
        """
        # TODO: Implement
        raise NotImplementedError("Reidemeister 2 (remove) not yet implemented")
    
    def reidemeister_3(self, triangle_face):
        """Perform R3 move on a triangular face.
        
        Args:
            triangle_face: Triangular face with three crossings
        """
        # TODO: Implement
        raise NotImplementedError("Reidemeister 3 not yet implemented")
    
    # ========== CONSTRUCTION FROM DIAGRAM ==========
    
    @classmethod
    def from_rectangular_diagram(cls, diagram):
        """Build a VirtualTangle from a PreRectangularDiagram.
        
        Args:
            diagram: PreRectangularDiagram object
            
        Returns:
            VirtualTangle with all crossings and connections
        """
        # TODO: Implement in next step
        raise NotImplementedError("Construction from rectangular diagram not yet implemented")
    
    # ========== UTILITY ==========
    
    def is_closed(self) -> bool:
        """Check if this is a closed knot/link (no open ends).
        
        Returns:
            True if all crossings are fully connected
        """
        for crossing in self.crossings:
            if (crossing.north_successor is None or 
                crossing.east_successor is None or
                crossing.south_predecessor is None or
                crossing.west_predecessor is None):
                return False
        return True
    
    def __str__(self) -> str:
        tangle_type = "Knot/Link" if self.is_closed() else "Tangle"
        return f"Virtual{tangle_type}({self.num_classical_crossings} classical, {self.num_virtual_crossings} virtual)"
    
    def __repr__(self) -> str:
        return self.__str__()