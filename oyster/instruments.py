from oyster.adjust import d_separated, d_separator_search
from oyster.utils.graph_utils import do_X, De, observable_nodes, hidden_nodes
from oyster.utils.set_utils import _set

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
        poss_Ws = [W for W in d_separator_search(do_X(DAG, X), Z, Y) 
                   if not (hidden_nodes(DAG) | _set(X)) & W] 
        for W in poss_Ws:
            if not d_separated(DAG, Z, X, W) and not W & DeY:
                ivs.append((Z, W))
             
    if ivs:
        print('Instrumental Variables:')
        for Z, W in ivs:
            print(f'{Z} | {W}' if W else Z)
    else:
        print('No Conditional instrumental variables')
    
                    

        
        