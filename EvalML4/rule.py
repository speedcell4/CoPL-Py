from typing import List

from EvalML3.rule import EvalToEnv, EInt, EBool, EIfT, EIfF, EPlus, EMinus, ETimes, ELt, ELet, EFun, EApp, \
    ELetRec, EAppRec, BPlus, BMinus, BTimes, BLt
from EvalML4.data import *
from bases.derivation import Assertion, Rule, System
from bases.util import type_checking


class EVar(Rule):
    name = r'E-Var'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpVar) and env[e] == v:
            return []


class ENil(Rule):
    name = r'E-Nil'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpNil) and isinstance(v, ValueNil):
            return []


class ECons(Rule):
    name = r'E-Cons'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpCons):
            e1, e2 = e.a, e.b
            v1, v2 = env[e1], env[e2]
            return [EvalToEnv(env, e1, v1), EvalToEnv(env, e2, v2)]


import logging


class EMatchNil(Rule):
    name = r'E-MatchNil'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpMatch):
            e1, e2, x, y, e3 = e.e1, e.e2, e.x, e.y, e.e3
            nil = env[e1]
            logging.debug(r'{} :: {}'.format(nil, type(nil)))
            if isinstance(nil, ValueNil):
                v = env[e2]
                return [EvalToEnv(env, e1, nil), EvalToEnv(env, e2, v)]


class EMatchCons(Rule):
    name = r'E-MatchCons'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpMatch):
            e1, e2, x, y, e3 = e.e1, e.e2, e.x, e.y, e.e3
            cons = env[e1]
            if isinstance(cons, ValueCons):
                v1, v2 = cons.v1, cons.v2
                env2 = env.update(x, v1).update(y, v2)
                v = env2[e3]
                return [EvalToEnv(env, e1, cons), EvalToEnv(env2, e3, v)]


eval_ml_4 = System([
    EInt(), EBool(), EIfT(), EIfF(), EPlus(), EMinus(), ETimes(), ELt(), EVar(), ELet(), EFun(), EApp(),
    ELetRec(), EAppRec(), ENil(), ECons(), EMatchNil(), EMatchCons(), BPlus(), BMinus(), BTimes(), BLt()])
