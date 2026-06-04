from .crossing import Crossing, StrandRef, connect, disconnect
from typing import List, Iterable, Literal
from .segment import Segment
from .arc_routing_strandref import route_arc_from_strandref
import matplotlib.pyplot as plt

def _event_sort_key(e):
        type_priority = {'vertical_start': 0, 'horizontal': 1, 'vertical_end': 2}
        return (e['y'], type_priority[e['type']])

class VirtualLinkDiagram:
    """
    Virtual link diagram - includes both classical and virtual crossings.
    Must be planar (all crossings properly connected in a planar diagram).
    """

    def __init__(self, link: "VirtualLink"):
        self.link = link
        self.arc_routes: dict = {}
        self.virtual_crossings: list = []
 

    @property
    def crossings(self) -> List[Crossing]:
        return self.link.crossings
    
    def compute_arc_routes(self):
        for crossing in self.crossings:
            for i in range(2):
                ref = crossing.ref(i)
                result = route_arc_from_strandref(ref)
                if result is None:
                    continue
                xs, ys = result
                self.arc_routes[ref] = [
                    Segment(
                        start=(xs[j], ys[j]),
                        end=(xs[j+1], ys[j+1]),
                        strand_ref=ref
                    )
                    for j in range(len(xs) - 1)
                ]
    # --- plot a diagram ---
    def plot(self, ax=None, show=True):
        if ax is None:
            fig, ax = plt.subplots()

        all_vals = []

        # Plot arcs from precomputed routes
        for ref, segments in self.arc_routes.items():
            for seg in segments:
                xs = [seg.start[0], seg.end[0]]
                ys = [seg.start[1], seg.end[1]]
                all_vals.extend(xs)
                all_vals.extend(ys)
                ax.plot(xs, ys, color='steelblue')

        # Plot crossings
        for n, crossing in enumerate(self.crossings):
            cx, cy = 4 * n, 4 * n
            if crossing.sign == 1:  # positive: x-axis over, y-axis broken
                ax.plot([cx - 1, cx + 1], [cy, cy], color='black')
                ax.plot([cx, cx], [cy - 1, cy - 0.2], color='black')
                ax.plot([cx, cx], [cy + 0.2, cy + 1], color='black')
            elif crossing.sign == -1:  # negative: y-axis over, x-axis broken
                ax.plot([cx, cx], [cy - 1, cy + 1], color='black')
                ax.plot([cx - 1, cx - 0.2], [cy, cy], color='black')
                ax.plot([cx + 0.2, cx + 1], [cy, cy], color='black')
            # virtual crossings (sign=None) are skipped

        if all_vals:
            lim = [min(all_vals), max(all_vals)]
            ax.plot(lim, [v + 1 for v in lim], color='red', linestyle='--', alpha=0.3)

        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout()

        if show:
            plt.show()

        return ax

    

    def find_virtual_crossings(self) -> list:
        """
        Find all virtual crossings using a line sweep algorithm.
        Returns a list of (vertical_ref, horizontal_ref) tuples.
        Collect all intersections first, then insert.
        """
        events = []

        for ref, segments in self.arc_routes.items():
            for seg in segments:
                if seg.is_horizontal:
                    x_min, x_max = seg.x_range()
                    events.append({
                        'type': 'horizontal',
                        'y': seg.start[1],
                        'x_min': x_min,
                        'x_max': x_max,
                        'ref': ref,
                        'seg': seg
                    })
                else:  # vertical
                    y_min, y_max = seg.y_range()
                    events.append({
                        'type': 'vertical_start',
                        'y': y_min,
                        'x': seg.start[0],
                        'y_max': y_max,
                        'ref': ref,
                        'seg': seg
                    })
                    events.append({
                        'type': 'vertical_end',
                        'y': y_max,
                        'x': seg.start[0],
                        'ref': ref,
                        'seg': seg
                    })

        

        events.sort(key=_event_sort_key)

        active_verticals = []
        intersections = []

        for event in events:
            if event['type'] == 'vertical_start':
                active_verticals.append(event)

            elif event['type'] == 'vertical_end':
                active_verticals = [
                    v for v in active_verticals
                    if v['seg'] is not event['seg']
                ]

            elif event['type'] == 'horizontal':
                for v in active_verticals:
                    if event['x_min'] <= v['x'] <= event['x_max']:
                        if v['y'] <= event['y'] <= v['y_max']:
                            if event['ref'] is not v['ref']:
                                intersections.append((v['ref'], event['ref']))

        return intersections

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
        
    # --- Build arcs ---


    # --- editing ---
    def admit_virtual_crossing(self, 
                               strand_ref1: StrandRef, 
                               strand_ref2: StrandRef,
                               strand_ref1_connects_to: Literal[0, 1],  # 0 or 1
                               strand_ref2_connects_to: Literal[0, 1]   # 0 or 1
                               ) -> Crossing:
        """
        Insert a virtual crossing between two arcs. 
        It's called 'admit' because we are not changing how the classical crossings connect.
        
        Given two strand references that define arcs:
        - arc1: strand_ref1 -> strand_ref1.next()
        - arc2: strand_ref2 -> strand_ref2.next()
        
        Creates a virtual crossing that connects these arcs.
        
        Args:
        strand_ref1: First arc's starting position
        strand_ref2: Second arc's starting position
        strand_ref1_connects_to: Which strand (0 or 1) of the virtual crossing strand_ref1 connects to
        strand_ref2_connects_to: Which strand (0 or 1) of the virtual crossing strand_ref2 connects to
        
        Returns:
            The newly created virtual crossing

        Raises:
        ValueError: If both strand_refs connect to the same virtual crossing strand
        
        """
        # check that the *_connects_to values are different
        if strand_ref1_connects_to == strand_ref2_connects_to:
            raise ValueError(f"strand_ref1_connects_to and strand_ref2_connects_to both connect to {strand_ref1_connects_to}. This is not allowed.")
        

        # Store the original next positions
        old_next1 = strand_ref1.next()
        old_next2 = strand_ref2.next()
        
        # Create the virtual crossing
        virtual = Crossing(kind="virtual")
        
        # Insert into crossings list and assign ID
        self.crossings.append(virtual)
        virtual.id = len(self.crossings) - 1
        
        # Determine which strands to use based on flag
        #if flag == 0:
         #   v_strand1 = 0
          #  v_strand2 = 1
        #else:
         #   v_strand1 = 1
          #  v_strand2 = 0
        
        # Reconnect strand_ref1's arc through the virtual crossing
        disconnect(strand_ref1)
        connect(strand_ref1, virtual.ref(strand_ref1_connects_to))
        connect(virtual.ref(strand_ref1_connects_to), old_next1)
        
        # Reconnect strand_ref2's arc through the virtual crossing
        disconnect(strand_ref2)
        connect(strand_ref2, virtual.ref(strand_ref2_connects_to))
        connect(virtual.ref(strand_ref2_connects_to), old_next2)
        
        return virtual
    
    # --- Add all the found virtual crossings ---
    def compute_virtual_crossings(self):
        while True:
            intersections = self.find_virtual_crossings()
            if not intersections:
                break
            v_ref, h_ref = intersections[0]
            self.admit_virtual_crossing(v_ref, h_ref, 0, 1)


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