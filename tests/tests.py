"""Testing suite."""

from context import oyster

import unittest

from oyster.adjust import (d_separated, d_separator_search, 
                           backdoor_criterion_search, minimal_adjustment_sets, specific_adjustment_sets, 
                           meets_frontdoor_criterion, frontdoor_criterion_search)
from oyster.identify import is_identifiable, is_identifiable_single_x
from oyster.structures import (root_set, is_tree, is_forest, is_c_component,
                               c_components,)
from oyster.equivalence import equivalence_class_size
from oyster.utils.set_utils import minimal_sets, _set, same_sets
from oyster.utils.graph_utils import MB, NA_pairs, v_structures
from oyster.example.graphs import mit, bow, primer, sp08, chickering

class test_causal_structures(unittest.TestCase):
    
    def test_MB(self):
        # Primer study question 2.4.1 d)
        self.assertEqual({node: MB(primer['fig2_9'], node) for node in primer['fig2_9']},
                         {'W': {'X', 'Y', 'Z2', 'Z3'},
                          'X': {'W', 'Z1', 'Z3'},
                          'Y': {'W', 'Z2', 'Z3'},
                          'Z1': {'X', 'Z2', 'Z3'},
                          'Z2': {'W', 'Y', 'Z1', 'Z3'},
                          'Z3': {'W', 'X', 'Y', 'Z1', 'Z2'}})
    
    def test_v_structures(self):
        vs = v_structures(primer['fig3_8'])
        self.assertTrue(same_sets((vs['Z'], [{'B', 'C'}])))
        self.assertTrue(same_sets((vs['X'], [{'A', 'Z'}])))
        self.assertTrue(same_sets((vs['Y'], [{'W', 'Z'}, {'D', 'W'}, {'D', 'Z'}])))


class test_adjust(unittest.TestCase):
        
    def test_d_seperator_search(self):
        G = primer['fig2_9']
        # Primer study question 2.4.1 a)
        part_a = {frozenset((X,Y)): 
                  {frozenset(el) 
                   for el in minimal_sets(d_separator_search(G, X, Y))}
                  for X,Y in NA_pairs(G)}
        
        self.assertEqual(part_a, 
                         {frozenset({'X', 'Y'}): {frozenset({'W', 'Z1', 'Z3'}), frozenset({'W', 'Z2', 'Z3'})},
                          frozenset({'X', 'Z2'}): {frozenset({'Z1', 'Z3'})},
                          frozenset({'W', 'Z1'}): {frozenset({'X'})},
                          frozenset({'W', 'Z3'}): {frozenset({'X'})},
                          frozenset({'W', 'Z2'}): {frozenset({'Z1', 'Z3'}), frozenset({'X'})},
                          frozenset({'Y', 'Z1'}): {frozenset({'W', 'Z2', 'Z3'}), frozenset({'X', 'Z2', 'Z3'})},
                          frozenset({'Z1', 'Z2'}): {frozenset()}})
        
        # Primer study question 2.4.1 b)
        def only_measurable_variables(s): return s < {'Z3', 'Z1', 'X', 'W'}
        part_b = {k:list(filter(only_measurable_variables, v)) 
                  for k,v in part_a.items() if only_measurable_variables(k)}
        
        self.assertEqual(part_b, 
                         {frozenset({'W', 'Z1'}): [frozenset({'X'})],
                          frozenset({'W', 'Z3'}): [frozenset({'X'})]})
        
    def test_d_separated(self):
        G = primer['fig2_9']
        # Primer study question 2.4.1 c)
        part_c = {frozenset((X,Y)):
                  d_separated(G, X, Y, (G.nodes - {X} - {Y}))
                  for X,Y in NA_pairs(G)}
        self.assertEqual(part_c, 
                         {frozenset({'X', 'Y'}): True,
                          frozenset({'X', 'Z2'}): True,
                          frozenset({'W', 'Z1'}): True,
                          frozenset({'W', 'Z3'}): False,
                          frozenset({'W', 'Z2'}): False,
                          frozenset({'Y', 'Z1'}): True,
                          frozenset({'Z1', 'Z2'}): False})
        
        self.assertFalse(d_separated(mit, 'A', 'B', ['D', 'F']))
        self.assertTrue(d_separated(mit, 'A', 'B', []))
        self.assertTrue(d_separated(mit, 'D', 'E', ['C']))
        self.assertFalse(d_separated(mit, 'D', 'E', []))
        self.assertFalse(d_separated(mit, 'D', 'E', ['A', 'B']))
        self.assertFalse(d_separated(mit, ['E', 'G'], 'D', 'C'))
        
    def test_backdoor_criterion_search(self):
        self.assertTrue(same_sets((
            backdoor_criterion_search(primer['fig3_7'], 'X', 'Y'), 
            [{'A', 'Z'}, {'E', 'Z'}, {'A', 'E', 'Z'}]
        )))
        
        # Primer study question 3.3.1 a)
        self.assertTrue(same_sets((
            backdoor_criterion_search(primer['fig3_8'], 'X', 'Y'),
            [{'B', 'Z'}, {'D', 'Z'}, {'C', 'Z'}, {'A', 'Z'},
             {'B', 'D', 'Z'}, {'B', 'C', 'Z'}, {'A', 'B', 'Z'},
             {'C', 'D', 'Z'}, {'A', 'D', 'Z'}, {'A', 'C', 'Z'},
             {'B', 'C', 'D', 'Z'}, {'A', 'B', 'D', 'Z'},
             {'A', 'B', 'C', 'Z'}, {'A', 'C', 'D', 'Z'},
             {'A', 'B', 'C', 'D', 'Z'}]
        )))

    def test_minimal_adjustment_sets(self):
        G = primer['fig3_8']
        # Primer study question 3.3.1 b)
        self.assertTrue(same_sets((
            minimal_adjustment_sets(G, 'X', 'Y'), 
            [{'A', 'Z'}, {'C', 'Z'}, {'B', 'Z'}, {'D', 'Z'}])))
        
        # Primer study question 3.3.1 c1)
        self.assertTrue(same_sets((
            minimal_adjustment_sets(G, 'D', 'Y'),
            [{'C'}, {'A', 'Z'}, {'X', 'Z'}, {'B', 'Z'}, {'W', 'Z'}])))
        
        # Primer study question 3.3.1 c2)
        self.assertTrue(same_sets((
            minimal_adjustment_sets(primer['fig3_8'], ['W', 'D'], 'Y'),
            [{'Z'}, {'C', 'X'}])))
        
        # Book of Why, pp. 164 ('C' is unobservable)
        self.assertTrue(same_sets((
            minimal_adjustment_sets(bow['fig4_7'], 'X', 'Y'),
            [{'C', 'E', 'F', 'G'}, {'A', 'B', 'E', 'F', 'G'}])))

    def test_specfic_adjustment_sets(self):
        G = primer['fig3_8']
        # Primer 3.5.1 a)
        self.assertTrue(same_sets((
            minimal_sets(specific_adjustment_sets(G, 'X','Y','C')), 
            [{'C', 'Z'}])))
        # Primer 3.5.1 b) any of these:
        self.assertTrue(same_sets((
            [_ for _ in specific_adjustment_sets(G, 'X', 'Y', 'Z') if len(_) == 4],
            [{'A', 'B', 'C', 'Z'}, {'B', 'C', 'D', 'Z'},
             {'A', 'B', 'D', 'Z'}, {'A', 'C', 'D', 'Z'}])))

    def frontdoor_criterion_search(self):
        self.assertTrue(same_sets(frontdoor_criterion_search(primer['fig3_8'], 'X', 'Y'), [{'W'}]))

    

class test_identify(unittest.TestCase):
    
    def test_root_set(self):
        self.assertTrue(
            all(root_set(G) == {'Y'} for G in sp08['fig1'].values())
        )
        self.assertTrue(
            all(root_set(G) == {'Y1', 'Y2'} for G in sp08['fig3'].values())
        )
    
    def test_is_tree(self):
        trees = ['a', 'b', 'd', 'e', 'f', 'g', 'h']
        self.assertEqual(
            [is_tree(G) for G in sp08['fig1'].values()],
            [True, True, False, True, True, True, True, True]
        )
        self.assertFalse(
            any(is_tree(G) for G in sp08['fig3'].values())
        )
        
    def test_is_forest(self):
        self.assertEqual(
            [is_forest(G) for G in sp08['fig1'].values()],
            [True, True, False, True, True, True, True, True]
        )
        self.assertEqual(
            [is_forest(G) for G in sp08['fig3'].values()],
            [True, False]
        )
    
    def test_is_c_component(self):
        self.assertEqual(
            [is_c_component(G) for G in sp08['fig1'].values()],
            [True, False, False, True, True, True, False, True]
        )
        
    def test_c_components(self):
        self.assertEqual(
            [set([frozenset(c) for c in c_components(g)]) for g in sp08['fig2'].values()],
            [{frozenset({'Y'}), frozenset({'X'})},
             {frozenset({'Y', 'Z'}), frozenset({'X'})},
             {frozenset({'Y', 'Z'}), frozenset({'X'})},
             {frozenset({'X', 'Z'}), frozenset({'Y'})},
             {frozenset({'Z'}), frozenset({'X', 'Y'})},
             {frozenset({'X', 'Z2'}), frozenset({'Y', 'Z1'})},
             {frozenset({'Z1'}), frozenset({'X', 'Y', 'Z2', 'Z3'})}]
        )
        
    def test_is_identifiable_single_x(self):
        self.assertFalse(
            any(is_identifiable_single_x(G, 'X', 'Y') for G in sp08['fig1'].values())
        )
        self.assertTrue(
            any(is_identifiable_single_x(G, 'X', 'Y') for G in sp08['fig2'].values())
        )
        
    def test_is_identifiable(self):
        self.assertFalse(
            any(is_identifiable(G, 'X', 'Y') for G in sp08['fig1'].values())
        )
        self.assertTrue(
            any(is_identifiable(G, 'X', 'Y') for G in sp08['fig2'].values())
        )
        self.assertTrue(
            is_identifiable(sp08['fig3']['a'], 'X', {'Y1', 'Y2'})
        )
        self.assertFalse(
            is_identifiable(sp08['fig3']['b'], 'X', {'Y1', 'Y2'})
        )
        
class test_equivalence(unittest.TestCase):
    
    def test_equivalence_class_size(self):
        self.assertEqual(equivalence_class_size(chickering['fig5']), 2)
        self.assertEqual(equivalence_class_size(primer['fig2_9']), 1)
        self.assertEqual(equivalence_class_size(primer['fig3_7']), 1)
        self.assertEqual(equivalence_class_size(primer['fig3_8']), 4)
        self.assertEqual(equivalence_class_size(bow['fig4_7']), 2)

if __name__ == '__main__':
    unittest.main()