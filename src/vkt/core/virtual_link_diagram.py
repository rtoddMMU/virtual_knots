from .crossing import Crossing, StrandRef
from typing import List, Iterable


class VirtualLinkDiagram:
    """
    Virtual link diagram - includes both classical and virtual crossings.
    Must be planar (all crossings properly connected in a planar diagram).
    """

    def __init__(self, crossings: Iterable[Crossing]):
        self.crossings: List[Crossing] = list(crossings)
        
        # Assign IDs
        for i, c in enumerate(self.crossings):
            c.id = i

    # --- validation ---
    def validate(self) -> None:
        """Check structural correctness."""
        for c in self.crossings:
            for i in (0, 1):
                if c.next[i] is None or c.prev[i] is None:
                    raise RuntimeError(f"Crossing {c.id} has incomplete connections")

                # consistency check
                nxt = c.next[i]
                if nxt.prev() != c.ref(i):
                    raise RuntimeError("next/prev inconsistency")
        
        if not self.planar():
            raise ValueError("Diagram is not planar.")

    # --- traversal ---
    def strands(self) -> Iterable[StrandRef]:
        """Yield all strand references in the diagram."""
        for c in self.crossings:
            yield StrandRef(c, 0)
            yield StrandRef(c, 1)

    def components(self) -> List[List[StrandRef]]:
        """Return components as lists of StrandRefs."""
        seen = set()
        comps = []

        for s in self.strands():
            if (s.crossing, s.strand) in seen:
                continue

            comp = []
            current = s

            while (current.crossing, current.strand) not in seen:
                seen.add((current.crossing, current.strand))
                comp.append(current)
                current = current.next()

            comps.append(comp)

        return comps
    
    def seifert_components(self) -> List[List[StrandRef]]:
        """
        Return Seifert circles as lists of StrandRefs.
        Each Seifert circle is formed by alternating next() and jump().
        We append both the position after next() and after jump() to see the smoothing.
        """
        visited = set()  # Track (crossing, strand) pairs we've seen
        circles = []
        
        for c in self.crossings:
            for strand in (0, 1):
                start = c.ref(strand)
                
                # Skip if we've already visited this position
                if (start.crossing, start.strand) in visited:
                    continue
                
                # Trace the Seifert circle
                circle = []
                current = start
                
                while True:
                    # Mark current position as visited
                    visited.add((current.crossing, current.strand))
                    circle.append(current)
                    
                    # Move to next crossing
                    current = current.next()
                    circle.append(current)  # Append after next()
                    
                    # Jump to other strand (smoothing happens here)
                    current = current.jump()
                    # Don't append after jump yet - it becomes the next iteration's start
                    
                    if current == start:
                        break
                
                circles.append(circle)
        
            return circles
    
    def disoriented_seifert_components(self) -> List[List[tuple]]:
        """
        Return disoriented Seifert circles.
        Each element is (StrandRef, is_outgoing).
        Traversal: next() when outgoing, prev() when incoming, flip direction, then jump().
        Record state after both next()/prev() and after jump().
        """
        visited = set()
        circles = []

        for c in self.crossings:
            for strand in (0, 1):
                for is_outgoing in (False, True):
                    
                    start_ref = c.ref(strand)
                    #print(f"start ref is {start_ref, is_outgoing}\n")
                    start_state = (start_ref.crossing, start_ref.strand, is_outgoing)
                    
                    if start_state in visited:
                        #print(f"we've already seen {start_state}. Moving on.\n")
                        continue
                    
                    visited.add(start_state)
                    
                    circle = [(start_ref, is_outgoing)]
                    current_ref = start_ref
                    current_outgoing = is_outgoing
                    
                    while True:
                        
                        if current_outgoing:
                            current_ref = current_ref.next()
                        else:
                            current_ref = current_ref.prev()
                        
                        current_outgoing = not current_outgoing
                        
                        visited.add((current_ref.crossing, current_ref.strand, current_outgoing))
                        circle.append((current_ref, current_outgoing))
                        
                        #print("----------------\n")
                        #print(f"current {current_ref, current_outgoing}")
                        #print("----------------\n")
                        
                        current_ref = current_ref.jump()
                        visited.add((current_ref.crossing, current_ref.strand, current_outgoing))
                        circle.append((current_ref, current_outgoing))
                        #print("+++++++++++++++++\n")
                        #print(f"current {current_ref, current_outgoing}")
                        #print("+++++++++++++++++\n")
                        
                        if (current_ref.crossing == start_ref.crossing and 
                            current_ref.strand == start_ref.strand and
                            current_outgoing == is_outgoing):
                            
                            #print('just arrived back at start')
                            break
                            
                    circles.append(circle)
                    
        return circles
        
    def euler(self) ->int:
     
        return len(self.seifert_components()) + len(self.disoriented_seifert_components()) -len(self.crossings)
    
    def planar(self) -> bool:

        if self.euler() == 2:
            return True
        else:
            return False

    # --- properties ---
    def num_crossings(self) -> int:
        return len(self.crossings)

    def num_classical_crossings(self) -> int:
        return sum(1 for c in self.crossings if c.is_classical())

    def num_virtual_crossings(self) -> int:
        return sum(1 for c in self.crossings if c.is_virtual())


    def __repr__(self):
        return (f"VirtualLinkDiagram({self.num_crossings()} crossings: "
                f"{self.num_classical_crossings()} classical, "
                f"{self.num_virtual_crossings()} virtual)")