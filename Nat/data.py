from bases.util import type_checking


class Nat(object):
    @type_checking
    def __eq__(self, other: 'Nat') -> bool:
        raise NotImplementedError

    @type_checking
    def __add__(self, other: 'Nat') -> 'Nat':
        raise NotImplementedError

    @type_checking
    def __mul__(self, other: 'Nat') -> 'Nat':
        raise NotImplementedError

    @type_checking
    def __str__(self) -> str:
        raise NotImplementedError

    @type_checking
    def __lt__(self, other: 'Nat') -> bool:
        raise NotImplementedError


class Z(Nat):
    @type_checking
    def __eq__(self, other: 'Nat') -> bool:
        return isinstance(other, Z)

    @type_checking
    def __add__(self, other: 'Nat') -> 'Nat':
        return other

    @type_checking
    def __mul__(self, other: 'Nat') -> 'Nat':
        return Z()

    @type_checking
    def __str__(self):
        return 'Z'

    @type_checking
    def __lt__(self, other: 'Nat') -> bool:
        return isinstance(other, S)


class S(Nat):
    @type_checking
    def __init__(self, prev: 'Nat'):
        self.prev = prev

    @type_checking
    def __eq__(self, other: 'Nat') -> bool:
        if isinstance(other, S):
            return self.prev == other.prev
        else:
            return False

    @type_checking
    def __add__(self, other: 'Nat') -> 'Nat':
        return self.prev + S(other)

    @type_checking
    def __mul__(self, other: 'Nat') -> 'Nat':
        return self.prev * other + other

    @type_checking
    def __str__(self):
        return 'S({})'.format(self.prev)

    @type_checking
    def __lt__(self, other: 'Nat') -> bool:
        if isinstance(other, S):
            return self.prev < other.prev
        else:
            return False
