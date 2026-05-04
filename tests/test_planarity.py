# Example: Test if a knot from Gauss code is classical

from vkt.notation import GaussCode
from vkt.core import VirtualTangle

# Parse a Gauss code
gauss = GaussCode.from_string("O1-U2+O3-U1+O2-U3+")
diagram = gauss.to_rectangular_diagram()
knot = VirtualTangle.from_rectangular_diagram(diagram)

# Test if it's classical
if knot.is_classical():
    print("This is a CLASSICAL knot!")
    print("It can be drawn without virtual crossings.")
    
    # Get the planar embedding
    embedding = knot.get_planar_embedding()
    print(f"Planar embedding: {embedding.get_data()}")
else:
    print("This is a VIRTUAL knot!")
    print("It requires virtual crossings.")