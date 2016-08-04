import logging
from typing import List

from EvalNatExp.rule import PlusIs, TimesIs
from Nat.rule import PZero, PSucc, TZero, TSucc
from ReduceNatExp.data import Exp, ExpNat, ExpPlus, ExpTimes
from bases.deduction import Assertion, Rule, System
from bases.util import type_checking


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

    @type_checking
    def __call__(self, assertion: Reduce1) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpNat):
            n1, n2 = a.a, a.b
            if isinstance(n1, ExpNat) and isinstance(n2, ExpNat):
                return [PlusIs(n1.value, n2.value, b.value)]


class RTimes(Rule):
    name = r'R-Times'

    @type_checking
    def __call__(self, assertion: Reduce1) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpNat):
            n1, n2 = a.a, a.b
            if isinstance(n1, ExpNat) and isinstance(n2, ExpNat):
                return [TimesIs(n1.value, n2.value, b.value)]


class RPlusL(Rule):
    name = r'R-PlusL'

    @type_checking
    def __call__(self, assertion: Reduce1) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpPlus):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e2 == e2_:
                return [Reduce1(e1, e1_)]


class RPlusR(Rule):
    name = r'R-PlusR'

    @type_checking
    def __call__(self, assertion: Reduce1) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpPlus):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e1 == e1_:
                return [Reduce1(e2, e2_)]


class RTimesL(Rule):
    name = r'R-TimesL'

    @type_checking
    def __call__(self, assertion: Reduce1) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpTimes):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e2 == e2_:
                return [Reduce1(e1, e1_)]


class RTimesR(Rule):
    name = r'R-TimesR'

    @type_checking
    def __call__(self, assertion: Reduce1) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpTimes):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e1 == e1_:
                return [Reduce1(e2, e2_)]


class DRPlus(Rule):
    name = r'DR-Plus'

    @type_checking
    def __call__(self, assertion: ReduceD) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpNat):
            n1, n2 = a.a, a.b
            if isinstance(n1, ExpNat) and isinstance(n2, ExpNat):
                return [PlusIs(n1.value, n2.value, b.value)]


class DRTimes(Rule):
    name = r'DR-Times'

    @type_checking
    def __call__(self, assertion: ReduceD) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpNat):
            n1, n2 = a.a, a.b
            if isinstance(n1, ExpNat) and isinstance(n2, ExpNat):
                return [TimesIs(n1.value, n2.value, b.value)]


class DRPlusL(Rule):
    name = r'DR-PlusL'

    @type_checking
    def __call__(self, assertion: ReduceD) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpPlus):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e2 == e2_:
                return [ReduceD(e1, e1_)]


class DRPlusR(Rule):
    name = r'DR-PlusR'

    @type_checking
    def __call__(self, assertion: ReduceD) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpPlus) and isinstance(b, ExpPlus):
            n1, e2 = a.a, a.b
            n1_, e2_ = b.a, b.b
            if isinstance(n1, ExpNat) and isinstance(n1_, ExpNat) and n1 == n1_:
                return [ReduceD(e2, e2_)]


class DRTimesL(Rule):
    name = r'DR-TimesL'

    @type_checking
    def __call__(self, assertion: ReduceD) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpTimes):
            e1, e2 = a.a, a.b
            e1_, e2_ = b.a, b.b
            if e2 == e2_:
                return [ReduceD(e1, e1_)]


class DRTimesR(Rule):
    name = r'DR-TimesR'

    @type_checking
    def __call__(self, assertion: ReduceD) -> List[Assertion]:
        a, b = assertion.args
        if isinstance(a, ExpTimes) and isinstance(b, ExpTimes):
            n1, e2 = a.a, a.b
            n1_, e2_ = b.a, b.b
            if isinstance(n1, ExpNat) and isinstance(n1_, ExpNat) and n1 == n1_:
                return [ReduceD(e2, e2_)]


class MRZero(Rule):
    name = r'MR-Zero'

    @type_checking
    def __call__(self, assertion: Reduce0) -> List[Assertion]:
        e, e_ = assertion.args
        if e == e_:
            return []


class MRMulti(Rule):
    name = r'MR-Multi'

    @type_checking
    def __call__(self, assertion: Reduce0) -> List[Assertion]:
        e, e__ = assertion.args
        if e != e__:
            e_ = e.one_step(e__)
            logging.debug('MR-Multi: {} => {} => {}'.format(e, e_, e__))
            return [Reduce0(e, e_), Reduce0(e_, e__)]


class MROne(Rule):
    name = r'MR-One'

    @type_checking
    def __call__(self, assertion: Reduce0) -> List[Assertion]:
        e, e_ = assertion.args
        if e != e_ and e.one_step(e_) == e_:
            return [Reduce1(e, e_)]


reduce_nat_exp = System([RPlus(), RTimes(), RPlusL(), RPlusR(), RTimesL(), RTimesR(), DRPlus(), DRTimes(),
                         DRPlusL(), DRPlusR(), DRTimesL(), DRTimesR(), MRZero(), MROne(), MRMulti(),
                         PZero(), PSucc(), TZero(), TSucc()])
