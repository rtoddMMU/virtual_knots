# src/vkt/notation/line_sweep.py

from typing import List, Dict, Any
from .arc import Arc

__all__ = ["find_virtual_crossings"]


def find_virtual_crossings(arcs: List[Arc]) -> List[Dict[str, Any]]:
    """Find all virtual crossings using a line sweep algorithm.
    
    Virtual crossings occur where a horizontal segment intersects
    a vertical segment from different arcs.
    
    Args:
        arcs: List of Arc objects
    
    Returns:
        List of dictionaries containing:
            - 'position': (x, y) coordinates of the virtual crossing
            - 'horizontal_arc': Arc with the horizontal segment
            - 'vertical_arc': Arc with the vertical segment
            - 'horizontal_segment': The horizontal Segment
            - 'vertical_segment': The vertical Segment
    """
    events = []
    
    # Create events for all segments
    for arc in arcs:
        for segment in arc.segments:
            if segment.is_horizontal():
                # Horizontal segment: single event at its y-coordinate
                x_min, x_max = segment.x_range()
                events.append({
                    'type': 'horizontal',
                    'y': segment.y,
                    'x_min': x_min,
                    'x_max': x_max,
                    'arc': arc,
                    'segment': segment
                })
            else:  # vertical
                # Vertical segment: start and end events
                y_min, y_max = segment.y_range()
                events.append({
                    'type': 'vertical_start',
                    'y': y_min,
                    'x': segment.x,
                    'y_max': y_max,
                    'arc': arc,
                    'segment': segment
                })
                events.append({
                    'type': 'vertical_end',
                    'y': y_max,
                    'x': segment.x,
                    'arc': arc,
                    'segment': segment
                })
    
    # Sort events by y-coordinate, then by type (process vertical_start before horizontal)
    def event_sort_key(e):
        # Primary: y coordinate
        # Secondary: type priority (vertical_start < horizontal < vertical_end)
        type_priority = {'vertical_start': 0, 'horizontal': 1, 'vertical_end': 2}
        return (e['y'], type_priority[e['type']])
    
    events.sort(key=event_sort_key)
    
    # Track active vertical segments
    active_verticals = []
    virtual_crossings = []
    
    for event in events:
        if event['type'] == 'vertical_start':
            active_verticals.append(event)
        
        elif event['type'] == 'vertical_end':
            # Remove this vertical from active list
            active_verticals = [
                v for v in active_verticals 
                if not (v['x'] == event['x'] and v['segment'] is event['segment'])
            ]
        
        elif event['type'] == 'horizontal':
            # Check intersection with all active verticals
            for v_event in active_verticals:
                # Check if vertical's x is within horizontal's x range
                if event['x_min'] <= v_event['x'] <= event['x_max']:
                    # Check if horizontal's y is within vertical's y range
                    if v_event['y'] <= event['y'] <= v_event['y_max']:
                        # Check that they're from different arcs
                        if event['arc'] is not v_event['arc']:
                            virtual_crossings.append({
                                'position': (v_event['x'], event['y']),
                                'horizontal_arc': event['arc'],
                                'vertical_arc': v_event['arc'],
                                'horizontal_segment': event['segment'],
                                'vertical_segment': v_event['segment']
                            })
    
    return virtual_crossings