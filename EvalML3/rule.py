import logging
from typing import List

from EvalML2.rule import Assertion, Rule, System, EvalToEnv, EInt, EBool, EIfT, EIfF, EPlus, EMinus, ETimes, ELt, EVar1, \
    EVar2, ELet, BPlus, BMinus, BTimes, BLt
from EvalML3.data import ExpFun, ExpApp, ExpLetRec, ValueFn, ValueRec
from bases.util import type_checking


class EFun(Rule):
    name = r'E-Fun'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpFun) and isinstance(v, ValueFn):
            logging.debug(r'EFun => {} {} {}'.format(env, e, v))
            logging.info(r'{} == {}, {}'.format(env, v.env, env == v.env))
            if (env, e.x, e.e) == (v.env, v.x, v.e):
                return []


class EApp(Rule):
    name = r'E-App'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        logging.debug(r'EApp: {} |- {} evalto {}'.format(env, e, v))

        if isinstance(e, ExpApp):
            e1, e2 = e.a, e.b
            v1, v2 = env[e1], env[e2]
            if isinstance(v1, ValueFn):
                env2, x, e0 = v1.env, v1.x, v1.e
                return [EvalToEnv(env, e1, ValueFn(env2, x, e0)),
                        EvalToEnv(env, e2, v2),
                        EvalToEnv(env2.update(x, v2), e0, v)]


class ELetRec(Rule):
    name = r'E-LetRec'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpLetRec):
            x, y, e1, e2 = e.x, e.y, e.e1, e.e2
            return [EvalToEnv(env.update(x, ValueRec(env, x, y, e1)), e2, v)]


class EAppRec(Rule):
    name = r'E-AppRec'

    @type_checking
    def __call__(self, assertion: EvalToEnv) -> List[Assertion]:
        env, e, v = assertion.args
        if isinstance(e, ExpApp):
            e1, e2 = e.a, e.b
            v1, v2 = env[e1], env[e2]
            if isinstance(v1, ValueRec):
                env2, x, y, e0 = v1.env, v1.x, v1.y, v1.e
                return [EvalToEnv(env, e1, ValueRec(env2, x, y, e0)),
                        EvalToEnv(env, e2, v2),
                        EvalToEnv(env2.update(x, ValueRec(env2, x, y, e0)).update(y, v2), e0, v)]


eval_ml_3 = System([
    EInt(), EBool(), EIfT(), EIfF(), EPlus(), EMinus(), ETimes(), ELt(), EVar1(), EVar2(), ELet(), EFun(), EApp(),
    ELetRec(), EAppRec(), BPlus(), BMinus(), BTimes(), BLt()
])
