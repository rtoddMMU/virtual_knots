from vkt.notation import create_arc_with_routing

# Create a forward arc from crossing 1 to crossing 3
arc = create_arc_with_routing(3, 1, 'east', 'south')

print(arc)
print(f"Number of segments: {len(arc.segments)}")
for i, seg in enumerate(arc.segments):
    print(f"  Segment {i}: {seg}")