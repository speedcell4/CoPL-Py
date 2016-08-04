from typing import List

from EvalML1.data import ValueInt, ValueBool, Exp, ExpPlus, ExpMinus, ExpTimes, ExpLt, ExpIf
from EvalML1.rule import EvalTo, EInt, EBool, EIfT, EIfF, EPlus, EMinus, ETimes, ELt, BPlus, BMinus, BTimes, BLt
from EvalML1Err.data import ResErr
from bases.deduction import Assertion, Rule, System
from bases.util import type_checking


class EvalToErr(Assertion):
    template = r'{} evalto {}'

    @type_checking
    def __init__(self, a: Exp, b: ResErr):
        self.args = (a, b)


class EPlusBoolL(Rule):
    name = r'E-PlusBoolL'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpPlus):
            e1, e2 = e.a, e.b
            b = e1.value
            if isinstance(b, ValueBool):
                return [EvalTo(e1, b)]


class EPlusBoolR(Rule):
    name = r'E-PlusBoolR'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpPlus):
            e1, e2 = e.a, e.b
            b = e2.value
            if isinstance(b, ValueBool):
                return [EvalTo(e2, b)]


class EPlusErrorL(Rule):
    name = r'E-PlusErrorL'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpPlus):
            e1, e2 = e.a, e.b
            return [EvalToErr(e1, ResErr())]


class EPlusErrorR(Rule):
    name = r'E-PlusErrorR'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpPlus):
            e1, e2 = e.a, e.b
            return [EvalToErr(e2, ResErr())]


class EMinusBoolL(Rule):
    name = r'E-MinusBoolL'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpMinus):
            e1, e2 = e.a, e.b
            b = e1.value
            if isinstance(b, ValueBool):
                return [EvalTo(e1, b)]


class EMinusBoolR(Rule):
    name = r'E-MinusBoolR'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpMinus):
            e1, e2 = e.a, e.b
            b = e2.value
            if isinstance(b, ValueBool):
                return [EvalTo(e2, b)]


class EMinusErrorL(Rule):
    name = r'E-MinusErrorL'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpMinus):
            e1, e2 = e.a, e.b
            return [EvalToErr(e1, ResErr())]


class EMinusErrorR(Rule):
    name = r'E-MinusErrorR'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpMinus):
            e1, e2 = e.a, e.b
            return [EvalToErr(e2, ResErr())]


class ETimesBoolL(Rule):
    name = r'E-TimesBoolL'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpTimes):
            e1, e2 = e.a, e.b
            b = e1.value
            if isinstance(b, ValueBool):
                return [EvalTo(e1, b)]


class ETimesBoolR(Rule):
    name = r'E-TimesBoolR'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpTimes):
            e1, e2 = e.a, e.b
            b = e2.value
            if isinstance(b, ValueBool):
                return [EvalTo(e2, b)]


class ETimesErrorL(Rule):
    name = r'E-TimesErrorL'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpTimes):
            e1, e2 = e.a, e.b
            return [EvalToErr(e1, ResErr())]


class ETimesErrorR(Rule):
    name = r'E-TimesErrorR'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpTimes):
            e1, e2 = e.a, e.b
            return [EvalToErr(e2, ResErr())]


class ELtBoolL(Rule):
    name = r'E-LtBoolL'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpLt):
            e1, e2 = e.a, e.b
            b = e1.value
            if isinstance(b, ValueBool):
                return [EvalTo(e1, b)]


class ELtBoolR(Rule):
    name = r'E-LtBoolR'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpLt):
            e1, e2 = e.a, e.b
            b = e2.value
            if isinstance(b, ValueBool):
                return [EvalTo(e2, b)]


class ELtErrorL(Rule):
    name = r'E-LtErrorL'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpLt):
            e1, e2 = e.a, e.b
            return [EvalToErr(e1, ResErr())]


class ELtErrorR(Rule):
    name = r'E-LtErrorR'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpLt):
            e1, e2 = e.a, e.b
            return [EvalToErr(e2, ResErr())]


class EIfInt(Rule):
    name = r'E-IfInt'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpIf):
            e1, e2, e3 = e.a, e.b, e.c
            i1 = e1.value
            if isinstance(i1, ValueInt):
                return [EvalTo(e1, i1)]


class EIfError(Rule):
    name = r'E-IfError'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpIf):
            e1, e2, e3 = e.a, e.b, e.c
            return [EvalToErr(e1, ResErr())]


class EIfTError(Rule):
    name = r'E-IfTError'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpIf):
            e1, e2, e3 = e.a, e.b, e.c
            return [EvalTo(e1, ValueBool(True)), EvalToErr(e2, ResErr())]


class EIfFError(Rule):
    name = r'E-IfFError'

    @type_checking
    def __call__(self, assertion: EvalToErr) -> List[Assertion]:
        e, r = assertion.args
        if isinstance(e, ExpIf):
            e1, e2, e3 = e.a, e.b, e.c
            return [EvalTo(e1, ValueBool(True)), EvalToErr(e3, ResErr())]


eval_ml_1_err = System(
    [EInt(), EBool(), EIfT(), EIfF(), EPlus(), EMinus(), ETimes(), ELt(), BPlus(), BMinus(), BTimes(), BLt(),
     EPlusBoolL(), EPlusBoolR(), EPlusErrorL(), EPlusErrorR(),
     EMinusBoolL(), EMinusBoolR(), EMinusErrorL(), EMinusErrorR(),
     ETimesBoolL(), ETimesBoolR(), ETimesErrorL(), ETimesErrorR(),
     ELtBoolL(), ELtBoolR(), ELtErrorL(), ELtErrorR(),
     EIfInt(), EIfError(), EIfTError(), EIfFError()])
