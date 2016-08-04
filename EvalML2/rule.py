import logging
from typing import List

from EvalML1.rule import PlusIs, MinusIs, TimesIs, LtIs, BPlus, BMinus, BTimes, BLt
from EvalML2.data import Env, Value, ValueInt, ValueBool, Exp, ExpInt, ExpBool, ExpVar, ExpPlus, ExpMinus, ExpTimes, \
    ExpLet, ExpLt, ExpIf
from bases.deduction import Assertion, Rule, System
from bases.util import type_checking


class EvalToEnv(Assertion):
    template = r'{} |- {} evalto {}'

    @type_checking
    def __init__(self, env: Env, e: Exp, v: Value):
        self.args = (env, e, v)


class EInt(Rule):
    name = r'E-Int'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpInt) and isinstance(v, ValueInt):
            if e.i == v.i:
                return []


class EBool(Rule):
    name = r'E-Bool'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpBool) and isinstance(v, ValueBool):
            if e.b == v.b:
                return []


class EVar1(Rule):
    name = r'E-Var1'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        logging.debug(r'EVar1: {} |- {} -> {}'.format(env, e, v))
        if isinstance(e, ExpVar) and env.items:
            logging.debug(r'EVar1: 2 :: {} {} '.format(env.items[-1].x, e))
            if env.items[-1].x == e.x and env.items[-1].v == v:
                logging.debug(r'EVar1: ok')
                return []


class EVar2(Rule):
    name = r'E-Var2'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpVar) and env.items:
            if env.items[-1].x != e.x:
                return [EvalToEnv(Env(env.items[:-1]), e, v)]


class EPlus(Rule):
    name = r'E-Plus'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        logging.debug(r'EPlus => {}, {}, {}'.format(env, e, v))
        logging.debug(r'EPlus => {} {} {} {}'.format(type(e), ExpPlus, type(v), ValueInt))
        if isinstance(e, ExpPlus) and isinstance(v, ValueInt):
            logging.debug('EPlus: 1')
            e1, e2 = e.a, e.b
            logging.debug('EPlus: ({})::{} + ({})::{}'.format(e1, type(e1), e2, type(e2)))
            try:
                i1, i2, i3 = env[e1], env[e2], v
            except Exception as error:
                logging.exception(error)
            logging.debug('EPlus: 2')
            if isinstance(i1, ValueInt) and isinstance(i2, ValueInt):
                logging.debug('EPlus: 3')
                return [EvalToEnv(env, e1, i1), EvalToEnv(env, e2, i2), PlusIs(i1, i2, i3)]


class EMinus(Rule):
    name = r'E-Minus'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpMinus) and isinstance(v, ValueInt):
            e1, e2 = e.a, e.b
            i1, i2, i3 = env[e1], env[e2], v
            if isinstance(i1, ValueInt) and isinstance(i2, ValueInt):
                return [EvalToEnv(env, e1, i1), EvalToEnv(env, e2, i2), MinusIs(i1, i2, i3)]


class ETimes(Rule):
    name = r'E-Times'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpTimes) and isinstance(v, ValueInt):
            e1, e2 = e.a, e.b
            i1, i2, i3 = env[e1], env[e2], v
            if isinstance(i1, ValueInt) and isinstance(i2, ValueInt):
                return [EvalToEnv(env, e1, i1), EvalToEnv(env, e2, i2), TimesIs(i1, i2, i3)]


class ELt(Rule):
    name = r'E-Lt'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpLt) and isinstance(v, ValueBool):
            e1, e2 = e.a, e.b
            i1, i2, b3 = env[e1], env[e2], v
            if isinstance(i1, ValueInt) and isinstance(i2, ValueInt):
                return [EvalToEnv(env, e1, i1), EvalToEnv(env, e2, i2), LtIs(i1, i2, b3)]


class EIfT(Rule):
    name = r'E-IfT'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpIf):
            e1, e2, e3 = e.a, e.b, e.c
            return [EvalToEnv(env, e1, ValueBool(True)), EvalToEnv(env, e2, v)]


class EIfF(Rule):
    name = r'E-IfF'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpIf):
            e1, e2, e3 = e.a, e.b, e.c
            return [EvalToEnv(env, e1, ValueBool(False)), EvalToEnv(env, e3, v)]


class ELet(Rule):
    name = r'E-Let'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpLet):
            x, e1, e2 = e.a, e.b, e.c
            v1 = env[e1]
            return [EvalToEnv(env, e1, v1), EvalToEnv(env.update(x, v1), e2, v)]


eval_ml_2 = System([
    EInt(), EBool(), EVar1(), EVar2(), EPlus(), EMinus(), ETimes(), ELt(), EIfT(), EIfF(),
    ELet(), BPlus(), BMinus(), BTimes(), BLt()
])
