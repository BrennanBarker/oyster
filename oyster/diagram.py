import networkx as nx

class CausalDiagram(nx.DiGraph):
    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, *attr)
        assert nx.is_directed_acyclic_graph(self), "Input data is not acyclic!"