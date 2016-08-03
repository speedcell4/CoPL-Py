from typing import List

from EvalML1.data import Value, ValueInt, ValueBool, Exp, ExpInt, ExpBool, ExpPlus, ExpMinus, ExpTimes, ExpIf, ExpLt
from bases.mixins import Token, TrinaryOp
from bases.util import type_checking


class Var(object):
    @type_checking
    def __init__(self, name: str):
        self.name = name.strip()

    @type_checking
    def __str__(self) -> str:
        return r'{}'.format(self.name)

    @type_checking
    def __eq__(self, other: 'Var') -> 'Var':
        return self.name == other.name


class ExpVar(Exp, Token):
    @type_checking
    def __init__(self, x: Var):
        self.x = x

    @type_checking
    def __str__(self) -> str:
        return r'{}'.format(self.x)

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpVar):
            return self.x == other.x
        else:
            return False


class ExpLet(Exp, TrinaryOp):
    operator = ['let', '=', 'in']

    @type_checking
    def __init__(self, a: Var, b: Exp, c: Exp):
        self.a = a
        self.b = b
        self.c = c

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpLet):
            return (self.a, self.b, self.c) == (other.a, other.b, other.c)
        else:
            return False


class EnvItem(object):
    @type_checking
    def __init__(self, x: Var, v: Value):
        self.x = x
        self.v = v

    @type_checking
    def __str__(self) -> str:
        return r'{} = {}'.format(self.x, self.v)


class Env(object):
    @type_checking
    def __init__(self, items: List[EnvItem]):
        self.items = items

    @type_checking
    def __str__(self) -> str:
        return ', '.join(str(item) for item in self.items)

    @type_checking
    def update(self, x: Var, v: Value) -> 'Env':
        if self.items and self.items[-1].x == x:
            return Env(self.items[:-1:] + [EnvItem(x, v)])
        else:
            return Env(self.items[::] + [EnvItem(x, v)])

    @type_checking
    def __getitem__(self, x: Exp) -> Value:
        return self.__getattribute__('__getitem__{}__'.format(x.__class__.__name__))(x)

    @type_checking
    def __getitem__ExpInt__(self, e: ExpInt) -> ValueInt:
        return e.value

    @type_checking
    def __getitem__ExpBool__(self, e: ExpBool) -> ValueBool:
        return e.value

    @type_checking
    def __getitem__ExpPlus__(self, e: ExpPlus) -> ValueInt:
        a_value = self[e.a]
        b_value = self[e.b]
        assert isinstance(a_value, ValueInt)
        assert isinstance(b_value, ValueInt)
        return a_value + b_value

    @type_checking
    def __getitem__ExpMinus__(self, e: ExpMinus) -> ValueInt:
        a_value = self[e.a]
        b_value = self[e.b]
        assert isinstance(a_value, ValueInt)
        assert isinstance(b_value, ValueInt)
        return a_value - b_value

    @type_checking
    def __getitem__ExpTimes__(self, e: ExpTimes) -> ValueInt:
        a_value = self[e.a]
        b_value = self[e.b]
        assert isinstance(a_value, ValueInt)
        assert isinstance(b_value, ValueInt)
        return a_value * b_value

    @type_checking
    def __getitem__ExpLt__(self, e: ExpLt) -> ValueBool:
        a_value = self[e.a]
        b_value = self[e.b]
        assert isinstance(a_value, ValueInt)
        assert isinstance(b_value, ValueInt)
        return a_value < b_value

    @type_checking
    def __getitem__ExpIf__(self, e: ExpIf) -> Value:
        a_value = self[e.a]
        assert isinstance(a_value, ValueBool)
        if a_value.b:
            return self[e.b]
        else:
            return self[e.c]

    @type_checking
    def __getitem__ExpVar__(self, e: ExpVar) -> Value:
        for item in self.items[::-1]:
            if item.x == e.x:
                return item.v
        raise IndexError(r'{} is not in environment'.format(e))

    @type_checking
    def __getitem__ExpLet__(self, e: ExpLet) -> Value:
        return self.update(e.a, self[e.b])[e.c]
