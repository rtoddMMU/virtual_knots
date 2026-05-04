# src/vkt/algorithms/planarity_test.py

import networkx as nx
from typing import List, Tuple, Optional
from ..core import ClassicalCrossing

__all__ = ["is_classical_knot", "check_classical_planarity"]


def crossings_to_graph(crossings: List[ClassicalCrossing]) -> nx.Graph:
    """Convert a list of classical crossings to an undirected 4-regular graph.
    
    Ignores over/under information - just looks at the graph structure.
    
    Args:
        crossings: List of ClassicalCrossing objects with successor/predecessor set
        
    Returns:
        NetworkX Graph representing the knot diagram topology
    """
    G = nx.Graph()
    
    # Add all crossings as nodes
    for crossing in crossings:
        G.add_node(crossing.id)
    
    # Add edges based on successor relationships
    for crossing in crossings:
        # North successor
        if crossing.north_successor:
            next_crossing, _ = crossing.north_successor
            G.add_edge(crossing.id, next_crossing.id)
        
        # East successor
        if crossing.east_successor:
            next_crossing, _ = crossing.east_successor
            G.add_edge(crossing.id, next_crossing.id)
    
    return G


def is_classical_knot(crossings: List[ClassicalCrossing]) -> bool:
    """Test if a collection of classical crossings can form a classical knot.
    
    A knot is classical (non-virtual) if its underlying 4-regular graph is planar.
    
    Args:
        crossings: List of ClassicalCrossing objects
        
    Returns:
        True if the knot can be drawn without virtual crossings
    """
    G = crossings_to_graph(crossings)
    return nx.is_planar(G)


def check_classical_planarity(
    crossings: List[ClassicalCrossing],
    return_embedding: bool = False
) -> Tuple[bool, Optional[nx.PlanarEmbedding]]:
    """Check if crossings form a classical knot and optionally return embedding.
    
    Args:
        crossings: List of ClassicalCrossing objects
        return_embedding: If True, return the planar embedding when planar
        
    Returns:
        (is_classical, embedding) tuple where:
        - is_classical: True if knot is classical (planar)
        - embedding: PlanarEmbedding if planar and requested, else None
    """
    G = crossings_to_graph(crossings)
    is_planar, certificate = nx.check_planarity(G)
    
    if is_planar and return_embedding:
        return True, certificate
    else:
        return is_planar, None