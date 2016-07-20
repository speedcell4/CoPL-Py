from typing import List

from bases.derivation import Assertion, Rule, System

from CompareNat.data import Nat, Z, S
from bases.util import DEBUG


class IsLessThan(Assertion):
    template = r'{} is less than {}'

    def __init__(self, n1: Nat, n2: Nat):
        assert isinstance(n1, Nat)
        assert isinstance(n2, Nat)
        self.args = (n1, n2)


class LSucc(Rule):
    name = r'L-Succ'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, IsLessThan)
        n1, n2 = assertion.args
        if isinstance(n2, S):
            if n1 == n2.prev:
                return []


class LTrans(Rule):
    name = r'L-Trans'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, IsLessThan)
        n1, n3 = assertion.args
        if DEBUG:
            print(n1, n3)
        if isinstance(n3, S) and n1 < n3:
            return [IsLessThan(n1, n3.prev), IsLessThan(n3.prev, n3)]


compare_nat1 = System([LSucc(), LTrans()])


class LZero(Rule):
    name = r'L-Zero'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, IsLessThan)
        n1, n2 = assertion.args
        if isinstance(n1, Z) and isinstance(n2, S):
            return []


class LSuccSucc(Rule):
    name = r'L-SuccSucc'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, IsLessThan)
        n1, n2 = assertion.args
        if isinstance(n1, S) and isinstance(n2, S):
            return [IsLessThan(n1.prev, n2.prev)]


compare_nat2 = System([LZero(), LSuccSucc()])


class LSuccR(Rule):
    name = r'L-SuccR'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, IsLessThan)
        n1, n2 = assertion.args
        if DEBUG:
            print(n1, n2)
        if isinstance(n2, S):
            return [IsLessThan(n1, n2.prev)]


compare_nat3 = System([LSucc(), LSuccR()])
