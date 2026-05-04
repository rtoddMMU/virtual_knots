# tests/test_virtual_tangle.py

from vkt.core import ClassicalCrossing, VirtualCrossing, VirtualTangle

def test_basic_tangle():
    """Test basic VirtualTangle functionality."""
    tangle = VirtualTangle()
    
    # Create crossings
    c0 = ClassicalCrossing(sign=1)
    c1 = ClassicalCrossing(sign=-1)
    c2 = VirtualCrossing()
    
    # Add to tangle
    tangle.add_crossing(c0)
    tangle.add_crossing(c1)
    tangle.add_crossing(c2)
    
    print(f"Created: {tangle}")
    print(f"Number of crossings: {tangle.num_crossings}")
    print(f"Classical: {tangle.num_classical_crossings}")
    print(f"Virtual: {tangle.num_virtual_crossings}")
    
    # Add arcs
    tangle.add_arc(c0, 'east', c1, 'south')
    tangle.add_arc(c1, 'north', c2, 'west')
    tangle.add_arc(c2, 'east', c0, 'south')
    
    print(f"\nNumber of arcs: {len(tangle.arcs)}")
    print(f"Is closed: {tangle.is_closed()}")
    
    # Test traversal
    path = tangle.traverse_strand(c1, 'south')
    print(f"\nTraversal from c1.south: {len(path)} steps")

if __name__ == "__main__":
    test_basic_tangle()