# tests/test_crossings.py

import pytest
from src.vkt.core import Crossing, ClassicalCrossing, VirtualCrossing


def test_classical_crossing_creation():
    """Test creating classical crossings with signs."""
    # Positive crossing
    pos = ClassicalCrossing(sign=1, south="a1", north="a2", west="b1", east="b2")
    assert pos.sign == 1
    assert pos.is_positive()
    assert not pos.is_negative()
    assert pos.is_classical()
    assert not pos.is_virtual()
    
    # Negative crossing
    neg = ClassicalCrossing(sign=-1, south="c1", north="c2", west="d1", east="d2")
    assert neg.sign == -1
    assert neg.is_negative()
    assert not neg.is_positive()


def test_classical_crossing_sign_validation():
    """Test that invalid signs raise ValueError."""
    with pytest.raises(ValueError):
        ClassicalCrossing(sign=0)
    
    with pytest.raises(ValueError):
        ClassicalCrossing(sign=2)


def test_sign_flip():
    """Test flipping the sign of a crossing."""
    crossing = ClassicalCrossing(sign=1)
    assert crossing.sign == 1
    
    crossing.flip_sign()
    assert crossing.sign == -1
    
    crossing.flip_sign()
    assert crossing.sign == 1


def test_positive_crossing_over_under():
    """Test over/under strands for positive crossing."""
    pos = ClassicalCrossing(sign=1, south="s", north="n", west="w", east="e")
    
    # Positive: over = [west, east], under = [south, north]
    assert pos.over_strand == ["w", "e"]
    assert pos.under_strand == ["s", "n"]


def test_negative_crossing_over_under():
    """Test over/under strands for negative crossing."""
    neg = ClassicalCrossing(sign=-1, south="s", north="n", west="w", east="e")
    
    # Negative: over = [south, north], under = [west, east]
    assert neg.over_strand == ["s", "n"]
    assert neg.under_strand == ["w", "e"]


def test_sign_flip_changes_over_under():
    """Test that flipping sign swaps over/under strands."""
    crossing = ClassicalCrossing(sign=1, south="s", north="n", west="w", east="e")
    
    # Initially positive
    assert crossing.over_strand == ["w", "e"]
    assert crossing.under_strand == ["s", "n"]
    
    # Flip to negative
    crossing.flip_sign()
    assert crossing.over_strand == ["s", "n"]
    assert crossing.under_strand == ["w", "e"]


def test_virtual_crossing():
    """Test creating virtual crossings."""
    virtual = VirtualCrossing(south="e1", north="e2", west="f1", east="f2")
    assert virtual.is_virtual()
    assert not virtual.is_classical()


def test_oriented_smoothing():
    """Test oriented smoothing."""
    crossing = ClassicalCrossing(sign=1, south="s", north="n", west="w", east="e")
    smoothing = crossing.oriented_smoothing()
    
    assert smoothing == [["s", "e"], ["w", "n"]]
    assert isinstance(smoothing, list)
    assert isinstance(smoothing[0], list)


def test_disoriented_smoothing():
    """Test disoriented smoothing."""
    crossing = ClassicalCrossing(sign=1, south="s", north="n", west="w", east="e")
    smoothing = crossing.disoriented_smoothing()
    
    assert smoothing == [["s", "w"], ["e", "n"]]
    assert isinstance(smoothing, list)
    assert isinstance(smoothing[0], list)


def test_arcs_property():
    """Test the arcs property."""
    crossing = VirtualCrossing(south=1, north=2, west=3, east=4)
    arcs = crossing.arcs
    
    assert arcs == {'south': 1, 'north': 2, 'west': 3, 'east': 4}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])