import logging
from typing import List

from TypingML4.data import Env, Exp, Types, ExpInt, ExpBool, TypesInt, TypesBool, TypesFun, TypesList, \
    ExpIf, \
    ExpLet, ExpPlus, ExpMatch, ExpMinus, ExpTimes, ExpCons, ExpNil, ExpApp, ExpFun, ExpLetRec, ExpLt, ExpVar, \
    TypesUnkown
from bases.derivation import Assertion, Rule, System
from bases.util import type_checking


class EvalToType(Assertion):
    template = r'{} |- {} : {}'

    @type_checking
    def __init__(self, env: Env, e: Exp, t: Types):
        self.args = (env, e, t)


class TInt(Rule):
    name = r'T-Int'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        logging.debug(r'TInt: {}'.format(assertion))
        if isinstance(e, ExpInt):
            t.define(TypesInt())
            if isinstance(t, TypesInt):
                return []


class TBool(Rule):
    name = r'T-Bool'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpBool):
            t.define(TypesBool())
            if isinstance(t, TypesBool):
                return []


class TIf(Rule):
    name = r'T-If'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpIf):
            e1, e2, e3 = e.a, e.b, e.c
            t1, t2, t3, tb = env[e1], env[e2], env[e3], TypesBool()

            t1.define(tb)
            t2.define(t3)
            t3.define(t2)

            if t2 == t3:
                t.define(t2)
                return [
                    EvalToType(env, e1, t1),
                    EvalToType(env, e2, t2),
                    EvalToType(env, e3, t3),
                ]


class TPlus(Rule):
    name = r'T-Plus'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpPlus):
            e1, e2 = e.a, e.b
            t1, t2, ti = env[e1], env[e2], TypesInt()

            t1.define(ti)
            t2.define(ti)
            t.define(ti)

            return [
                EvalToType(env, e1, t1),
                EvalToType(env, e2, t2),
            ]


class TMinus(Rule):
    name = r'T-Minus'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpMinus):
            e1, e2 = e.a, e.b
            t1, t2, ti = env[e1], env[e2], TypesInt()

            t1.define(ti)
            t2.define(ti)
            t.define(ti)

            return [
                EvalToType(env, e1, t1),
                EvalToType(env, e2, t2),
            ]


class TTime(Rule):
    name = r'T-Times'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpTimes):
            e1, e2 = e.a, e.b
            t1, t2, ti = env[e1], env[e2], TypesInt()

            t1.define(ti)
            t2.define(ti)
            t.define(ti)

            return [
                EvalToType(env, e1, t1),
                EvalToType(env, e2, t2),
            ]


class TLt(Rule):
    name = r'T-Lt'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpLt):
            e1, e2 = e.a, e.b
            t1, t2, ti, tb = env[e1], env[e2], TypesInt(), TypesBool()

            t1.define(ti)
            t2.define(ti)
            t.define(tb)

            return [
                EvalToType(env, e1, t1),
                EvalToType(env, e2, t2),
            ]


class TVar(Rule):
    name = r'T-Var'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpVar):
            t.define(env[e])
            if env[e] == t:
                return []


class TLet(Rule):
    name = r'T-Let'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        logging.debug(r'TLet *')
        if isinstance(e, ExpLet):
            logging.debug(r'TLet **')
            x, e1, e2 = e.a, e.b, e.c
            logging.debug(r'TLet e1 = {}, e2 = {}'.format(e1, e2))
            t1 = env[e1]
            logging.debug(r'TLet[e1] {} :: {}'.format(e1, t1))
            t2 = env.update(x, t1)[e2]
            logging.debug(r'TLet[e2] {} :: {}'.format(e2, t2))
            t.define(t2)
            logging.debug(r'TLet {} <-> {}'.format(t, t2))
            return [
                EvalToType(env, e1, t1),
                EvalToType(env.update(x, t1), e2, t)
            ]


class TFun(Rule):
    name = r'T-Fun'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, fun, t = assertion.args
        logging.debug(r'TFun*')
        if isinstance(fun, ExpFun):
            logging.debug(r'TFun**')
            x, e = fun.x, fun.e
            t1 = TypesUnkown()
            t2 = env.update(x, t1)[e]
            t.define(TypesFun(t1, t2))
            return [
                EvalToType(env.update(x, t1), e, t2)
            ]


class TApp(Rule):
    name = r'T-App'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t2 = assertion.args
        if isinstance(e, ExpApp):
            e1, e2 = e.e1, e.e2
            t12, t1 = env[e1], env[e2]

            if isinstance(t12, TypesUnkown):
                t12.define(TypesFun(t1, t2))

            if isinstance(t1, TypesUnkown) and isinstance(t12, TypesFun):
                t1.define(t12.a)

            if isinstance(t2, TypesUnkown) and isinstance(t12, TypesFun):
                t2.define(t12.b)

            return [
                EvalToType(env, e1, t12),
                EvalToType(env, e2, t1),
            ]


class TLetRec(Rule):
    name = r'T-LetRec'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpLetRec):
            x, y, e1, e2 = e.x, e.y, e.e1, e.e2
            t1, t2 = TypesUnkown(), TypesUnkown()
            t12 = TypesFun(t1, t2)
            t2.define(env.update(x, t12).update(y, t1)[e1])
            t.define(env.update(x, t12)[e2])
            return [
                EvalToType(env.update(x, t12).update(y, t1), e1, t2),
                EvalToType(env.update(x, t12), e2, t),
            ]


class TNil(Rule):
    name = r'T-Nil'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpNil):
            t.define(TypesList(TypesUnkown()))
            if isinstance(t, TypesList):
                return []


class TCons(Rule):
    name = r'T-Cons'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, ts = assertion.args
        logging.debug(r'T-Cons*')
        if isinstance(e, ExpCons):
            logging.debug(r'T-Cons**')
            e1, e2 = e.a, e.b
            t, ts_ = env[e1], env[e2]

            ts_.define(TypesList(t))
            ts.define(TypesList(t))
            if isinstance(ts, TypesList):
                t.define(ts.a)
            if isinstance(ts_, TypesList):
                t.define(ts_.a)

            logging.debug(r'T-Cons: final')
            logging.debug(r'T-Cons: {} :: {}'.format(e1, t))
            logging.debug(r'T-Cons: {} :: {}'.format(e2, ts_))
            logging.debug(r'T-Cons: {} '.format(ts))

            if t == ts_.a == ts.a:
                return [
                    EvalToType(env, e1, t),
                    EvalToType(env, e2, ts_),
                ]


class TMatch(Rule):
    name = r'T-Match'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpMatch):
            e1, e2, x, y, e3 = e.e1, e.e2, e.x, e.y, e.e3
            t1s, t2 = env[e1], env[e2]
            t1 = TypesUnkown()
            t1s.define(TypesList(t1))
            t2.define(env.update(x, t1).update(y, t1s)[e3])
            t.define(t2)
            return [
                EvalToType(env, e1, t1s),
                EvalToType(env, e2, t2),
                EvalToType(env.update(x, t1).update(y, t1s), e3, t2)
            ]


typing_ml_4 = System([
    TInt(), TBool(), TIf(), TPlus(), TMinus(), TTime(), TLt(),
    TVar(), TLet(), TFun(), TApp(), TLetRec(), TNil(), TCons(), TMatch()
])
