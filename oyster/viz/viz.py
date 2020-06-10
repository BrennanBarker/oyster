"""Visualization functions for graphical causal models."""

import networkx as nx
from oyster.structures import paths
from oyster.utils.graph_utils import ancestral_graph, moral_graph
from oyster.utils.set_utils import _set
from oyster.equivalence import dag_to_cpdag, equivalence_class_size
import oyster.example.graphs as ex
from itertools import chain
import matplotlib.pyplot as plt

def print_path(path, start):
    """Pretty-prints a path from an nx.DiGraph"""
    ppstr = start
    head = start
    for (s, t) in path.edges():
        if s == head:
            ppstr += f' -> {t}'
            head = t
        else:
            ppstr += f' <- {s}'
            head = s
    print(ppstr)

def print_paths(DAG, start, finish, directed=False):
    for path in paths(DAG, start, finish, directed=directed): 
        print_path(path, start='X') 

def draw(G, pos=None, title=None, ax=None, 
         _show_axis_lines=False):
    """A simple wrapper for drawing graphs."""
    if not ax: 
        fig, ax = plt.subplots()    
    ax.set_title(title)
    ax.axis(_show_axis_lines)
    #ax.set_aspect('equal', 'box')
    if not pos: # If pos not specified...
        pos = ex.pos.get(G, None) # Try to find a matching example
    if title:
        plt.title=title
    nx.draw_networkx(G, pos, with_labels=True, 
            node_color='lightgray', font_color='black', ax=ax)

def d_sep_graphs(DAG, X, Y, Z, pos=None):
    """Visualize d-separation."""
    X, Y, Z = _set(X), _set(Y), _set(Z) 
    a = ancestral_graph(DAG, X|Y|Z) 
    m = moral_graph(a)
    mwoz = m.subgraph(m.nodes - Z) 
    
    if not pos: # If pos not specified...
        pos = ex.pos.get(DAG, None) # Try to find a matching example

    f, axs = plt.subplots(1,3, constrained_layout=True)
    draw(a, title='Ancestral', pos=pos, ax=axs[0], _show_axis_lines=True)
    draw(m, title='Moral', pos=pos, ax=axs[1], _show_axis_lines=True)
    draw(mwoz, title='Without Givens', pos=pos, ax=axs[2], _show_axis_lines=True)
        
def draw_cpdag(DAG, pos):
    plt.subplot(1,2,1); plt.title('DAG')
    oy.draw(DAG, pos=pos)
    plt.subplot(1,2,2); plt.title('CPDAG')
    oy.draw(dag_to_cpdag(DAG), pos=pos)
    print(f'equivalent dags: {equivalence_class_size(DAG)}')

def gv_draw(G, pos=None, filename='oyster/viz/images/graph.png', 
            font_color='black', 
            node_style='solid', hidden_node_style='solid',
            node_color='black', hidden_node_color='black',
            edge_color='black', hidden_edge_color='black',
            edge_style='solid', hidden_edge_style='dashed'):
    """Draw using Graphviz to write an image (requires pygraphviz)."""
    import pygraphviz as pgv
    A = nx.nx_agraph.to_agraph(G)
    
    A.node_attr['fontname']='helvetica'
    A.node_attr['fontcolor']=font_color  
    A.node_attr['shape'] = 'circle'
    A.node_attr['fixedsize'] = 'true'
    A.node_attr['fontsize'] = 8

    for node in A.nodes(): 
        node.attr['width'] = .2
        if pos and pos.get(node.name):
                node.attr['pos'] = f'{pos[node.name][0]},{pos[node.name][1]}!'
        node.attr['color'] = hidden_node_color if node.attr.get('hidden') else node_color
        node.attr['style'] = hidden_node_style if node.attr.get('hidden') else node_style
        
    for edge in A.edges():
        edge.attr['arrowsize'] = .75
        edge.attr['color'] = hidden_edge_color if edge.attr.get('hidden') else edge_color
        edge.attr['style'] = hidden_edge_style if edge.attr.get('hidden') else edge_style

    A.draw(filename, prog='neato')
    return filename