from bases.util import type_checking


class RenderError(Exception):
    pass


class BaseToken(object):
    @type_checking
    def sub(self, index: int) -> str:
        raise NotImplementedError

    @type_checking
    def __str__(self) -> str:
        raise NotImplementedError


class Token(BaseToken):
    @type_checking
    def sub(self, index: int) -> str:
        raise RenderError


class Function(Token):
    @type_checking
    def sub(self, index: int) -> str:
        raise RenderError


class Operator(BaseToken):
    operator = None  # type: str
    precedence = -1  # type: int

    @type_checking
    def sub(self, index: int) -> str:
        raise RenderError


class UnaryOp(Operator):
    a = None  # type: BaseToken

    @type_checking
    def sub(self, index: int) -> str:
        if index not in [0]:
            raise RenderError
        return r'{}'.format(self.a)

    @type_checking
    def __str__(self) -> str:
        return r'{}'.format(self.a)


class BinaryOp(Operator):
    a = None  # type: BaseToken
    b = None  # type: BaseToken

    associate = -1  # type: int

    @type_checking
    def __str__(self) -> str:
        return r'{} {} {}'.format(self.sub(0), self.operator, self.sub(1))

    @type_checking
    def sub(self, index: int) -> str:
        child = [self.a, self.b][index]

        if isinstance(child, Operator):
            if child.precedence < self.precedence:
                return r'({})'.format(child)
            if isinstance(child, BinaryOp) and child.precedence == self.precedence:
                if self.associate != index:
                    return r'({})'.format(child)
        elif isinstance(child, Function):
            return r'({})'.format(child)
        return r'{}'.format(child)


class TrinaryOp(Operator):
    a = None  # type: BaseToken
    b = None  # type: BaseToken
    c = None  # type: BaseToken

    @type_checking
    def __str__(self) -> str:
        return r'{} {} {} {} {} {}'.format(
            self.operator[0], self.sub(0),
            self.operator[1], self.sub(1),
            self.operator[2], self.sub(2))

    @type_checking
    def sub(self, index: int) -> str:
        return r'{}'.format([self.a, self.b, self.c][index])
