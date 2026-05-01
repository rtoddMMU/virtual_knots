# src/vkt/visualization/plot_diagram.py

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from ..notation.pre_rectangular_diagram import PreRectangularDiagram

__all__ = ["plot_pre_rectangular_diagram"]


def plot_pre_rectangular_diagram(diagram: PreRectangularDiagram, figsize=(10, 10)):
    """Plot a PreRectangularDiagram.
    
    Args:
        diagram: PreRectangularDiagram to plot
        figsize: Figure size tuple
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot arcs FIRST (so crossings draw on top)
    for arc in diagram.arcs:
        for segment in arc.segments:
            x_coords = [segment.start[0], segment.end[0]]
            y_coords = [segment.start[1], segment.end[1]]
            
            # All arcs same color, solid lines
            ax.plot(x_coords, y_coords, color='black', linestyle='-', 
                    linewidth=1.5, alpha=0.8, zorder=5)
    
    # Plot crossings as actual crossing diagrams with over/under
    for i, crossing in enumerate(diagram.classical_crossings):
        points = diagram.get_crossing_points(i)
        
        # Get the four cardinal points
        south = points['south']
        north = points['north']
        west = points['west']
        east = points['east']
        
        # Get over and under strands
        over_strand = crossing.over_strand  # Returns [arc1, arc2]
        under_strand = crossing.under_strand
        
        # Determine which is vertical and which is horizontal
        # over_strand and under_strand contain the arc endpoints
        # For positive crossing: over = [west, east], under = [south, north]
        # For negative crossing: over = [south, north], under = [west, east]
        
        if crossing.sign == 1:
            # Positive: over is horizontal (west-east), under is vertical (south-north)
            over_start, over_end = west, east
            under_start, under_end = south, north
        else:
            # Negative: over is vertical (south-north), under is horizontal (west-east)
            over_start, over_end = south, north
            under_start, under_end = west, east
        
        # Draw UNDER strand with a gap in the middle
        center = diagram.get_crossing_position(i)
        gap_size = 0.4
        
        # Calculate the gap points
        if under_start[0] == under_end[0]:  # Vertical under-strand
            # Draw from start to gap, then from gap to end
            gap_bottom = (center[0], center[1] - gap_size)
            gap_top = (center[0], center[1] + gap_size)
            
            ax.plot([under_start[0], gap_bottom[0]], [under_start[1], gap_bottom[1]], 
                    'black', linewidth=2, zorder=10)
            ax.plot([gap_top[0], under_end[0]], [gap_top[1], under_end[1]], 
                    'black', linewidth=2, zorder=10)
        else:  # Horizontal under-strand
            # Draw from start to gap, then from gap to end
            gap_left = (center[0] - gap_size, center[1])
            gap_right = (center[0] + gap_size, center[1])
            
            ax.plot([under_start[0], gap_left[0]], [under_start[1], gap_left[1]], 
                    'black', linewidth=2, zorder=10)
            ax.plot([gap_right[0], under_end[0]], [gap_right[1], under_end[1]], 
                    'black', linewidth=2, zorder=10)
        
        # Draw OVER strand as an arrow (continuous, no gap)
        arrow = FancyArrowPatch(
            over_start, over_end,
            arrowstyle='->', mutation_scale=20,
            linewidth=2, color='black', zorder=15
        )
        ax.add_patch(arrow)
        
        # Optional: Add small label near crossing
        # Uncomment if you want to see crossing numbers
        # sign_str = '+' if crossing.sign == 1 else '-'
        # ax.text(center[0] + 0.5, center[1] + 0.5, f"{i}{sign_str}", 
        #         fontsize=8, color='gray', zorder=20)
    
    # Plot y = x + 1 line (separator) - optional, can remove if too busy
    x_min = -2
    x_max = 4 * diagram.num_crossings + 2
    ax.plot([x_min, x_max], [x_min + 1, x_max + 1], 
            'gray', linestyle='--', alpha=0.3, linewidth=1, zorder=1)
    
    # Formatting
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle=':', linewidth=0.5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title(f'Rectangular Diagram: {diagram.num_crossings} crossings', fontsize=14)
    
    plt.tight_layout()
    plt.show()