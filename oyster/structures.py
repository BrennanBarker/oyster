"""Definitions of causal structures in causal diagrams."""

import networkx as nx
from oyster.utils.graph_utils import observable_nodes, observable_pairs, De

def paths(DAG, X, Y, directed=False):
    """Return a generator of all paths in DAG from X to Y.
    """
    def reorient_path(DAG, path_list):
        """Map a list of nodes specifying an undirected path back to a DAG 
        to recover the original edge orientation and data."""
        pairs = zip(path_list, path_list[1:])
        edges = []
        for (u,v) in pairs:
            if DAG.has_edge(u,v): edges.append((u,v, DAG.get_edge_data(u,v)))
            else: edges.append((v,u, DAG.get_edge_data(v,u)))
        return nx.DiGraph(edges)
    G = DAG if directed else nx.to_undirected(DAG) 
    paths = nx.all_simple_paths(G, X, Y) 
    return (reorient_path(DAG, path) for path in paths)

def root_set(DAG):
    """The root set of the DAG, i.e. nodes without children.
    Note that this definition, while consistent with Shpitser 2008,
    is reversed from most literature."""
    return {X for X in DAG.nodes() if De(DAG, X) == set()}

def is_forest(DAG):
    """Return if DAG is a tree defined as in Shiptser 2008:
    
    A graph G such that each vertex has at most one child, 
    (ignoring hidden edges) is called a forest."""
    return max(
        [out_degree for (node, out_degree) in
         DAG.subgraph(observable_nodes(DAG)).out_degree()]
    ) <= 1

def is_tree(DAG):
    """Return if DAG is a tree defined according to Shiptser 2008:
    
    A graph G such that each vertex has at most one child, 
    and only one vertex (called the root) has no children 
    is called a tree."""
    return is_forest(DAG) and len(root_set(DAG)) == 1

def is_confounded(path):
    """
    path is assumed to be an nx.DiGraph representing a path
    A path where all directed arrowheads point at observable nodes, 
    and never away from observable nodes is called a confounded path."""
    arrowheads_in, arrowheads_out = [], []
    for u,v in path.edges():
        arrowheads_in.append(v)
        arrowheads_out.append(u)
    return (all([i in observable_nodes(path) for i in arrowheads_in]) and
        not any([o in observable_nodes(path) for o in arrowheads_out]))

def has_confounded_path(DAG, X, Y):
    "Return if there is at least one confounded path between X and Y in DAG."
    return any((is_confounded(path) for path in paths(DAG, X, Y)))

def is_c_component(DAG):
    """Return if the graph is a c-component.
    From Shpitser 2008: a graph where any pair of observable 
    nodes is connected by a confounded path is called a 
    c-component (confounded component)."""
    return all((has_confounded_path(DAG, u, v) for u,v in observable_pairs(DAG)))
        
def c_components(DAG):
    """Return a list of the maximal c-component node sets in DAG."""
    G = nx.Graph(); 
    G.add_nodes_from(observable_nodes(DAG))
    G.add_edges_from([(u,v) for u,v in observable_pairs(DAG) if 
                      has_confounded_path(DAG, u, v)])
    return list(nx.connected_components(G))

def is_c_tree(DAG):
    return is_c_component(DAG) and is_tree(DAG)

def is_c_forest(DAG):
    return is_c_component(DAG) and is_forest(DAG)