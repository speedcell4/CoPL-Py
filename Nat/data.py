class Nat(object):
    def __eq__(self, other: 'Nat') -> bool:
        raise NotImplementedError

    def __add__(self, other: 'Nat') -> 'Nat':
        raise NotImplementedError

    def __mul__(self, other: 'Nat') -> 'Nat':
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def __lt__(self, other: 'Nat') -> bool:
        raise NotImplementedError


class Z(Nat):
    def __eq__(self, other: 'Nat') -> bool:
        assert isinstance(other, Nat)
        return isinstance(other, Z)

    def __add__(self, other: 'Nat') -> 'Nat':
        assert isinstance(other, Nat)
        return other

    def __mul__(self, other: 'Nat') -> 'Nat':
        assert isinstance(other, Nat)
        return Z()

    def __str__(self):
        return 'Z'

    def __lt__(self, other: 'Nat') -> bool:
        return isinstance(other, S)


class S(Nat):
    def __init__(self, prev: 'Nat'):
        assert isinstance(prev, Nat)
        self.prev = prev

    def __eq__(self, other: 'Nat') -> bool:
        assert isinstance(other, Nat)
        if isinstance(other, S):
            return self.prev == other.prev
        else:
            return False

    def __add__(self, other: 'Nat') -> 'Nat':
        assert isinstance(other, Nat)
        return self.prev + S(other)

    def __mul__(self, other: 'Nat') -> 'Nat':
        assert isinstance(other, Nat)
        return self.prev * other + other

    def __str__(self):
        return 'S({})'.format(self.prev)

    def __lt__(self, other: 'Nat') -> bool:
        if isinstance(other, S):
            return self.prev < other.prev
        else:
            return False
