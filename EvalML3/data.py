import logging

from EvalML2.data import *
from bases.mixins import Function
from bases.util import type_checking

__all__ = [
    'Value', 'ValueInt', 'ValueBool', 'ValueFn', 'ValueRec',
    'Exp', 'ExpInt', 'ExpBool', 'ExpPlus', 'ExpMinus', 'ExpTimes', 'ExpLt', 'ExpVar', 'ExpFn', 'ExpCall', 'ExpIf',
    'ExpLet', 'ExpRec',
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


class ExpFn(Exp, Function):
    @type_checking
    def __init__(self, x: Var, e: Exp):
        self.x = x
        self.e = e
        logging.debug(r'{}'.format(self.x))
        logging.debug(r'{}'.format(self.e))

    @type_checking
    def __str__(self) -> str:
        return r'fun {} -> {}'.format(self.x, self.e)


class ExpCall(Exp, Function):
    @type_checking
    def __init__(self, e1: Exp, e2: Exp):
        self.e1 = e1
        self.e2 = e2

    @type_checking
    def __str__(self) -> str:
        return r'{} ({})'.format(self.e1, self.e2)


class ExpRec(Exp, Function):
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
def __getitem__ExpFn__(self: Env, e: ExpFn) -> Value:
    return ValueFn(self, e.x, e.e)


Env.__getitem__ExpFn__ = __getitem__ExpFn__


@type_checking
def __getitem__ExpCall__(self, e: ExpCall) -> Value:
    logging.debug(r'ExpCall {}'.format(e))
    e1, e2 = e.e1, e.e2
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


Env.__getitem__ExpCall__ = __getitem__ExpCall__


@type_checking
def __getitem__ExpRec__(self, e: ExpRec) -> Value:
    x, y, e1, e2 = e.x, e.y, e.e1, e.e2
    return self.update(x, ValueRec(self, x, y, e1))[e2]


Env.__getitem__ExpRec__ = __getitem__ExpRec__
