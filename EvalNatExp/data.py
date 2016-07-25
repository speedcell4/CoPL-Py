from Nat.data import Nat
from bases.mixins import Token, BinaryOp


class Exp(object):
    @property
    def value(self) -> Nat:
        raise NotImplementedError


class ExpNat(Exp, Token):
    def __init__(self, a: Nat):
        assert isinstance(a, Nat), type(a)
        self.a = a

    @property
    def value(self) -> Nat:
        return self.a


class ExpPlus(Exp, BinaryOp):
    operator = '+'
    associate = 0
    precedence = 1

    def __init__(self, a: Exp, b: Exp):
        assert isinstance(a, Exp), type(a)
        assert isinstance(b, Exp), type(b)
        self.a = a
        self.b = b

    @property
    def value(self) -> Nat:
        return self.a.value + self.b.value


class ExpTimes(Exp, BinaryOp):
    operator = '*'
    associate = 0
    precedence = 2

    def __init__(self, a: Exp, b: Exp):
        assert isinstance(a, Exp), type(a)
        assert isinstance(b, Exp), type(b)
        self.a = a
        self.b = b

    @property
    def value(self) -> Nat:
        return self.a.value * self.b.value


if __name__ == '__main__':
    pass
