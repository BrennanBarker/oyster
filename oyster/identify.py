"""Algorithms for determining identifiability of causal diagrams."""

from oyster.utils.graph_utils import (An, Ch, De, observable_nodes, 
                                      observable_pairs, ancestral_graph, 
                                      do_X)
from oyster.utils.set_utils import _set
from oyster.structures import paths, c_components, has_confounded_path


def is_identifiable_single_x(G, X, Y):
    """Return if the causal effect of singletons X and Y in G
    is identifiable based on the algorithm in Tian and Pearl 2002."""
    return not any(
        [has_confounded_path(ancestral_graph(G, Y), X, ChX) 
         for ChX in Ch(G, X)])

def is_identifiable(G, X, Y, print_hedge=False):
    """Return if the causal effect of variables X on variables Y in G
    is identifiable based on algorithm ID in Shpitser and Pearl 2008."""
    C = c_components
    X = _set(X)
    Y = _set(Y)
    V = observable_nodes(G)
    Gprime = G.subgraph(G.nodes - X)
    
    if X == set(): return True # Line 1
    
    if V - An(G, Y) - Y != set(): # Line 2
        return is_identifiable(ancestral_graph(G, Y), X & An(G, Y), Y)
    
    W = (V - X) - An(do_X(G, X), Y) - Y 
    if W != set(): return is_identifiable(G, X|W, Y) # Line 3

    Sk = C(Gprime)
    if len(Sk) > 1: # Line 4
        return all(is_identifiable(G, V - S, S) for S in Sk)
    else: 
        S = Sk[0]
        if any(c == V for c in C(G)): # Line 5
            if print_hedge: print(f'Hedge at ({V}, {V&S})')
            return False 
        if S in C(G): # Line 6
            return True
        else: # Line 7
            Sprime = [c for c in C(G) if S < c][0]
            return is_identifiable(G.subgraph(Sprime | Y), X & Sprime, Y) # Should subgraph really include Y?