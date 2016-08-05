from bases.util import type_checking


class Regex(object):
    def __str__(self) -> str:
        raise NotImplementedError


class RegexEmpty(Regex):
    @type_checking
    def __str__(self) -> str:
        return r''


class RegexLiteral(Regex):
    @type_checking
    def __init__(self, char: str):
        assert len(char) == 1
        self.char = char

    @type_checking
    def __str__(self) -> str:
        return r'{}'.format(self.char)


class RegexConcatenation(Regex):
    @type_checking
    def __init__(self, r1: Regex, r2: Regex):
        self.r1 = r1
        self.r2 = r2

    @type_checking
    def __str__(self) -> str:
        return r'{}{}'.format(self.r1, self.r2)


class RegexAlternation(Regex):
    @type_checking
    def __init__(self, r1: Regex, r2: Regex):
        self.r1 = r1
        self.r2 = r2

    @type_checking
    def __str__(self) -> str:
        return r'{}|{}'.format(self.r1, self.r2)


class RegexKleene(Regex):
    @type_checking
    def __init__(self, r: Regex):
        self.r = r

    @type_checking
    def __str__(self) -> str:
        return r'({})*'.format(self.r)
