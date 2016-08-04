from EvalML3.data import *
from bases.mixins import Token, BinaryOp, BaseToken
from bases.util import type_checking

__all__ = [
    'Value', 'ValueInt', 'ValueBool', 'ValueFn', 'ValueRec', 'ValueNil', 'ValueCons',
    'Exp', 'ExpInt', 'ExpBool', 'ExpPlus', 'ExpMinus', 'ExpTimes', 'ExpLt', 'ExpVar', 'ExpFun', 'ExpApp', 'ExpIf',
    'ExpLet', 'ExpLetRec', 'ExpNil', 'ExpCons', 'ExpMatch',
    'Env', 'EnvItem', 'Var'
]


class ValueNil(Value, Token):
    @type_checking
    def __str__(self) -> str:
        return r'[]'

    @type_checking
    def __eq__(self, other: 'Value') -> bool:
        return isinstance(other, ValueNil)


class ValueCons(Value, Token):
    @type_checking
    def __eq__(self, other: 'Value') -> bool:
        if isinstance(other, ValueCons):
            return (self.v1, self.v2) == (other.v1, other.v2)
        else:
            return False

    @type_checking
    def __init__(self, v1: Value, v2: Value):
        self.v1 = v1
        self.v2 = v2

    @type_checking
    def __str__(self) -> str:
        return r'({} :: {})'.format(self.v1, self.v2)


class ExpNil(Exp, Token):
    @property
    def value(self) -> Value:
        raise NotImplementedError

    @type_checking
    def __str__(self) -> str:
        return r'[]'


@type_checking
def __getitem__ExpNil__(self: Env, e: ExpNil) -> Value:
    return ValueNil()


Env.__getitem__ExpNil__ = __getitem__ExpNil__


class ExpCons(Exp, BinaryOp):
    operator = r'::'

    associate = 1
    precedence = 10

    @type_checking
    def __init__(self, a: Exp, b: Exp):
        self.a = a
        self.b = b

    @property
    def value(self) -> Value:
        raise NotImplementedError

    @type_checking
    def __str__(self) -> str:
        return r'({} {} {})'.format(self.sub(0), self.operator, self.sub(1))


@type_checking
def __getitem__ExpCons__(self: Env, e: ExpCons) -> Value:
    e1, e2 = e.a, e.b
    v1, v2 = self[e1], self[e2]
    return ValueCons(v1, v2)


Env.__getitem__ExpCons__ = __getitem__ExpCons__


class ExpMatch(Exp, BaseToken):
    @type_checking
    def __init__(self, e1: Exp, e2: Exp, x: Var, y: Var, e3: Exp):
        self.e1 = e1
        self.e2 = e2
        self.x = x
        self.y = y
        self.e3 = e3

    def __str__(self) -> str:
        return r'match {} with [] -> {} | {} :: {} -> {}'.format(self.e1, self.e2, self.x, self.y, self.e3)

    def sub(self, index: int) -> str:
        pass

    @property
    def value(self) -> Value:
        raise NotImplementedError


@type_checking
def __getitem__ExpMatch__(self: Env, e: ExpMatch) -> Value:
    e1, e2, x, y, e3 = e.e1, e.e2, e.x, e.y, e.e3
    v0 = self[e1]
    if isinstance(v0, ValueNil):
        return self[e2]
    elif isinstance(v0, ValueCons):
        v1, v2 = v0.v1, v0.v2
        return self.update(x, v1).update(y, v2)[e3]
    else:
        raise ValueError(r'what is {}'.format(e1))


Env.__getitem__ExpMatch__ = __getitem__ExpMatch__
