"""Representing adjustment formulas in Latex."""

from oyster import *
from oyster.utils.graph_utils import *
from oyster.utils.set_utils import _set
from oyster.utils.set_utils import *

def joint_factorization(DAG, do=[], hidden=[]):
    """Return an expression for the joint probability distribution
    factorized according to the relationships encoded in DAG."""
    if do: DAG = do_X(DAG, do)
    factors = [P(val(V), given=pa(DAG, V)) for V in DAG.nodes - _set(do)]
    return joint(DAG, do=do) + '=' + product(factors)

def backdoor_adjustment_formula(DAG, X, Y, Z):
    """An expression for the causal effect of X on Y when adjusting 
    for a set of variables Z that satisfy the back-door criterion."""

    assert meets_backdoor_criterion(DAG, X, Y, Z), 'Z does not meet backdoor criterion'
    
    x,y,z = map(val, (X, Y, Z))  
    if len(z) > 0: z = '{'+str(z)+'}'
    bd_formula = f'\sum_{z}{P(y, given=(x, z))}{P(z)}'
    
    return P(y, do=x) + '=' + bd_formula

def frontdoor_adjustment_formula(DAG, X, Y, Z):
    """An expression for the causal effect of X on Y when adjusting 
    for a set of variables Z that satisfy the front-door criterion."""
    
    assert meets_frontdoor_criterion(DAG, X, Y, Z), 'Z does not meet frontdoor criterion'
    
    x,y,z = map(val, (X, Y, Z))
    xp = x+"'"
    subxp = '{'+xp+'}'
    
    fd_formula = f"\sum_{z}{P(z, given=x)}\sum_{subxp}{P(y, given=(xp, z))}{P(xp)}"

    return P(y, do=x) + '=' + fd_formula

def specific_adjustment_formula(DAG, X, Y, Z, S):
    """An expression for the z-specific causal effect of X on Y.
    Z U S must satisfy the front-door criterion."""

    assert meets_backdoor_criterion(DAG, X, Y, _set(Z) | _set(S)), 'Z does not meet backdoor criterion'
    
    x,y,z,s = map(val, (X, Y, Z, S))  
    if len(s) > 0: sub_s = '{'+str(s)+'}'
    specific_formula = f'\sum_{sub_s}{P(y, given=(x, s, z))}{P(s, given=z)}'
    
    return P(y, given=z, do=x) + '=' + specific_formula
    
# Representations
def val(Variables):
    """Represent a variable as a value"""
    return ','.join(sorted(_set(Variables))).lower()

def tjoin(vals):
    return ','.join(sorted(vals)) if type(vals) == tuple else vals

def _sub(do):
    return '_{'+do+'}' if do else ''

def P(event, given=[], do=[]):
    """Represent the (maybe conditional) probability of an event(s)."""
    conditional = f' | {tjoin(given)}' if given else ''
    return f'P{_sub(tjoin(do))}({tjoin(event)}{tjoin(conditional)})'

def product(factors):
    """Represent a product of a list of factors"""
    return ''.join(sorted(factors))

def joint(DAG, do=[]):
    do = _set(do)
    return P(val(DAG.nodes - do), do=val(do))

def pa(DAG, V):
    return val(Pa(DAG, V))
