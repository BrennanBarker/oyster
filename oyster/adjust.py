"""Functions for determining d-separation and adjustment sets."""

import networkx as nx
from oyster.utils.set_utils import powerset, minimal_sets, _set 
from oyster.utils.graph_utils import An, De, Pa, Ch, ancestral_graph, moral_graph, backdoor_graph

# TODO: powerset search is probably prohibitive for moderately-sized graphs, might need to sized bsed on some number

### D-separation ###
def d_separated(DAG, X, Y, Z):
    """Return if Z d-separates X and Y in the DAG."""
    X, Y, Z = _set(X), _set(Y), _set(Z)
    ancestral = ancestral_graph(DAG, X|Y|Z) # Take ancestral graph of nodes in question..
    moral = moral_graph(ancestral) # Moralize & disorient...
    moral_without_givens = moral.subgraph(moral.nodes - Z) # Remove givens...
    # Any paths between X and Y?
    return not any([nx.has_path(moral_without_givens, x, y) 
                    for x in X for y in Y])

def d_separator_search(DAG, X, Y):
    """Return d_separators for X and Y in DAG."""
    return [set(z) for z in powerset(DAG.nodes - _set(X) - _set(Y))
            if d_separated(DAG, X, Y, z)]


### Back-Door Criterion ###
def meets_backdoor_criterion(DAG, X, Y, Z):
    """Return if Z satisfies the backdoor criterion from X to Y in DAG."""
    return all((
        # i) No node in Z is a descendant of X
        not De(DAG, X) & _set(Z), 
        # ii) Z d-separates all backdoor paths between X and Y
        d_separated(backdoor_graph(DAG, X), X, Y, Z)))

def backdoor_criterion_search(DAG, X, Y):
    """Return all sets of nodes satisfying the backdoor criterion from X to Y in DAG."""
    possible_nodes = DAG.nodes() - De(DAG, X) - _set(X) - _set(Y)
    return [set(z) for z in powerset(possible_nodes)
            if meets_backdoor_criterion(DAG, X, Y, z)]


### Front-Door Criterion ###
def meets_frontdoor_criterion(DAG, X, Y, Z):
    """Return if Z satisfies the frontdoor criterion for X on Y in DAG."""
    return all((
        # i) Z intercepts all directed paths from X to Y
        not nx.has_path(DAG.subgraph(DAG.nodes - Z), X, Y),
        # ii) All backdoor paths from X to Z are blocked by the empty set
        d_separated(backdoor_graph(DAG, X), X, Z, set()),
        # iii) All backdoor paths from Z to Y are blocked by X
        d_separated(backdoor_graph(DAG, Z), Z, Y, X)))

def frontdoor_criterion_search(DAG, X, Y):
    """Return all sets of nodes that satisfy the backdoor criterion from X to Y in DAG."""
    return [set(Z) for Z in powerset(DAG.nodes - _set(X) - _set(Y)) 
            if meets_frontdoor_criterion(DAG, X, Y, Z)]


### Adjusters
def minimal_adjustment_sets(DAG, X, Y):
    """Return the minimal sets of nodes that meet the backdoor criterion for X on Y in DAG."""
    return minimal_sets(backdoor_criterion_search(DAG, X, Y))

def specific_adjustment_sets(DAG, X, Y, Z):
    """Return minimal sets of variables including Z that meet the backdoor criterion (z-specific effects)."""
    return [s for s in backdoor_criterion_search(DAG, X, Y) if Z in s]

def adjusters(G,X,Y, exclude=[]):
    """Return the minimal sets of adjusters capable of 
    determining the causal effect of X on Y in the causal
    model specified by DAG."""
    def no_excludeds(adj_set): return not set(exclude) & adj_set
    iden = identifiable_single_X(G, X, Y)
    bd_sets = [set(S) for S in backdoor_criterion_search(G, X, Y) 
               if no_excludeds(S)]
    fd_sets = [set(S) for S in frontdoor_criterion_search(G, X, Y) 
               if no_excludeds(S)]
    
    adj = {
        'identifiable': iden,
        'back-door adjustment sets': bd_sets if bd_sets else None,
        'front-door adjustment sets': fd_sets if fd_sets else None,
    }
    return adj