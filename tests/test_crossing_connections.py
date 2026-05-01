# tests/test_crossing_connections.py

from vkt.core import ClassicalCrossing, VirtualCrossing

# Create crossings
c0 = ClassicalCrossing(sign=1)
c1 = ClassicalCrossing(sign=-1)
c2 = VirtualCrossing()

print(f"Created: {c0}, {c1}, {c2}")

# Connect them
c0.set_successor('east', c1, 'south')
c1.set_successor('north', c2, 'west')
c2.set_successor('east', c0, 'south')

# Check connections
print(f"\n{c0}.east_successor = {c0.east_successor}")
print(f"{c1}.south_predecessor = {c1.south_predecessor}")
print(f"{c1}.north_successor = {c1.north_successor}")
print(f"{c2}.west_predecessor = {c2.west_predecessor}")

# Test disconnection
c0.disconnect_successor('east')
print(f"\nAfter disconnecting {c0}.east:")
print(f"{c0}.east_successor = {c0.east_successor}")
print(f"{c1}.south_predecessor = {c1.south_predecessor}")