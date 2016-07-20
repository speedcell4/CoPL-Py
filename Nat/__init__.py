from base.derivation import Solver

from Nat.parser import assertion
from Nat.rule import nat
from bases.util import generate_unittest

Nat = Solver(assertion, nat)

if __name__ == '__main__':
    import unittest

    _ = generate_unittest('Nat', Nat, range(1, 9))
    unittest.main()
