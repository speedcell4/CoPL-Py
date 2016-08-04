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
            if isinstance(t, TypesUnkown):
                t.define(TypesInt())
            if isinstance(t, TypesInt):
                return []


class TBool(Rule):
    name = r'T-Bool'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpBool):
            if isinstance(t, TypesUnkown):
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
            if isinstance(t, TypesUnkown):
                t2, t3 = env[e2], env[e3]
                if t2 == t3:
                    t.define(t2)
            return [
                EvalToType(env, e1, TypesBool()),
                EvalToType(env, e2, t),
                EvalToType(env, e3, t)
            ]


class TPlus(Rule):
    name = r'T-Plus'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpPlus):
            if isinstance(t, TypesUnkown):
                t.define(TypesInt())
            if isinstance(t, TypesInt):
                e1, e2 = e.a, e.b
                return [
                    EvalToType(env, e1, t),
                    EvalToType(env, e2, t),
                ]


class TMinus(Rule):
    name = r'T-Minus'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpMinus):
            if isinstance(t, TypesUnkown):
                t.define(TypesInt())
            if isinstance(t, TypesInt):
                e1, e2 = e.a, e.b
                return [
                    EvalToType(env, e1, t),
                    EvalToType(env, e2, t),
                ]


class TTime(Rule):
    name = r'T-Times'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpTimes):
            if isinstance(t, TypesUnkown):
                t.define(TypesInt())
            if isinstance(t, TypesInt):
                e1, e2 = e.a, e.b
                return [
                    EvalToType(env, e1, t),
                    EvalToType(env, e2, t),
                ]


class TLt(Rule):
    name = r'T-Lt'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpLt):
            if isinstance(t, TypesUnkown):
                t.define(TypesBool())
            if isinstance(t, TypesBool):
                e1, e2 = e.a, e.b
                return [
                    EvalToType(env, e1, t),
                    EvalToType(env, e2, t),
                ]


class TVar(Rule):
    name = r'T-Var'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpVar):
            if isinstance(t, TypesUnkown):
                t.define(env[e])
            if env[e] == t:
                return []


class TLet(Rule):
    name = r'T-Let'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpLet):
            x, e1, e2 = e.a, e.b, e.c
            t1 = env[e1]
            t2 = env.update(x, t1)[e2]
            if isinstance(t, TypesUnkown):
                t.define(t2)
            if t == t2:
                return [
                    EvalToType(env, e1, t1),
                    EvalToType(env.update(x, t1), e2, t)
                ]


class TFun(Rule):
    name = r'T-Fun'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, fun, t = assertion.args
        if isinstance(fun, ExpFun):
            x, e = fun.x, fun.e
            if isinstance(t, TypesUnkown):
                t1, t2 = TypesUnkown(), TypesUnkown()
                t.define(TypesFun(t1, t2))
            if isinstance(t, TypesFun):
                t1, t2 = t.a, t.b
                return [
                    EvalToType(env.update(x, t1), e, t2)
                ]


class TApp(Rule):
    name = r'T-App'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpApp):
            e1, e2 = e.e1, e.e2
            t12 = env[e1]
            t1 = env[e2]
            if isinstance(t, TypesUnkown):
                if isinstance(t12, TypesFun):
                    if t12.a == t1:
                        t.define(t12.b)
            if isinstance(t12, TypesFun):
                if t12.a == t1:
                    return [
                        EvalToType(env, e1, TypesFun(t1, t)),
                        EvalToType(env, e2, t1)
                    ]


class TLetRec(Rule):
    name = r'T-LetRec'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpLetRec):
            x, y, e1, e2 = e.x, e.y, e.e1, e.e2
            t1 = TypesUnkown()
            t2 = TypesUnkown()
            if isinstance(t, TypesUnkown):
                if env.update(x, TypesFun(t1, t2)).update(t, t1)[e1] == t2:
                    t.define(env.update(x, TypesFun(t1, t2))[e2])
            if env.update(x, TypesFun(t1, t2))[e2] == t:
                return [
                    EvalToType(env.update(x, TypesFun(t1, t2)).update(y, t1), e1, t2),
                    EvalToType(env.update(x, TypesFun(t1, t2)), e2, t)
                ]


class TNil(Rule):
    name = r'T-Nil'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpNil):
            if isinstance(t, TypesUnkown):
                t.define(TypesList(TypesUnkown()))
            if isinstance(t, TypesList):
                return []


class TCons(Rule):
    name = r'T-Cons'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpCons):
            e1, e2 = e.a, e.b
            t1 = env[e1]
            t2 = env[e2]
            if isinstance(t, TypesUnkown):
                if isinstance(t2, TypesList):
                    if t1 == t2.a:
                        t.define(t1)
            if isinstance(t, TypesList):
                if isinstance(t2, TypesList):
                    if t1 == t2.a:
                        return [
                            EvalToType(env, e1, t.a),
                            EvalToType(env, e2, t),
                        ]


class TMatch(Rule):
    name = r'T-Match'

    @type_checking
    def __call__(self, assertion: EvalToType) -> List[Assertion]:
        env, e, t = assertion.args
        if isinstance(e, ExpMatch):
            e1, e2, x, y, e3 = e.e1, e.e2, e.x, e.y, e.e3
            t1, t2 = env[e1], env[e2]
            if isinstance(t, TypesUnkown):
                if env.update(x, t1).update(y, TypesList(t1))[e3] == t2:
                    t.define(t2)
            if isinstance(t1, TypesList):
                if env.update(x, t1).update(y, TypesList(t1))[e3] == t2:
                    return [
                        EvalToType(env, e1, t1),
                        EvalToType(env, e2, t),
                        EvalToType(env.update(x, t1.a).update(y, t1), e3, t)
                    ]


typing_ml_4 = System([
    TInt(), TBool(), TIf(), TPlus(), TMinus(), TTime(), TLt(),
    TVar(), TLet(), TFun(), TApp(), TLetRec(), TNil(), TCons(), TMatch()
])
