from __future__ import annotations

from typing import Optional, List

__all__ = ["Crossing", "StrandRef", "connect"]

class StrandRef:
    __slots__ = ("crossing", "strand")

    def __init__(self, crossing: Optional["Crossing"] = None, strand: int = 0):
        self.crossing = crossing
        self.strand = strand

    def __bool__(self):
        return self.crossing is not None

    def next(self) -> "StrandRef":
        nxt = self.crossing.next[self.strand]
        if nxt is None:
            raise RuntimeError("next not set")
        return nxt

    def prev(self) -> "StrandRef":
        prv = self.crossing.prev[self.strand]
        if prv is None:
            raise RuntimeError("prev not set")
        return prv

    def jump(self) -> "StrandRef":
        return StrandRef(self.crossing, self.strand ^ 1)

    def __repr__(self):
        return f"StrandRef(crossing={self.crossing.id}, strand={self.strand})"


class Crossing:
    __slots__ = ("kind", "sign", "next", "prev", "id")

    _id_counter = 0

    def __init__(self, kind: str = "virtual", sign: Optional[int] = None):

        if kind not in ("classical", "virtual"):
            raise ValueError("kind must be 'classical' or 'virtual'")
        
        if kind == "classical":
            if sign not in (-1,1):
                raise ValueError("classical crossings must have sign +/-1")
        
        if kind == "virtual" and sign is not None:
            raise ValueError("virutal crossings cann't have a sign")
        
        self.kind = kind
        self.sign = sign if kind == "classical" else None

        # strand 0: south ↔ north
        # strand 1: west ↔ east
        self.next: List[Optional[StrandRef]] = [None, None] # 0: crossing and strand North goes to. 1: crossing and stand East goes to
        self.prev: List[Optional[StrandRef]] = [None, None] # 0 crossing and stand south comes from. 1: Crossing and strand West comes from.

        self.id = Crossing._id_counter
        Crossing._id_counter += 1

    def is_classical(self) -> bool:
        return self.kind == "classical"

    def is_virtual(self) -> bool:
        return self.kind == "virtual"

    def ref(self, strand: int) -> StrandRef:
        return StrandRef(self, strand)

    def get_next(self, strand: int) -> Optional[StrandRef]:
        return self.next[strand]

    def get_prev(self, strand: int) -> Optional[StrandRef]:
        return self.prev[strand]

    def over_strand(self) -> Optional[int]:
        if self.kind != "classical":
            return None
        return 1 if self.sign == 1 else 0

    def under_strand(self) -> Optional[int]:
        if self.kind != "classical":
            return None
        return self.over_strand() ^ 1

    def __repr__(self):
        return f"Crossing(id={self.id}, kind={self.kind}, sign={self.sign})"



def connect(a: StrandRef, b: StrandRef) -> None:
    # Optional safety checks
    if a.crossing.next[a.strand] is not None:
        raise RuntimeError("next already set")
    if b.crossing.prev[b.strand] is not None:
        raise RuntimeError("prev already set")

    a.crossing.next[a.strand] = b
    b.crossing.prev[b.strand] = a


def disconnect(a: StrandRef):
    b = a.next()
    a.crossing.next[a.strand] = None
    b.crossing.prev[b.strand] = None
