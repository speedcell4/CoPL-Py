import logging

from Nat.data import Nat
from bases.derivation import DeductionError
from bases.mixins import Token, BinaryOp
from bases.util import type_checking


class Exp(object):
    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        raise NotImplementedError

    @property
    @type_checking
    def value(self) -> Nat:
        raise NotImplementedError

    @type_checking
    def one_step(self, other: 'Exp') -> 'Exp':
        raise NotImplementedError


class ExpNat(Exp, Token):
    @type_checking
    def __init__(self, a: Nat):
        self.a = a

    @type_checking
    def __eq__(self, other: Exp) -> bool:
        if isinstance(other, ExpNat):
            return self.a == other.a
        else:
            return False

    @property
    @type_checking
    def value(self) -> Nat:
        return self.a

    @type_checking
    def one_step(self, other: 'Exp') -> 'Exp':
        raise DeductionError


class ExpPlus(Exp, BinaryOp):
    operator = '+'
    associate = 0
    precedence = 1

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpPlus):
            return self.a == other.a and self.b == other.b
        else:
            return False

    @type_checking
    def __init__(self, a: Exp, b: Exp):
        self.a = a
        self.b = b

    @property
    @type_checking
    def value(self) -> Nat:
        return self.a.value + self.b.value

    @type_checking
    def one_step(self, other: 'Exp') -> 'Exp':
        logging.debug('one step: {} => {}'.format(self, other))
        if self == other:
            raise DeductionError
        elif isinstance(other, ExpPlus):
            if self.a != other.a:
                logging.debug(r'ExpPlus, a: {} + {}'.format(self.a.one_step(other.a), self.b))
                return ExpPlus(self.a.one_step(other.a), self.b)
            if self.b != other.b:
                logging.debug(r'ExpPlus, b: {} + {}'.format(self.a, self.b.one_step(other.b)))
                return ExpPlus(self.a, self.b.one_step(other.b))
            raise DeductionError
        elif isinstance(other, ExpTimes):
            raise DeductionError
        elif isinstance(other, ExpNat):
            if not isinstance(self.a, ExpNat):
                logging.debug(r'ExpNat, a: {} + {}'.format(self.a.one_step(ExpNat(self.a.value)), self.b))
                return ExpPlus(self.a.one_step(ExpNat(self.a.value)), self.b)
            if not isinstance(self.b, ExpNat):
                logging.debug(r'ExpNat, b: {} + {}'.format(self.a, self.b.one_step(ExpNat(self.b.value))))
                return ExpPlus(self.a, self.b.one_step(ExpNat(self.b.value)))
            logging.debug(r'ExpNat: {}'.format(ExpNat(self.a.value + self.b.value)))
            return ExpNat(self.a.value + self.b.value)
        else:
            raise DeductionError


class ExpTimes(Exp, BinaryOp):
    operator = '*'
    associate = 0
    precedence = 2

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpTimes):
            return self.a == other.a and self.b == other.b
        else:
            return False

    @type_checking
    def __init__(self, a: Exp, b: Exp):
        assert isinstance(a, Exp), type(a)
        assert isinstance(b, Exp), type(b)
        self.a = a
        self.b = b

    @property
    @type_checking
    def value(self) -> Nat:
        return self.a.value * self.b.value

    @type_checking
    def one_step(self, other: 'Exp') -> 'Exp':
        logging.debug('one step: {} => {}'.format(self, other))
        if self == other:
            raise DeductionError
        elif isinstance(other, ExpTimes):
            if self.a != other.a:
                logging.debug(r'ExpTimes, a: {} * {}'.format(self.a.one_step(other.a), self.b))
                return ExpTimes(self.a.one_step(other.a), self.b)
            if self.b != other.b:
                logging.debug(r'ExpTimes, b: {} * {}'.format(self.a, self.b.one_step(other.b)))
                return ExpTimes(self.a, self.b.one_step(other.b))
            raise DeductionError
        elif isinstance(other, ExpPlus):
            raise DeductionError
        elif isinstance(other, ExpNat):
            if not isinstance(self.a, ExpNat):
                logging.debug(r'ExpNat, a: {} * {}'.format(self.a.one_step(ExpNat(self.a.value)), self.b))
                return ExpTimes(self.a.one_step(ExpNat(self.a.value)), self.b)
            if not isinstance(self.b, ExpNat):
                logging.debug(r'ExpNat, b: {} * {}'.format(self.a, self.b.one_step(ExpNat(self.b.value))))
                return ExpTimes(self.a, self.b.one_step(ExpNat(self.b.value)))
            logging.debug(r'ExpNat: {}'.format(ExpNat(self.a.value + self.b.value)))
            return ExpNat(self.a.value * self.b.value)
        else:
            raise DeductionError


if __name__ == '__main__':
    pass
