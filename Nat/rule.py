from typing import List

from Nat.data import Nat, S, Z
from bases.deduction import Assertion, Rule, System
from bases.util import type_checking


class PlusIs(Assertion):
    template = '{} plus {} is {}'

    @type_checking
    def __init__(self, a: Nat, b: Nat, c: Nat):
        self.args = (a, b, c)


class TimesIs(Assertion):
    template = '{} times {} is {}'

    @type_checking
    def __init__(self, a: Nat, b: Nat, c: Nat):
        self.args = (a, b, c)


class PZero(Rule):
    name = 'P-Zero'

    @type_checking
    def __call__(self, assertion: PlusIs) -> List[Assertion]:
        n1, n2, n3 = assertion.args
        if n1 == Z() and n2 == n3:
            return []


class PSucc(Rule):
    name = 'P-Succ'

    @type_checking
    def __call__(self, assertion: PlusIs) -> List[Assertion]:
        n1, n2, n3 = assertion.args
        if isinstance(n1, S) and isinstance(n3, S):
            return [PlusIs(n1.prev, n2, n3.prev)]


class TZero(Rule):
    name = 'T-Zero'

    @type_checking
    def __call__(self, assertion: TimesIs) -> List[Assertion]:
        n1, n2, n3 = assertion.args
        if isinstance(n1, Z) and isinstance(n3, Z):
            return []


class TSucc(Rule):
    name = 'T-Succ'

    @type_checking
    def __call__(self, assertion: TimesIs) -> List[Assertion]:
        n1, n2, n4 = assertion.args
        if isinstance(n1, S):
            n3 = n1.prev * n2
            return [TimesIs(n1.prev, n2, n3), PlusIs(n2, n3, n4)]


nat = System([PZero(), PSucc(), TZero(), TSucc()])
