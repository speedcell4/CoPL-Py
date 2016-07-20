from typing import List

from base.derivation import Assertion, Rule, System
from Nat.data import Nat, S, Z


class PlusIs(Assertion):
    template = '{} plus {} is {}'

    def __init__(self, a: Nat, b: Nat, c: Nat):
        assert isinstance(a, Nat)
        assert isinstance(b, Nat)
        assert isinstance(c, Nat)
        self.args = (a, b, c)


class TimesIs(Assertion):
    template = '{} times {} is {}'

    def __init__(self, a: Nat, b: Nat, c: Nat):
        assert isinstance(a, Nat)
        assert isinstance(b, Nat)
        assert isinstance(c, Nat)
        self.args = (a, b, c)


class PZero(Rule):
    name = 'P-Zero'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, PlusIs)
        n1, n2, n3 = assertion.args
        if n1 == Z() and n2 == n3:
            return []


class PSucc(Rule):
    name = 'P-Succ'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, PlusIs)
        n1, n2, n3 = assertion.args
        if isinstance(n1, S) and isinstance(n3, S):
            return [PlusIs(n1.prev, n2, n3.prev)]


class TZero(Rule):
    name = 'T-Zero'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, TimesIs)
        n1, n2, n3 = assertion.args
        if isinstance(n1, Z) and isinstance(n3, Z):
            return []


class TSucc(Rule):
    name = 'T-Succ'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, TimesIs)
        n1, n2, n4 = assertion.args
        if isinstance(n1, S):
            n3 = n1.prev * n2
            return [TimesIs(n1.prev, n2, n3), PlusIs(n2, n3, n4)]


nat = System([PZero(), PSucc(), TZero(), TSucc()])
