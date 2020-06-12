"""Top-level functions for inference from causal diagrams."""

import networkx as nx
from oyster.utils.graph_utils import NA_pairs, De, Pa
from oyster.utils.set_utils import minimal_sets
from oyster.adjust import d_separated, d_separator_search
from oyster.viz.viz import draw

def implied_independencies(DAG):
    print('Implied independencies:')
    ind = {(X, Y): minimal_sets(d_separator_search(DAG, X, Y))
           for X, Y in NA_pairs(DAG)}
    for (X, Y), minsets in ind.items():
           print(f'{X} ⫫ {Y} | {minsets}')

def basis_set(DAG):
    for v in DAG.nodes:
        pa = Pa(DAG, v)
        nondesc = DAG.nodes - {v} - De(DAG, v) - pa 
        if nondesc: print(f'{v} ⫫ {nondesc} | {pa}')