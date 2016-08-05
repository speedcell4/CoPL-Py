import logging
from typing import List

from EvalML4.data import Var, Exp, ExpInt, ExpBool, ExpIf, ExpPlus, ExpMinus, ExpTimes, ExpLt, ExpLet, ExpVar, ExpFun, \
    ExpApp, ExpLetRec, ExpNil, ExpCons, ExpMatch
from bases.mixins import Token, UnaryOp, BinaryOp
from bases.util import type_checking


# __all__ = [
#     'Value', 'ValueInt', 'ValueBool', 'ValueFn', 'ValueRec', 'ValueNil', 'ValueCons',
#     'Exp', 'ExpInt', 'ExpBool', 'ExpPlus', 'ExpMinus', 'ExpTimes', 'ExpLt', 'ExpVar', 'ExpFun', 'ExpApp', 'ExpIf',
#     'ExpLet', 'ExpLetRec', 'ExpNil', 'ExpCons', 'ExpMatch',
#     'Env', 'EnvItem', 'Var',
#     'Types', 'TypesInt', 'TypesBool', 'TypesFun', 'TypesList',
# ]


class Types(object):
    def __eq__(self, other: 'Types') -> bool:
        raise NotImplementedError

    def define(self, other: 'Types'):
        raise NotImplementedError

    @type_checking
    def get_from(self, other: 'Types'):
        self.__class__ = other.__class__
        self.__dict__ = other.__dict__


class TypesUnkown(Types):
    @type_checking
    def __eq__(self, other: 'Types') -> bool:
        return isinstance(other, TypesUnkown)

    @type_checking
    def define(self, other: 'Types'):
        self.get_from(other)

    @type_checking
    def __str__(self) -> str:
        return r'TypeUnkown'


class TypesInt(Types, Token):
    @type_checking
    def define(self, other: 'Types'):
        if isinstance(other, TypesUnkown):
            other.define(self)
        elif isinstance(other, TypesInt):
            pass

    @type_checking
    def __eq__(self, other: 'Types') -> bool:
        return isinstance(other, TypesInt)

    @type_checking
    def __str__(self) -> str:
        return r'int'


class TypesBool(Types, Token):
    @type_checking
    def define(self, other: 'Types'):
        if isinstance(other, TypesUnkown):
            other.define(self)
        elif isinstance(other, TypesBool):
            pass

    @type_checking
    def __eq__(self, other: 'Types') -> bool:
        return isinstance(other, TypesBool)

    @type_checking
    def __str__(self) -> str:
        return r'bool'


class TypesFun(Types, BinaryOp):
    operator = r'->'

    associate = 1
    precedence = 1

    @type_checking
    def define(self, other: 'Types'):
        if isinstance(other, TypesUnkown):
            other.define(self)
        elif isinstance(other, TypesFun):
            self.a.define(other.a)
            self.b.define(other.b)

    @type_checking
    def __init__(self, a: Types, b: Types):
        self.a = a
        self.b = b

    @type_checking
    def __eq__(self, other: 'Types') -> bool:
        if isinstance(other, TypesFun):
            return (self.a, self.b) == (other.a, other.b)
        else:
            return False

    @type_checking
    def sub(self, index: int) -> str:
        child = [self.a, self.b][index]

        if isinstance(child, TypesFun):
            return r'({})'.format(child)
        else:
            return r'{}'.format(child)


class TypesList(Types, UnaryOp):
    @type_checking
    def define(self, other: 'Types'):
        if isinstance(other, TypesUnkown):
            other.define(self)
        elif isinstance(other, TypesFun):
            self.a.define(other.a)

    @type_checking
    def __init__(self, a: Types):
        self.a = a

    @type_checking
    def __str__(self) -> str:
        return r'{} list'.format(self.sub(0))

    def sub(self, index: int) -> str:
        return r'{}'.format(self.a)

    @type_checking
    def __eq__(self, other: 'Types') -> bool:
        if isinstance(other, TypesList):
            return self.a == other.a
        else:
            return False


class EnvItem(object):
    @type_checking
    def __init__(self, x: Var, t: Types):
        self.x = x
        self.t = t

    @type_checking
    def __str__(self) -> str:
        return r'{} : {}'.format(self.x, self.t)

    @type_checking
    def __eq__(self, other: 'EnvItem') -> bool:
        return (self.x, self.t) == (other.x, other.t)


class Env(object):
    @type_checking
    def __init__(self, items: List[EnvItem]):
        self.items = items

    @type_checking
    def __eq__(self, other: 'Env') -> bool:
        return self.items == other.items

    @type_checking
    def __str__(self) -> str:
        # logging.debug(r'Env: ({}) items'.format(len(self.items)))
        return ','.join(str(item) for item in self.items)

    @type_checking
    def update(self, x: Var, t: Types):
        return Env(self.items + [EnvItem(x, t)])

    @type_checking
    def __getitem__(self, x: Exp) -> Types:
        logging.debug(r'disptch {} :: {}'.format(x, type(x)))
        return self.__getattribute__('__getitem__{}__'.format(x.__class__.__name__))(x)

    @type_checking
    def __getitem__ExpInt__(self, e: ExpInt) -> TypesInt:
        return TypesInt()

    @type_checking
    def __getitem__ExpBool__(self, e: ExpBool) -> TypesBool:
        return TypesBool()

    @type_checking
    def __getitem__ExpIf__(self, e: ExpIf) -> Types:
        e1, e2, e3 = e.a, e.b, e.c
        t1, t2, t3, tb = self[e1], self[e2], self[e3], TypesBool()

        t1.define(tb)
        t2.define(t3)
        t3.define(t2)

        if isinstance(t1, TypesBool):
            if t2 == t3:
                return t2
            else:
                raise TypeError(r'{} :: {} and {} :: {} should be same type'.format(e2, t2, e3, t3))
        else:
            raise TypeError(r'{} :: {} should be TypeBool'.format(e1, t1))

    @type_checking
    def __getitem__ExpPlus__(self, e: ExpPlus) -> TypesInt:
        e1, e2 = e.a, e.b
        t1, t2, ti = self[e1], self[e2], TypesInt()

        t1.define(ti)
        t2.define(ti)

        if not isinstance(t1, TypesInt):
            raise TypeError(r'{} :: {} should be TypeInt-l'.format(e1, t1))
        if not isinstance(t2, TypesInt):
            raise TypeError(r'{} :: {} should be TypeInt-r'.format(e2, t2))
        return ti

    @type_checking
    def __getitem__ExpMinus__(self, e: ExpMinus) -> TypesInt:
        e1, e2 = e.a, e.b
        t1, t2, ti = self[e1], self[e2], TypesInt()

        if isinstance(t1, TypesUnkown):
            t1.define(ti)
        if isinstance(t2, TypesUnkown):
            t2.define(ti)

        if not isinstance(t1, TypesInt):
            raise TypeError(r'{} :: {} should be TypeInt-l'.format(e1, t1))
        if not isinstance(t2, TypesInt):
            raise TypeError(r'{} :: {} should be TypeInt-r'.format(e2, t2))
        return ti

    @type_checking
    def __getitem__ExpTimes__(self, e: ExpTimes) -> TypesInt:
        e1, e2 = e.a, e.b
        t1, t2, ti = self[e1], self[e2], TypesInt()

        if isinstance(t1, TypesUnkown):
            t1.define(ti)
        if isinstance(t2, TypesUnkown):
            t2.define(ti)

        if not isinstance(t1, TypesInt):
            raise TypeError(r'{} :: {} should be TypeInt-l'.format(e1, t1))
        if not isinstance(t2, TypesInt):
            raise TypeError(r'{} :: {} should be TypeInt-r'.format(e2, t2))
        return ti

    @type_checking
    def __getitem__ExpLt__(self, e: ExpLt) -> TypesBool:
        e1, e2 = e.a, e.b
        t1, t2, ti, tb = self[e1], self[e2], TypesInt(), TypesBool()

        if isinstance(t1, TypesUnkown):
            t1.define(ti)
        if isinstance(t2, TypesUnkown):
            t2.define(ti)

        if not isinstance(t1, TypesInt):
            raise TypeError(r'{} :: {} should be TypeInt-l'.format(e1, t1))
        if not isinstance(t2, TypesInt):
            raise TypeError(r'{} :: {} should be TypeInt-r'.format(e2, t2))

        return tb

    @type_checking
    def __getitem__ExpVar__(self, e: ExpVar) -> Types:
        for item in self.items[::-1]:
            if item.x == e.x:
                return item.t
        raise IndexError(r'{} is not in enviroment'.format(e))

    @type_checking
    def __getitem__ExpLet__(self, e: ExpLet) -> Types:
        x, e1, e2 = e.a, e.b, e.c
        t1 = self[e1]
        return self.update(x, t1)[e2]

    @type_checking
    def __getitem__ExpFun__(self, e: ExpFun) -> Types:
        x, e = e.x, e.e
        t1 = TypesUnkown()
        t2 = self.update(x, t1)[e]
        return TypesFun(t1, t2)

    @type_checking
    def __getitem__ExpApp__(self, e: ExpApp) -> Types:
        e1, e2 = e.e1, e.e2
        t12, t1, t2 = self[e1], self[e2], TypesUnkown()

        t12.define(TypesFun(t1, t2))

        if isinstance(t12, TypesFun):
            t1.define(t12.a)
            if t12.a == t1:
                return t12.b

        logging.debug(r'ExpApp {} :: {} . {}'.format(e1, t12.a, t12.b))
        logging.debug(r'ExpApp {} :: {}'.format(e2, t1))

        raise TypeError('{} :: {} can not be applied to {} :: {}'.format(e2, t1, e1, t12))

    @type_checking
    def __getitem__ExpLetRec__(self, e: ExpLetRec) -> Types:
        x, y, e1, e2 = e.x, e.y, e.e1, e.e2
        t1, t2 = TypesUnkown(), TypesUnkown()
        tx = TypesFun(t1, t2)
        if self.update(x, tx).update(y, t1)[e1] == t2:
            return self.update(x, tx)[e2]

    @type_checking
    def __getitem__ExpNil__(self, e: ExpNil) -> Types:
        return TypesList(TypesUnkown())

    @type_checking
    def __getitem__ExpCons__(self, e: ExpCons) -> Types:
        e1, e2 = e.a, e.b
        t1, t2s = self[e1], self[e2]

        t2s.define(TypesList(t1))

        if isinstance(t2s, TypesList):
            t1.define(t2s.a)
            logging.debug(r'__getitem__ExpCons__[e1]: {} :: {}'.format(e1, t1))
            logging.debug(r'__getitem__ExpCons__[e2]: {} :: {}'.format(e2, t2s))
            if t1 == t2s.a:
                return t2s
        raise TypeError(r'{} :: {} could not cons {} :: {}'.format(e1, t1, e2, t2s))

    @type_checking
    def __getitem__ExpMatch__(self, e: ExpMatch) -> Types:
        e1, e2, x, y, e3 = e.e1, e.e2, e.x, e.y, e.e3
        t_s, t = self[e1], self[e2]

        t_s.define(TypesList(TypesUnkown()))

        if isinstance(t_s, TypesList):
            t3 = self.update(x, t_s.a).update(y, t_s)[e3]
            t.define(t3)
            if t == t3:
                return t
        raise TypeError(r'{} :: {} could not match {} :: {} or {} :: {}'.format(e1, t_s, e2, t, e3, t))


if __name__ == '__main__':
    print(TypesFun(TypesBool(), TypesInt()))
