# tests/test_gauss_parser.py
#  "O1-O2+O3+U1-O4-U3+U2+U4-"
from vkt.notation import parse_gauss_code
from vkt.visualization import plot_pre_rectangular_diagram

# Example: Trefoil knot
gauss_code = "O1-U2+O3-U4+O5-U6+O2+U1-O4+U3-O6+U5-"

# Parse and build diagram
diagram = parse_gauss_code(gauss_code)

print(diagram)
print(f"Crossings: {diagram.num_crossings}")
print(f"Arcs: {len(diagram.arcs)}")
print()

# Print each arc
for i, arc in enumerate(diagram.arcs):
    print(f"Arc {i}: crossing {arc.start_crossing}.{arc.start_direction} → "
          f"crossing {arc.end_crossing}.{arc.end_direction}")
    print(f"  Forward: {arc.is_forward()}, Backward: {arc.is_backward()}")
    print()

# Visualize
plot_pre_rectangular_diagram(diagram)