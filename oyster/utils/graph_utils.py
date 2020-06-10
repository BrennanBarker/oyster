"""Utility functions for working with graphical causal models."""
import networkx as nx
from oyster.utils.set_utils import _set
from itertools import chain, combinations


### Wrappers ###
def _vectorize_union(f):
    """Vectorize a function f(DAG, node) for one or more nodes, return unified set."""
    def wrapper(DAG, nodes): 
        return set.union(set(), *(set(f(DAG, node)) for node in _set(nodes)))
    return wrapper

def _vectorize_intersection(f):
    """Vectorize a function f(DAG, node) for one or more nodes, return set intersection."""
    def wrapper(DAG, nodes):
        return set.intersection(*(set(f(DAG, node)) for node in _set(nodes)))
    return wrapper


### Graph Comparisons ###
def equal(G, F):
    return (G.nodes() == F.nodes() and G.edges() == F.edges())


### Node Selectors ###
def De(DAG, nodes):
    """Set of the descendants of nodes in DAG."""
    return _vectorize_union(nx.descendants)(DAG, nodes)

def An(DAG, nodes):
    """Set of the ancestors of nodes in DAG."""
    return _vectorize_union(nx.ancestors)(DAG, nodes)

def Ch(DAG, nodes):
    """Set of the children of nodes in DAG."""
    def children(DAG, node): return DAG.successors(node) 
    return _vectorize_union(children)(DAG, nodes)

def Pa(DAG, nodes):
    """Set of the parents of nodes in DAG."""
    def parents(DAG, node): return DAG.predecessors(node) 
    return _vectorize_union(parents)(DAG, nodes)

def MB(DAG, nodes): 
    """Markov Blanket of a node in DAG.
    The set of parents, children, and parents of children."""
    def mb(DAG, node): 
        return set(Pa(DAG, node) | Ch(DAG, node) | Pa(DAG, Ch(DAG, node))) - {node}
    return _vectorize_union(mb)(DAG, nodes)

def NA(DAG, nodes):
    """Set of non-adjacent nodes to given nodes in DAG."""
    def na(DAG, node): return DAG.nodes - DAG.to_undirected()[node] - {node}
    return _vectorize_intersection(na)(DAG, nodes)


# Observable and hidden elements:
def hidden_edges(DAG):
    """Return a list of the hidden edges in DAG."""
    return [(u,v,d) for u,v,d in DAG.edges(data=True) 
            if d.get('hidden') == True]

def hidden_nodes(DAG):
    """Return a set of the hidden nodes in DAG."""
    #return {u for u,v,d in DAG.edges(data=True) if (d.get('hidden') == True} 
    # HACK: requires hidden nodes named 'U'
    return {node for node in DAG.nodes() if 'U' in node}

def observable_nodes(DAG):
    """Return a set of the observable nodes in DAG."""
    return DAG.nodes() - hidden_nodes(DAG)


### Node Pairings ###
def are_nonadjacent(G, nodes):
    for node in nodes:
        return all(other not in G.to_undirected()[node]
                   for other in _set(nodes) - _set(node))

def NA_pairs(DAG):
    "List of all nonadjacent pairs of nodes in DAG."
    return [set((X, Y)) for X,Y in combinations(DAG.nodes, 2)
            if Y not in set(DAG.to_undirected()[X])]

def observable_pairs(DAG):
    """An iterator of observable pairs of nodes in DAG."""
    return combinations(observable_nodes(DAG), 2)


### Subgraphs ###
def ancestral_graph(DAG, nodes):
    """A subgraph of the DAG containing only the specified nodes and their ancestors."""
    return DAG.subgraph(An(DAG, nodes) | set(nodes))

from networkx.algorithms.moral import moral_graph

def backdoor_graph(DAG, X):
    """Return the subgraph of DAG with arrows from nodes X removed."""
    return nx.subgraph_view(DAG, filter_edge=lambda a, b: a not in _set(X))

def do_X(DAG, X):
    """Return the subgraph of DAG with arrows into nodes X removed."""
    return nx.subgraph_view(DAG, filter_edge=lambda a, b: b not in _set(X))


### Graph Transformations ###
def skeleton(DAG):
    """Return the DAG skeleton."""
    return DAG.to_undirected()

def bidirected(DAG):
    """Return a graph with an opposing edge added for every edge in DAG."""
    return skeleton(DAG).to_directed()

def edges_removed(DAG, edges):
    """Return a view of the DAG with given edges removed."""
    def not_in_edges(u,v): return (u,v) not in edges
    return nx.subgraph_view(DAG, filter_edge=not_in_edges)


### Partial DAG (pDAG) Functions ###
def reversible_edges(pDAG):
    """A list of the bidirected edges in pDAG.
    These edges have not been definitively oriented."""
    return [(h, t) for (h, t) in pDAG.edges() if (t, h) in pDAG.edges()]

def compelled_edges(pDAG):
    """A list of the definitively oriented (or "compelled") edges in pDAG."""
    return [(h, t) for (h, t) in pDAG.edges() if (t, h) not in pDAG.edges()]


### Causal Structures ###
def colliders(G):
    cols = {}
    for node in G.nodes:
        parents = Pa(G, node)
        if len(parents) > 1:
            cols[node] = list(combinations(parents, 2))
    return cols

def v_structures(DAG):
    return {collider:[set(pair) 
                      for pair in parent_pairs 
                      if are_nonadjacent(DAG, pair)]
            for collider, parent_pairs in colliders(DAG).items()}