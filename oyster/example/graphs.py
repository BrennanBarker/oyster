"""Example graphs from causal inference literature."""

import networkx as nx
from oyster.diagram import CausalDiagram

# Graphs
mit = nx.DiGraph([('A', 'C'), ('B', 'C'), ('C', 'D'),
                  ('C', 'E'), ('D', 'F'), ('F', 'G'),])

# Causal Inference in Statistics: A Primer
primer = {
    'fig1_8': CausalDiagram([('X', 'W'), ('X', 'Y'), ('W', 'Y'), ('W', 'Z'), ('Y', 'T'), ('Y', 'Z'), ('Z', 'T')]),
    'fig2_5': CausalDiagram([('X', 'R'), ('R', 'S'), ('S', 'T'), ('U', 'T'), ('V', 'U'), ('V', 'Y')]),
    'fig2_6': CausalDiagram([('X', 'R'), ('R', 'S'), ('S', 'T'), ('T', 'P'), ('U', 'T'), ('V', 'U'), ('V', 'Y')]),
    'fig2_9': nx.DiGraph([('X', 'W'), ('W', 'Y'), ('Z1', 'X'), 
                          ('Z1', 'Z3'), ('Z2', 'Z3'), ('Z2', 'Y'), 
                          ('Z3', 'X'), ('Z3', 'Y')]),
    'fig3_7': nx.DiGraph([('E', 'X'), ('E', 'Z'), ('Z', 'X'), ('X', 'Y'),
                          ('Z', 'Y'), ('A', 'Z'), ('A', 'Y')]),
    'fig3_8': nx.DiGraph([('B', 'A'), ('B', 'Z'), ('C', 'Z'), ('C', 'D'),
                          ('A', 'X'), ('Z', 'X'), ('Z', 'Y'), ('D', 'Y'),
                          ('X', 'W'), ('W', 'Y')]),
}

# The Book of Why
bow = {
    'fig4_7': nx.DiGraph([('A', 'X'), ('A', 'B'), ('B', 'X'), ('C', 'B'), 
                          ('C', 'E'), ('C', 'Y'), ('D', 'C'), ('D', 'A'), 
                          ('E', 'X'), ('E', 'Y'), ('F', 'C'), ('F', 'X'), 
                          ('F', 'Y'), ('G', 'X'), ('G', 'Y'), ('X', 'Y')]),
}

# Shpitser and Pearl 2008
sp08 = {
    'fig1': {
        'a': nx.DiGraph([('X', 'Y'), 
                         ('U', 'X', {'hidden':True}), ('U', 'Y', {'hidden':True})]),
        'b': nx.DiGraph([('X', 'Z'), ('Z', 'Y'), 
                         ('U', 'X', {'hidden':True}), ('U', 'Z', {'hidden':True})]),
        'c': nx.DiGraph([('X', 'Z'), ('X', 'Y'), ('Z', 'Y'),
                         ('U', 'X', {'hidden':True}), ('U', 'Z', {'hidden':True})]),
        'd': nx.DiGraph([('X', 'Y'), ('Z', 'Y'),
                         ('U1', 'X', {'hidden':True}), ('U1', 'Z', {'hidden':True}),
                         ('U2', 'Z', {'hidden':True}), ('U2', 'Y', {'hidden':True})]),
        'e': nx.DiGraph([('X', 'Y'), ('Z', 'X'),
                         ('U1', 'X', {'hidden':True}), ('U1', 'Z', {'hidden':True}),
                         ('U2', 'Z', {'hidden':True}), ('U2', 'Y', {'hidden':True})]),
        'f': nx.DiGraph([('X', 'Z'), ('Z', 'Y'),
                         ('U1', 'X', {'hidden':True}), ('U1', 'Y', {'hidden':True}),
                         ('U2', 'Z', {'hidden':True}), ('U2', 'Y', {'hidden':True})]),
        'g': nx.DiGraph([('X', 'Z1'), ('Z1', 'Y'), ('Z2', 'Y'),
                         ('U1', 'X', {'hidden':True}), ('U1', 'Z2', {'hidden':True}),
                         ('U2', 'Z1', {'hidden':True}), ('U2', 'Z2', {'hidden':True})]),
        'h': nx.DiGraph([('X', 'W'), ('W', 'Y'), ('Z', 'X'),
                         ('U1', 'X', {'hidden':True}), ('U1', 'Y', {'hidden':True}),
                         ('U2', 'X', {'hidden':True}), ('U2', 'Z', {'hidden':True}),
                         ('U3', 'W', {'hidden':True}), ('U3', 'Z', {'hidden':True}),
                         ('U4', 'Y', {'hidden':True}), ('U4', 'Z', {'hidden':True})]),
    },
    'fig2': {
        'a': nx.DiGraph([('X', 'Y')]),
        'b': nx.DiGraph([('X', 'Z'), ('X', 'Y'), ('Z', 'Y'),
                         ('U', 'Y', {'hidden':True}), ('U', 'Z', {'hidden':True})]),
        'c': nx.DiGraph([('X', 'Y'), ('Z', 'X'), ('Z', 'Y'), 
                         ('U', 'Z', {'hidden':True}), ('U', 'Y', {'hidden':True})]),
        'd': nx.DiGraph([('X', 'Y'), ('Z', 'X'), ('Z', 'Y'), 
                         ('U', 'X', {'hidden':True}), ('U', 'Z', {'hidden':True})]),
        'e': nx.DiGraph([('X', 'Z'), ('Z', 'Y'),
                         ('U', 'X', {'hidden':True}), ('U', 'Y', {'hidden':True})]),
        'f': nx.DiGraph([('X', 'Z1'), ('Z1', 'Y'), ('Z1', 'Z2'), ('Z2', 'Y'),
                         ('U1', 'X', {'hidden':True}), ('U1', 'Z2', {'hidden':True}),
                         ('U2', 'Z1', {'hidden':True}), ('U2', 'Y', {'hidden':True})]),
        'g': nx.DiGraph([('X', 'Z1'), ('Z1', 'Y'), ('Z3', 'Y'),
                         ('Z2', 'X'), ('Z2', 'Z1'), ('Z2', 'Z3'),
                         ('U1', 'X', {'hidden':True}), ('U1', 'Z2', {'hidden':True}),
                         ('U2', 'X', {'hidden':True}), ('U2', 'Z3', {'hidden':True}),
                         ('U3', 'X', {'hidden':True}), ('U3', 'Y', {'hidden':True})]),
    },
    'fig3': {
        'a': nx.DiGraph([('W1', 'X'), ('X', 'Y1'), ('W2', 'Y2'),
                         ('U1', 'W1', {'hidden':True}), ('U1', 'Y1', {'hidden':True}),
                         ('U2', 'W1', {'hidden':True}), ('U2', 'Y2', {'hidden':True}),
                         ('U3', 'W1', {'hidden':True}), ('U3', 'W2', {'hidden':True}),
                         ('U4', 'W2', {'hidden':True}), ('U4', 'X', {'hidden':True})]),
        'b': nx.DiGraph([('W1', 'X'), ('X', 'Y1'), ('W2', 'Y2'), ('W1', 'W2'),
                         ('U1', 'W1', {'hidden':True}), ('U1', 'Y1', {'hidden':True}),
                         ('U2', 'W1', {'hidden':True}), ('U2', 'Y2', {'hidden':True}),
                         ('U3', 'W1', {'hidden':True}), ('U3', 'W2', {'hidden':True}),
                         ('U4', 'W2', {'hidden':True}), ('U4', 'X', {'hidden':True})])
    }
}

# Chickering 1995
chickering = {
    'fig5': nx.DiGraph([('X','Z'), ('Y', 'Z'), ('Y', 'U'), ('Z','W')])
}

# Positions for plotting above graphs. 
# These are keyed on the graphs themselves, so access by oy.ex.pos[graph]
pos = {
    mit: {'A': (0,0), 'B': (1,0), 'C': (.5, -1), 'D': (0, -2), 
          'E': (1, -2), 'F': (.5, -3), 'G': (0, -4)},
    primer['fig1_8']: {'X': (0,0), 'W': (1,1), 'Y': (1,0), 'Z': (2,0), 'T':(1.5, -.5)},
    primer['fig2_5']: {'X': (0,0), 'R': (1,0), 'S': (2, 0), 'T': (3, 0), 'U': (4, 0), 'V': (5, 0), 'Y': (6,0)},
    primer['fig2_6']: {'X': (0,0), 'R': (1,0), 'S': (2, 0), 'T': (3, 0), 'U': (4, 0), 'V': (5, 0), 'Y': (6,0), 'P': (3,-1)},
    primer['fig2_9']: {'X': (0,0), 'W': (1, -.25), 'Y': (2, -.5),
                       'Z1': (.8, 1.5), 'Z2': (2.25, 1.25), 'Z3': (1.25, .75)},
    primer['fig3_7']: {'E':(-1, 1.5), 'Z': (1, 1), 'A': (3,1.5),
                       'X':(0,0), 'Y':(2,0)},
    primer['fig3_8']: {'B': (0,0), 'C': (1,0), 'A': (0, -1), 'Z': (.5, -1), 
                       'D': (1, -1), 'X': (0, -2), 'W': (.5, -2), 'Y': (1, -2)},
    bow['fig4_7']: {'D': (0,-2), 'A': (2, -1), 'E': (4,0), 'X': (6, -1), 
                       'Y': (8, -1), 'C': (2,-3.7), 'B': (4, -2.25), 
                       'F': (2,-5), 'G': (6, -4)},
    sp08['fig1']['a']: {'X':(0,0), 'Y':(1, -2), 'U': (1, -.5)},
    sp08['fig1']['b']: {'X':(0,0), 'Y': (1, -2), 'Z':(.5, -1), 'U': (1, -.25)},
    sp08['fig1']['c']: {'X':(0,0), 'Y': (1, -2), 'Z':(2, -1.5), 'U': (1.5, -.5)},
    sp08['fig1']['d']: {'X':(0,0), 'Y': (1, -2), 'Z':(1, .5), 
                        'U1': (.3, .75), 'U2': (2, -.75)},
    sp08['fig1']['e']: {'X':(0,0), 'Y': (1, -2), 'Z':(1, .5), 
                        'U1': (.3, .75), 'U2': (2, -.75)},
    sp08['fig1']['f']: {'X':(0,0), 'Y': (1, -2), 'Z':(.5, -1), 
                        'U1': (1.5, -.25), 'U2': (1, -1.25)},
    sp08['fig1']['g']: {'X':(0,0), 'Y': (1, -2), 'Z1':(.5, -1), 'Z2':(2, -1.5), 
                        'U1': (1.5, -.5), 'U2': (1.25, -.75)},
    sp08['fig1']['h']: {'X':(0,0), 'Y': (1, -2), 'W':(.5, -1), 'Z':(-1, .5), 
                        'U1': (1.5, -.25), 'U2': (-.5, .75), 
                        'U3': (-.5, -.75), 'U4': (-.75, -1.75)},
    sp08['fig2']['a']: {'X':(0,0), 'Y':(1, -2)},
    sp08['fig2']['b']: {'X':(0,0), 'Y': (1, -2), 'Z':(2, -1.5), 'U': (1.75, -2)},
    sp08['fig2']['c']: {'X':(0,0), 'Y':(1, -2), 'Z': (1, .5), 'U': (1.75, -.5)},
    sp08['fig2']['d']: {'X':(0,0), 'Y':(1, -2), 'Z': (1, .5), 'U': (.3, .75)},
    sp08['fig2']['e']: {'X':(0,0), 'Y': (1, -2), 'Z':(.5, -1), 'U': (1.5, -.25)},
    sp08['fig2']['f']: {'X':(0,0), 'Y': (1, -2), 'Z1':(1, -.75), 'Z2':(2, -1.5), 
                        'U1': (1.5, -.5), 'U2': (1.25, -1.5)},
    sp08['fig2']['g']: {'X':(0,0), 'Z2':(2, 0), 'Z1': (.25, -.5), 
                        'Y': (.5, -1), 'Z3': (1.25, -.75)},
    sp08['fig3']['a']: {'W1': (0,0), 'X': (2,0), 'Y1': (4,0),
                        'W2': (1,-1), 'Y2': (3,-1),
                        'U1': (2,.5), 'U2': (1.25, -.25), 'U3':(0,-.6), 'U4': (1.75, -.75)},
    sp08['fig3']['b']: {'W1': (0,0), 'X': (2,0), 'Y1': (4,0),
                        'W2': (1,-1), 'Y2': (3,-1),
                        'U1': (2,.5), 'U2': (1.25, -.25), 'U3':(0,-.6), 'U4': (1.75, -.75)},
    chickering['fig5']: {'X': (0,0), 'Y': (1,0), 'Z': (.5,-.5), 
                         'U': (1.5,-.5), 'W': (.5,-1)},
}
