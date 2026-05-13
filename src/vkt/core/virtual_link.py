from typing import List, Iterable


class VirtualLink:
    """
    Abstract virtual link (no virtual crossings). This includes classical links. It should be thought about as the traversable version of gauss code. 
    One ought to be able to compute such invariants that don't 'see' virutal crossings. 
    We check to make sure that crossings are all classical only bevause virutal crossings exist as an object and will be used in constructin virtual diagrams.
    """

    def __init__(self, crossings: Iterable[Crossing]):
        self.crossings: List[Crossing] = list(crossings)

        # Enforce invariant: only classical crossings. This does not mean that we have a classical knot. Only that we are starting from the clasical crossings only.
        for c in self.crossings:
            if not c.is_classical():
                raise ValueError("VirtualLink cannot contain virtual crossings")

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

    # --- traversal ---
    def strands(self) -> Iterable"""Yield all strand references in the link. Here we are build all the naturally occuring strand refs that will be needed"""
        for c in self.crossings:
            yield StrandRef(c, 0)
            yield StrandRef(c, 1)

    def components(self) -> List[List[StrandRef]]:
        """
        Return components as lists of StrandRefs.
        I don't think this will currently work.
        """
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

    # --- convenience ---
    def num_crossings(self) -> int:
        return len(self.crossings)

    def __repr__(self):
        return f"VirtualLink({len(self.crossings)} crossings)"