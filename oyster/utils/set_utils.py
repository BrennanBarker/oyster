"""Utility functions for working with sets."""

from itertools import chain, combinations, groupby
from functools import reduce

def powerset(iterable):
    """Iterator of the set of all sets, (including {}) of elements in iterable."""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def same_sets(set_lists):
    """Return if the provided lists of sets contain the same sets."""
    set_sets = [{frozenset(S) for S in sl} for sl in set_lists]
    return all_equal(set_sets)

def minimal_sets(sets):
    "Return a list of the minimal sets in a list of sets."
    def append_if_no_subsets(xs, y):
        return xs + [y] if not any(x < y for x in xs) else xs
    return reduce(append_if_no_subsets, sorted(sets, key=len), [])

def _set(iterable):
    """Return a set from an iterable, treating multicharacter strings as one element."""
    if type(iterable) is str:
        return set() if iterable == '' else {iterable}
    else: return set(iterable)

def is_in(a_list):
    """Returns a *function* that checks if its argument is in list.
    Avoids recalculation of list at every comparison."""
    def check(arg): return arg in a_list
    return check