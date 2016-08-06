import logging

from EvalML2.data import *
from bases.mixins import Function, BinaryOp, Token
from bases.util import type_checking

__all__ = [
    'Value', 'ValueInt', 'ValueBool', 'ValueFn', 'ValueRec',
    'Exp', 'ExpInt', 'ExpBool', 'ExpPlus', 'ExpMinus', 'ExpTimes', 'ExpLt', 'ExpVar', 'ExpFun', 'ExpApp', 'ExpIf',
    'ExpLet', 'ExpLetRec',
    'Env', 'EnvItem', 'Var'
]


class ValueFn(Value, Function):
    @type_checking
    def __init__(self, env: Env, x: Var, e: Exp):
        self.env = env
        self.x = x
        self.e = e

    @type_checking
    def __str__(self) -> str:
        return r'({})[fun {} -> {}]'.format(self.env, self.x, self.e)

    @type_checking
    def __eq__(self, other: 'ValueFn') -> bool:
        return (self.env, self.x, self.e) == (other.env, other.x, other.e)


class ValueRec(Value, Function):
    @type_checking
    def __init__(self, env: Env, x: Var, y: Var, e: Exp):
        self.env = env
        self.x = x
        self.y = y
        self.e = e

    @type_checking
    def __str__(self) -> str:
        return r'({})[rec {} = fun {} -> {}]'.format(self.env, self.x, self.y, self.e)

    @type_checking
    def __eq__(self, other: 'ValueRec') -> bool:
        return (self.env, self.x, self.y, self.e) == (other.env, other.x, other.y, other.e)


class ExpFun(Exp, Function):
    @type_checking
    def __init__(self, x: Var, e: Exp):
        self.x = x
        self.e = e
        logging.debug(r'{}'.format(self.x))
        logging.debug(r'{}'.format(self.e))

    @type_checking
    def __str__(self) -> str:
        return r'fun {} -> {}'.format(self.x, self.e)


class ExpApp(Exp, BinaryOp):
    precedence = 100000
    associate = 1

    operator = r''

    @type_checking
    def __init__(self, a: Exp, b: Exp):
        self.a = a
        self.b = b

    @type_checking
    def __str__(self) -> str:
        return r'{} {}'.format(self.sub(0), self.sub(1))

    @type_checking
    def sub(self, index: int) -> str:
        if index == 0:
            if isinstance(self.a, (ExpVar, ExpApp)):
                return r'{}'.format(self.a)
            else:
                return r'({})'.format(self.a)
        else:
            if isinstance(self.b, Token) and not isinstance(self.b, Function):
                return r'{}'.format(self.b)
            else:
                return r'({})'.format(self.b)


class ExpLetRec(Exp, Function):
    @type_checking
    def __init__(self, x: Var, y: Var, e1: Exp, e2: Exp):
        self.x = x
        self.y = y
        self.e1 = e1
        self.e2 = e2

    @type_checking
    def __str__(self) -> str:
        return r'let rec {} = fun {} -> {} in {}'.format(self.x, self.y, self.e1, self.e2)


@type_checking
def __getitem__ExpFun__(self: Env, e: ExpFun) -> Value:
    return ValueFn(self, e.x, e.e)


Env.__getitem__ExpFun__ = __getitem__ExpFun__


@type_checking
def __getitem__ExpApp__(self, e: ExpApp) -> Value:
    logging.debug(r'ExpCall {}'.format(e))
    e1, e2 = e.a, e.b
    logging.debug(r'ExpCall {} {} {} {}'.format(e1, type(e1), e2, type(e2)))
    v1, v2 = self[e1], self[e2]
    logging.debug(r'ExpCall {} {} {} {}'.format(v1, type(v1), v2, type(v2)))
    if isinstance(v1, ValueFn):
        env2, x, e0 = v1.env, v1.x, v1.e
        return env2.update(x, v2)[e0]
    elif isinstance(v1, ValueRec):
        env2, x, y, e0 = v1.env, v1.x, v1.y, v1.e
        return env2.update(x, ValueRec(env2, x, y, e0)).update(y, v2)[e0]
    else:
        raise ValueError(r'{} is not a ValueFn or ValueRec'.format(e1))


Env.__getitem__ExpApp__ = __getitem__ExpApp__


@type_checking
def __getitem__ExpLetRec__(self, e: ExpLetRec) -> Value:
    x, y, e1, e2 = e.x, e.y, e.e1, e.e2
    return self.update(x, ValueRec(self, x, y, e1))[e2]


Env.__getitem__ExpLetRec__ = __getitem__ExpLetRec__
