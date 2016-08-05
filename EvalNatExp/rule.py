from typing import List

from EvalNatExp.data import Exp, ExpNat, ExpPlus, ExpTimes
from Nat.data import Nat
from Nat.rule import PlusIs, TimesIs, PZero, PSucc, TZero, TSucc
from bases.derivation import Assertion, Rule, System
from bases.util import type_checking


class EvalTo(Assertion):
    template = r'{} evalto {}'

    @type_checking
    def __init__(self, exp: Exp, nat: Nat):
        self.args = (exp, nat)


class EConst(Rule):
    name = r'E-Const'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, n = assertion.args
        if isinstance(e, ExpNat) and e.value == n:
            return []


class EPlus(Rule):
    name = r'E-Plus'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, n = assertion.args
        if isinstance(e, ExpPlus):
            e1, e2 = e.a, e.b
            n1, n2 = e1.value, e2.value
            return [EvalTo(e1, n1), EvalTo(e2, n2), PlusIs(n1, n2, n)]


class ETimes(Rule):
    name = r'E-Times'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, n = assertion.args
        if isinstance(e, ExpTimes):
            e1, e2 = e.a, e.b
            n1, n2 = e1.value, e2.value
            return [EvalTo(e1, n1), EvalTo(e2, n2), TimesIs(n1, n2, n)]


eval_nat_exp = System([EConst(), EPlus(), ETimes(), PZero(), PSucc(), TZero(), TSucc()])
