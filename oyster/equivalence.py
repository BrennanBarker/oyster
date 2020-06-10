"""Functions for generating equivalent DAGs and and working with Complete Partial DAGs."""

from oyster.utils.graph_utils import *
from oyster.utils.set_utils import *

def dag_to_cpdag(DAG):
    """Given a causal DAG, generate the completed partial DAG (CPDAG)
    that encapsulates DAG's equivalence class using R1-4 from Pearl 2009."""
    
    def oriented_v_structures(DAG):
        """Return a partial DAG (pDAG) with edges oriented to match DAG's 
        v_structures and an edge in both directions for all other edges."""
        collider_out_edges = []
        for collider, set_of_parent_pairs in v_structures(DAG).items():
            for parent_pair in set_of_parent_pairs:
                pair = list(parent_pair)
                collider_out_edges.append((collider, pair[0]))
                collider_out_edges.append((collider, pair[1]))
        return edges_removed(bidirected(DAG), collider_out_edges)
    
    def rule1(pDAG):
        """Return a pDAG with any b<->c oriented to b->c whenever 
        there is an arrow a->b such that a and c are non-adjacent."""
        nonadjacent = is_in(NA_pairs(pDAG))
        compelled = is_in(compelled_edges(pDAG))
        inconsistent_edges = set()
        for (b,c) in reversible_edges(pDAG):
            for a in pDAG.nodes() - {b} - {c}:
                if compelled((a,b)) and nonadjacent({a,c}):
                    inconsistent_edges.add((c, b))       
        return edges_removed(pDAG, inconsistent_edges)

    def rule2(pDAG):
        """Return a pDAG with any a<->b oriented to a->b whenever 
        there is a chain a->c->b."""
        compelled = is_in(compelled_edges(pDAG))
        inconsistent_edges = set()
        for (a,b) in reversible_edges(pDAG):
            for c in pDAG.nodes() - {a} - {b}:
                if compelled((a,c)) and compelled((c,b)):
                    inconsistent_edges.add((b,a))        
        return edges_removed(pDAG, inconsistent_edges)
        
    def rule3(pDAG):
        """Return a pDAG with any a<->b oriented to a->b whenever 
        there are two rule3-type chains (see below)."""
        rvs_edges = reversible_edges(pDAG)
        nonadjacent = is_in(NA_pairs(pDAG))
        compelled = is_in(compelled_edges(pDAG))
        reversible = is_in(rvs_edges)
    
        def two_rule3_chains(a,b):
            """Return if there are two chains between a and b of form 
            a<->c->b and a<->d->b and such that c and d are nonadjacent."""
            for c in pDAG.nodes() - {a} - {b}:
                if reversible((a,c)) and compelled((c,b)):
                    for d in pDAG.nodes() - {a} - {b} - {c}:
                        if all((reversible((a,d)), compelled((d,b)),
                                nonadjacent({c,d}))): return True
            return False

        inconsistent_edges = set()
        for (a,b) in rvs_edges:
            if two_rule3_chains(a,b): inconsistent_edges.add((b,a))
        return edges_removed(pDAG, inconsistent_edges)

    def rule4(pDAG):
        """Return a pDAG with any a<->b oriented to a->b whenever 
        there are two rule4-type chains (see below)."""
        rvs_edges = reversible_edges(pDAG)
        nonadjacent = is_in(NA_pairs(pDAG))
        def adjacent(pair): return not nonadjacent(pair)
        compelled = is_in(compelled_edges(pDAG))
        reversible = is_in(rvs_edges)

        def two_rule4_chains(a,b):
            """Return if there are two chains between a and b of form 
            a--c->d and c->d->b and such that c and b are nonadjacent 
            and a and d are adjacent."""
            for c in pDAG.nodes() - {a} - {b}:
                for d in pDAG.nodes() - {a} - {b} - {c}:
                    if all((reversible((a,c)), compelled((c,d)), 
                            compelled((d,b)), nonadjacent({c,b}), 
                            adjacent({a,d}))): return True
            return False

        inconsistent_edges = set()
        for (a,b) in rvs_edges:
            if two_rule4_chains(a,b): inconsistent_edges.add((b,a))
        return edges_removed(pDAG, inconsistent_edges)

    pDAG = oriented_v_structures(DAG)
    # Apply rules 1-4 until no more edges can be oriented
    new_pDAG = rule4(rule3(rule2(rule1(pDAG))))
    while not equal(new_pDAG, pDAG):
        pDAG = new_pDAG
        new_pDAG = rule4(rule3(rule2(rule1(pDAG)))) 
    cpDAG = new_pDAG
    return cpDAG

def equivalence_class_size(DAG):
    """Return the size of the DAG's equivalence class."""
    cpdag = dag_to_cpdag(DAG)
    return 2 ** (len(reversible_edges(cpdag)) // 2)
