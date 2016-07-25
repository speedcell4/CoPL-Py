from ReduceNatExp.data import Nat, Exp, ExpNat, ExpPlus, ExpTimes
from typing import List
from EvalNatExp.rule import PlusIs, TimesIs
from Nat.rule import PZero, PSucc, TZero, TSucc
from bases.derivation import Assertion, Rule, System, DeductionError


class Reduce(Assertion):
    def __init__(self, e1: 'Exp', e2: 'Exp'):
        assert isinstance(e1, Exp)
        assert isinstance(e2, Exp)
        self.args = (e1, e2)


class Reduce1(Reduce):
    template = r'{} ---> {}'


class Reduce0(Reduce):
    template = r'{} -*-> {}'


class ReduceD(Reduce):
    template = r'{} -d-> {}'


class RPlus(Rule):
    name = r'R-Plus'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, Reduce1)
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpNat):
            n1, n2 = a.a, a.b
            return [PlusIs(n1, n2, b.value)]


class RTimes(Rule):
    name = r'R-Times'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, Reduce1)
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpNat):
            n1, n2 = a.a, a.b
            return [TimesIs(n1, n2, b.value)]


class RPlusL(Rule):
    name = r'R-PlusL'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, Reduce1)
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpPlus):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e2 == e2_:
                return [Reduce1(e1, e1_)]


class RPlusR(Rule):
    name = r'R-PlusR'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, Reduce1)
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpPlus):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e1 == e1_:
                return [Reduce1(e2, e2_)]


class RTimesL(Rule):
    name = r'R-TimesL'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, Reduce1)
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpTimes):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e2 == e2_:
                return [Reduce1(e1, e1_)]


class RTimesR(Rule):
    name = r'R-TimesR'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, Reduce1)
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpTimes):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e1 == e1_:
                return [Reduce1(e2, e2_)]


class DRPlus(Rule):
    name = r'DR-Plus'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, ReduceD)
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpNat):
            n1, n2, n3 = a.a, a.b, b.value
            return [PlusIs(n1, n2, n3)]


class DRTimes(Rule):
    name = r'DR-Times'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, ReduceD)
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpNat):
            n1, n2, n3 = a.a, a.b, b.value
            return [TimesIs(n1, n2, n3)]


class DRPlusL(Rule):
    name = r'DR-PlusL'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, ReduceD)
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpPlus):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e2 == e2_:
                return [ReduceD(e1, e1_)]


class DRPlusR(Rule):
    name = r'DR-PlusR'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, ReduceD)
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpPlus):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e1 == e1_:
                return [ReduceD(e2, e2_)]


class DRTimesL(Rule):
    name = r'DR-TimesL'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, ReduceD)
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpTimes):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e2 == e2_:
                return [ReduceD(e1, e1_)]


class DRTimesR(Rule):
    name = r'DR-TimesR'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, ReduceD)
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpTimes):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e1 == e1_:
                return [ReduceD(e2, e2_)]


class MRZero(Rule):
    name = r'MR-Zero'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, Reduce0)
        a, b = assertion.args
        if a == b:
            return []


class MRMulti(Rule):
    name = r'MR-Multi'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, Reduce0)
        a, b = assertion.args
        if a != b:
            c = a.one_step(b)
            return [Reduce0(a, c), Reduce0(c, b)]


class MROne(Rule):
    name = r'MR-One'

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        assert isinstance(assertion, Reduce0)
        a, b = assertion.args
        return [Reduce1(a, b)]


reduce_nat_exp = System([RPlus(), RTimes(), RPlusL(), RPlusR(), RTimesL(), RTimesR(), DRPlus(), DRTimes(),
                         DRPlusL(), DRPlusR(), DRTimesL(), DRTimesR(), MRZero(), MRMulti(), MROne(),
                         PZero(), PSucc(), TZero(), TSucc()])
