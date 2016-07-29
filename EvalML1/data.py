from bases.mixins import BinaryOp, TrinaryOp, Token
from bases.util import type_checking


class EvaluationError(Exception):
    pass


class Value(object):
    @type_checking
    def __str__(self) -> str:
        raise NotImplementedError

    @type_checking
    def __eq__(self, other: 'Value') -> bool:
        raise NotImplementedError


class ValueInt(Value, Token):
    @type_checking
    def __init__(self, i: int):
        self.i = i

    @type_checking
    def __str__(self) -> str:
        return r'{}'.format(self.i)

    @type_checking
    def __eq__(self, other: 'Value') -> bool:
        if isinstance(other, ValueInt):
            return self.i == other.i
        else:
            return False

    @type_checking
    def __add__(self, other: 'ValueInt') -> 'ValueInt':
        return ValueInt(self.i + other.i)

    @type_checking
    def __sub__(self, other: 'ValueInt') -> 'ValueInt':
        return ValueInt(self.i - other.i)

    @type_checking
    def __mul__(self, other: 'ValueInt') -> 'ValueInt':
        return ValueInt(self.i * other.i)

    @type_checking
    def __lt__(self, other: 'ValueInt') -> 'ValueBool':
        return ValueBool(self.i < other.i)


class ValueBool(Value, Token):
    @type_checking
    def __init__(self, b: bool):
        self.b = b

    @type_checking
    def __str__(self) -> str:
        if self.b:
            return 'true'
        else:
            return 'false'

    @type_checking
    def __eq__(self, other: 'Value') -> bool:
        if isinstance(other, ValueBool):
            return self.b == other.b
        else:
            return False


class Exp(object):
    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        raise NotImplementedError

    @property
    @type_checking
    def value(self) -> Value:
        raise NotImplementedError


class ExpInt(Exp, Token):
    @type_checking
    def __str__(self) -> str:
        return r'{}'.format(self.i)

    @type_checking
    def __init__(self, i: int):
        self.i = i

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpInt):
            return self.i == other.i
        else:
            return False

    @property
    @type_checking
    def value(self) -> ValueInt:
        return ValueInt(self.i)


class ExpBool(Exp, Token):
    @type_checking
    def __str__(self) -> str:
        if self.b:
            return 'true'
        else:
            return 'false'

    @type_checking
    def __init__(self, b: bool):
        self.b = b

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpBool):
            return self.b == other.b
        else:
            return False

    @property
    @type_checking
    def value(self) -> ValueBool:
        return ValueBool(self.b)


class ExpPlus(Exp, BinaryOp):
    operator = r'+'

    associate = 0
    precedence = 2

    def __str__(self):
        return r'({} + {})'.format(self.a, self.b)

    @type_checking
    def __init__(self, a: Exp, b: Exp):
        self.a = a
        self.b = b

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpPlus):
            return self.a == other.a and self.b == other.b
        else:
            return False

    @property
    def value(self) -> ValueInt:
        a_value = self.a.value
        b_value = self.b.value
        assert isinstance(a_value, ValueInt)
        assert isinstance(b_value, ValueInt)
        return a_value + b_value


class ExpMinus(Exp, BinaryOp):
    operator = r'-'

    associate = 0
    precedence = 2

    @type_checking
    def __init__(self, a: Exp, b: Exp):
        self.a = a
        self.b = b

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpMinus):
            return self.a == other.a and self.b == other.b
        else:
            return False

    @property
    @type_checking
    def value(self) -> ValueInt:
        a_value = self.a.value
        b_value = self.b.value
        assert isinstance(a_value, ValueInt)
        assert isinstance(b_value, ValueInt)
        return a_value - b_value


class ExpTimes(Exp, BinaryOp):
    operator = r'*'

    associate = 0
    precedence = 3

    @type_checking
    def __init__(self, a: Exp, b: Exp):
        self.a = a
        self.b = b

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpTimes):
            return self.a == other.a and self.b == other.b
        else:
            return False

    @property
    def value(self) -> ValueInt:
        a_value = self.a.value
        b_value = self.b.value
        assert isinstance(a_value, ValueInt)
        assert isinstance(b_value, ValueInt)
        return a_value * b_value


class ExpLt(Exp, BinaryOp):
    operator = r'<'

    associate = 0
    precedence = 1

    @type_checking
    def __init__(self, a: Exp, b: Exp):
        self.a = a
        self.b = b

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpLt):
            return self.a == other.a and self.b == other.b
        else:
            return False

    @property
    def value(self) -> ValueBool:
        a_value = self.a.value
        b_value = self.b.value
        assert isinstance(a_value, ValueInt)
        assert isinstance(b_value, ValueInt)
        return a_value < b_value


class ExpIf(Exp, TrinaryOp):
    operator = ['if', 'then', 'else']

    @type_checking
    def __init__(self, a: Exp, b: Exp, c: Exp):
        self.a = a
        self.b = b
        self.c = c

    @type_checking
    def __eq__(self, other: 'Exp') -> bool:
        if isinstance(other, ExpIf):
            return self.a == other.a and self.b == other.b and self.c == other.c
        else:
            return False

    @property
    def value(self) -> Value:
        a_value = self.a.value
        if isinstance(a_value, ValueBool):
            if a_value.b:
                return self.b.value
            else:
                return self.c.value
        else:
            raise EvaluationError('condition {} is not ValueBool type'.format(self.a))
