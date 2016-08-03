import logging

from EvalML2.data import Value, Exp, Env, Var
from bases.mixins import Token
from bases.util import type_checking


class ValueFn(Value, Token):
    @type_checking
    def __init__(self, env: Env, x: Var, e: Exp):
        self.env = env
        self.x = x
        self.e = e

    @type_checking
    def __str__(self) -> str:
        return r'({})[fun {} -> {}]'.format(self.env, self.x, self.e)


class ValueRec(Value, Token):
    @type_checking
    def __init__(self, env: Env, x: Var, y: Var, e: Exp):
        self.env = env
        self.x = x
        self.y = y
        self.e = e

    @type_checking
    def __str__(self) -> str:
        return r'({})[rec {} = fun {} -> {}]'.format(self.env, self.x, self.y, self.e)


class ExpFn(Exp, Token):
    @type_checking
    def __init__(self, x: Var, e: Exp):
        self.x = x
        self.e = e
        logging.debug(r'{}'.format(self.x))
        logging.debug(r'{}'.format(self.e))

    @type_checking
    def __str__(self) -> str:
        return r'fun {} -> {}'.format(self.x, self.e)


class ExpCall(Exp, Token):
    @type_checking
    def __init__(self, e1: Exp, e2: Exp):
        self.e1 = e1
        self.e2 = e2

    @type_checking
    def __str__(self) -> str:
        return r'{} {}'.format(self.e1, self.e2)


class ExpRec(Exp, Token):
    @type_checking
    def __init__(self, x: Var, y: Var, e1: Exp, e2: Exp):
        self.x = x
        self.y = y
        self.e1 = e1
        self.e2 = e2

    @type_checking
    def __str__(self) -> str:
        return r'let rec {} = fun {} -> {} in {}'.format(self.x, self.y, self.e1, self.e2)
