from Nat.data import Nat
from bases.mixins import Token, BinaryOp


class Exp(object):
    pass


class ExpNat(Exp, Token):
    def __init__(self, a: Nat):
        assert isinstance(a, Nat), type(a)
        self.a = a


class ExpPlus(Exp, BinaryOp):
    operator = '+'
    associate = 0
    precedence = 1

    def __init__(self, a: Exp, b: Exp):
        assert isinstance(a, Exp), type(a)
        assert isinstance(b, Exp), type(b)
        self.a = a
        self.b = b


class ExpTimes(Exp, BinaryOp):
    operator = '*'
    associate = 0
    precedence = 2

    def __init__(self, a: Exp, b: Exp):
        assert isinstance(a, Exp), type(a)
        assert isinstance(b, Exp), type(b)
        self.a = a
        self.b = b


if __name__ == '__main__':
    pass
