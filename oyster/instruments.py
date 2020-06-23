from oyster.adjust import d_separated, d_separator_search
from oyster.utils.graph_utils import (do_X, De, An, 
                                      observable_nodes, hidden_nodes, 
                                      backdoor_graph, edges_removed,
                                      moral_graph, ancestral_graph)
from oyster.structures import paths
from oyster.utils.set_utils import _set, minimal_sets


### Exhaustive Instrumental Variable Search ###

def is_instrumental_variable(DAG, X, Y, Z, W=set()):
    """Return whether Z is an instrumental variable
    for the effect of X on Y in DAG, potentially
    conditional on W.
    
    From the graphical definition in Pearl 2009."""
    return all((
        d_separated(do_X(DAG, X), Z, Y, W),
        not d_separated(DAG, Z, X, W),
        not _set(W) & De(DAG, Y) # no descendants of Y in W
    ))

def instrumental_variable_search(DAG, X, Y):
    # for all variables in DAG - X - Y...
        # unconditional instrument?
        # if so, stop?
        # if not, intersection of d_separator_search(do_X(DAG, X), Z, Y)
        # and d_separator_search(DAG, Z, X)
        # return any not decendants of Y
    DeY = De(DAG, Y)
    potential_Zs = observable_nodes(DAG) - _set(X) - _set(Y)
    
    ivs = []
    for Z in potential_Zs:
        poss_Ws = [W for W in d_separator_search(backdoor_graph(DAG, X), Z, Y) 
                   if not (hidden_nodes(DAG) | _set(X)) & W] 
        Ws = [W for W in poss_Ws
              if not d_separated(DAG, Z, X, W) and not W & DeY]
        if Ws: ivs.append((Z, minimal_sets(Ws)))
             
    return ivs

### Ancestral Instrument Search ###
# Faster, guaranteed to find an instrument if one exists, 
# but not guaranteed to find all instruments or minimal instrumentalizing sets

def is_ancestral_instrument(DAG, X, Y, Z, W=set()):
    """Return whether Z is an ancestral instrument
    relative to X->Y in DAG,  X on Y in DAG, 
    conidtional on W.
    
    From Definition 3.3 in van der Zander 2015.
    
    Note van der Zander's assumption that DAG 
    includes an edge X->Y, so not sure this covers all
    cases."""
    Gc = edges_removed(DAG, [(X, Y)])
    return all((
        not d_separated(DAG, Z, X, W),
        d_separated(Gc, Z, Y, W),
        not _set(W) & De(DAG, Y),
        (bool(_set(W) & (oy.An(DAG, Y) | oy.An(DAG, Z))) 
         if _set(W) else True)
    ))
    
def nearest_separator(DAG, Y, Z):
    M = observable_nodes(DAG)
    moral = moral_graph(ancestral_graph(DAG, [Y, Z]))
    
    W = set()
    for path in paths(moral, Y, Z):
        pi = path.nodes
        Vs = list(pi)[1:-1]

        if all((
            len(pi) > 2, # Vs other than Y,Z
            not W & pi, # pi not blocked by W
            set(Vs) & M # at least one observable V
        )):
            W |= _set(next(V for V in Vs if V in M))
            
    if d_separated(DAG, Z, Y, W):
        return(W)
    else:
        return('⊥') # Separator not found

def ancestral_instrument(DAG, X, Y, Z):
    Gc = edges_removed(DAG, [(X, Y)])
    W = nearest_separator(Gc, Y, Z)
    
    if W == '⊥': return '⊥'
    if W & De(DAG, Y) != set(): return '⊥'
    if _set(X) < W: return '⊥'  
    return W if not d_separated(Gc, Z, X, W) else '⊥'
    
def ancestral_instrument_search(DAG, X, Y):
    possible_instruments = DAG.nodes - _set(X) - _set(Y) - De(DAG, Y)
    ivs = []
    for Z in possible_instruments:
        W = ancestral_instrument(DAG, X, Y, Z)
        if W != '⊥':
            ivs.append((Z, W))
    return ivs
    

def print_ivs(ivs):
    if ivs:
        print('Instrumental Variables:')
        for Z, Ws in ivs:
            print(f'{Z} | {",".join([str(W) for W in Ws])}' 
                  if Ws != [set()] else Z)
    else:
        print('No instrumental variables')
    

                    

        
        