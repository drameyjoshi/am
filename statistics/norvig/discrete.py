from collections.abc import Iterable
from typing import Any, Callable, Dict, Set, TypeVar, Union
from fractions import Fraction

import itertools

U = TypeVar('U')
type Predicate = Callable[..., bool]


def cross(A: Iterable[Any], B: Iterable[Any]) -> Set[str]:
    """
    Returns the cross product of two iterable containers A and B in the form
    of a concatenated string.
    """
    return {str(a) + str(b) for a in A for b in B}


def all_combos(items: Iterable[str], r: int, sep: str = ' ') -> Set[str]:
    """
    Returns all combinations of r items from an iterable collection of n items
    as a set of strings. Each string is a list of items from the collection
    separated by sep.
    """

    return {sep.join(c) for c in itertools.combinations(items, r)}


def such_that(f: Predicate, X: Iterable) -> set:
    """
    Returns a subset of elements x the set X that satisfy the predicate.
    """
    return {x for x in X if f(x)}


class Pmf(Dict[Any, float]):
    """
    Probability mass function.
    """

    def __init__(self, mapping=(), **kwargs):
        self.update(mapping, **kwargs)

        total = sum(self.values())
        for outcome in self:
            self[outcome] = self[outcome] / total
            assert self[outcome] >= 0


def P(event: Union[Predicate, Set[U]], space: Set[U]) -> Union[float, Fraction]:
    """
    Returns the probability of an event in a sample space.

    The event may be specified as a predicate or a set.    
    """
    if isinstance(event, callable):
        subset = such_that(event, space)
    else:
        subset = event

    if isinstance(space, Pmf):
        return sum(space[x] for x in space if x in subset)
    else:
        return Fraction(len(subset & space), len(space))


def joint_pmf(P1: Pmf, P2: Pmf, sep: str = '') -> Pmf:
    """
    Returns the joint probability distribution of two probability mass functions.

    The events in the joint distribution are strings formed of concatenation of
    events of P1 and P2 separated by sep.
    """
    return Pmf({e1 + sep + e1: P1[e1] * P2[e2] for e1 in P1 for e2 in P2})
