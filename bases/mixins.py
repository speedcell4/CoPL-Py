class BaseToken(object):
    def paraphrase(self, parent: 'BaseToken', index: int) -> str:
        raise NotImplementedError


class Token(BaseToken):
    def __str__(self) -> str:
        raise NotImplementedError

    def paraphrase(self, parent: 'BaseToken', index: int) -> str:
        return r'{}'.format(self)


class Operator(BaseToken):
    operator = None
    precedence = -1

    def paraphrase(self, parent: 'BaseToken', index: int) -> str:
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class UnaryOp(Operator):
    a = None

    def paraphrase(self, parent: 'BaseToken', index: int) -> str:
        return r'{}'.format(self.__str__())

    def __str__(self):
        assert isinstance(self.a, BaseToken)
        return r'{} {}'.format(self.operator, self.a.paraphrase(self, 0))


class BinaryOp(Operator):
    a = None
    b = None

    associate = -1

    def paraphrase(self, parent: 'BaseToken', index: int) -> str:
        if isinstance(parent, Token):
            raise TypeError('parent {} could not be {}'.format(parent, Token.__name__))
        elif isinstance(parent, UnaryOp):
            raise NotImplementedError
        elif isinstance(parent, BinaryOp):
            if parent.precedence == self.precedence:
                if parent.associate == self.associate == index:
                    return r'{}'.format(self.__str__())
                else:
                    return r'({})'.format(self.__str__())
            elif parent.precedence < self.precedence:
                return r'{}'.format(self.__str__())
            else:
                return r'({})'.format(self.__str__())
        elif isinstance(parent, TrinaryOp):
            raise NotImplementedError

    def __str__(self):
        assert isinstance(self.a, BaseToken)
        assert isinstance(self.b, BaseToken)
        return '{} {} {}'.format(self.a.paraphrase(self, 0), self.operator, self.b.paraphrase(self, 1))


class TrinaryOp(Operator):
    a = None
    b = None
    c = None

    def paraphrase(self, parent: 'BaseToken', index: int) -> str:
        pass

    def __str__(self):
        return r'{} {} {} {} {} {}'.format(self.operator[0], self.a, self.operator[1], self.b, self.operator[2], self.c)
