from typing import List

from EvalML1.data import Exp, ExpInt, ExpBool, ExpPlus, ExpMinus, ExpTimes, ExpLt, ExpIf, Value, ValueInt, ValueBool
from bases.derivation import Assertion, Rule, System
from bases.util import type_checking


class EvalTo(Assertion):
    template = r'{} evalto {}'

    @type_checking
    def __init__(self, a: Exp, b: Value):
        self.args = (a, b)


class PlusIs(Assertion):
    template = r'{} plus {} is {}'

    @type_checking
    def __init__(self, a: ValueInt, b: ValueInt, c: ValueInt):
        self.args = (a, b, c)


class MinusIs(Assertion):
    template = r'{} minus {} is {}'

    @type_checking
    def __init__(self, a: ValueInt, b: ValueInt, c: ValueInt):
        self.args = (a, b, c)


class TimesIs(Assertion):
    template = r'{} times {} is {}'

    @type_checking
    def __init__(self, a: ValueInt, b: ValueInt, c: ValueInt):
        self.args = (a, b, c)


class LtIs(Assertion):
    template = r'{} less than {} is {}'

    @type_checking
    def __init__(self, a: ValueInt, b: ValueInt, c: ValueBool):
        self.args = (a, b, c)


class EInt(Rule):
    name = r'E-Int'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, v = assertion.args
        if isinstance(e, ExpInt) and e.value == v:
            return []


class EBool(Rule):
    name = r'E-Bool'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, v = assertion.args
        if isinstance(e, ExpBool) and e.value == v:
            return []


class EIfT(Rule):
    name = r'E-IfT'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, v = assertion.args
        if isinstance(e, ExpIf):
            e1, e2, e3 = e.a, e.b, e.c
            return [EvalTo(e1, ValueBool(True)), EvalTo(e2, v)]


class EIfF(Rule):
    name = r'E-IfF'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, v = assertion.args
        if isinstance(e, ExpIf):
            e1, e2, e3 = e.a, e.b, e.c
            return [EvalTo(e2, ValueBool(False)), EvalTo(e3, v)]


class EPlus(Rule):
    name = r'E-Plus'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, i3 = assertion.args
        if isinstance(e, ExpPlus) and isinstance(i3, ValueInt):
            e1, e2 = e.a, e.b
            i1, i2 = e1.value, e2.value
            return [EvalTo(e1, i1), EvalTo(e2, i2), PlusIs(i1, i2, i3)]


class EMinus(Rule):
    name = r'E-Minus'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, i3 = assertion.args
        if isinstance(e, ExpMinus) and isinstance(i3, ValueInt):
            e1, e2 = e.a, e.b
            i1, i2 = e1.value, e2.value
            return [EvalTo(e1, i1), EvalTo(e2, i2), MinusIs(i1, i2, i3)]


class ETimes(Rule):
    name = r'E-Times'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, i3 = assertion.args
        if isinstance(e, ExpTimes) and isinstance(i3, ValueInt):
            e1, e2 = e.a, e.b
            i1, i2 = e1.value, e2.value
            return [EvalTo(e1, i1), EvalTo(e2, i2), TimesIs(i1, i2, i3)]


class ELt(Rule):
    name = r'E-Lt'

    @type_checking
    def __call__(self, assertion: EvalTo) -> List[Assertion]:
        e, b3 = assertion.args
        if isinstance(e, ExpLt) and isinstance(b3, ValueBool):
            e1, e2 = e.a, e.b
            i1, i2 = e1.value, e2.value
            return [EvalTo(e1, i1), EvalTo(e2, i2), LtIs(i1, i2, b3)]


class BPlus(Rule):
    name = r'B-Plus'

    @type_checking
    def __call__(self, assertion: PlusIs) -> List[Assertion]:
        i1, i2, i3 = assertion.args
        if i3 == i1 + i2:
            return []


class BMinus(Rule):
    name = r'B-Minus'

    @type_checking
    def __call__(self, assertion: MinusIs) -> List[Assertion]:
        i1, i2, i3 = assertion.args
        if i3 == i1 - i2:
            return []


class BTimes(Rule):
    name = r'B-Times'

    @type_checking
    def __call__(self, assertion: TimesIs) -> List[Assertion]:
        i1, i2, i3 = assertion.args
        if i3 == i1 * i2:
            return []


class BLt(Rule):
    name = r'B-Lt'

    @type_checking
    def __call__(self, assertion: LtIs) -> List[Assertion]:
        i1, i2, b3 = assertion.args
        if b3 == (i1 < i2):
            return []


eval_ml_1 = System(
    [EInt(), EBool(), EIfT(), EIfF(), EPlus(), EMinus(), ETimes(), ELt(), BPlus(), BMinus(), BTimes(), BLt()])
