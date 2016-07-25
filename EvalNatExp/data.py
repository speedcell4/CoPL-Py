from Nat.data import Nat
from bases.mixins import Token, BinaryOp
from bases.derivation import DeductionError


class Exp(object):
    def __eq__(self, other: 'Exp') -> bool:
        raise NotImplementedError

    @property
    def value(self) -> Nat:
        raise NotImplementedError

    def one_step(self, other: 'Exp') -> 'Exp':
        raise NotImplementedError


class ExpNat(Exp, Token):
    def __init__(self, a: Nat):
        assert isinstance(a, Nat), type(a)
        self.a = a

    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpNat):
            return self.a == other.a
        else:
            return False

    @property
    def value(self) -> Nat:
        return self.a

    def one_step(self, other: 'Exp') -> 'Exp':
        raise DeductionError


class ExpPlus(Exp, BinaryOp):
    operator = '+'
    associate = 0
    precedence = 1

    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpPlus):
            return self.a == other.a and self.b == other.b
        else:
            return False

    def __init__(self, a: Exp, b: Exp):
        assert isinstance(a, Exp), type(a)
        assert isinstance(b, Exp), type(b)
        self.a = a
        self.b = b

    @property
    def value(self) -> Nat:
        return self.a.value + self.b.value

    def one_step(self, other: 'Exp') -> 'Exp':
        if isinstance(other, ExpNat):
            return self.a.value + self.b.value
        elif isinstance(other, ExpPlus):
            try:
                a = self.a.one_step(other.a)
            except DeductionError:
                a = self.a

            try:
                b = self.b.one_step(other.b)
            except DeductionError:
                b = self.b

            return ExpPlus(a, b)
        else:
            raise DeductionError


class ExpTimes(Exp, BinaryOp):
    operator = '*'
    associate = 0
    precedence = 2

    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpTimes):
            return self.a == other.a and self.b == other.b
        else:
            return False

    def __init__(self, a: Exp, b: Exp):
        assert isinstance(a, Exp), type(a)
        assert isinstance(b, Exp), type(b)
        self.a = a
        self.b = b

    @property
    def value(self) -> Nat:
        return self.a.value * self.b.value

    def one_step(self, other: 'Exp') -> 'Exp':
        if isinstance(other, ExpNat):
            return self.a.value * self.b.value
        elif isinstance(other, ExpTimes):
            try:
                a = self.a.one_step(other.a)
            except DeductionError:
                a = self.a

            try:
                b = self.b.one_step(other.b)
            except DeductionError:
                b = self.b

            return ExpTimes(a, b)
        else:
            raise DeductionError


if __name__ == '__main__':
    pass
