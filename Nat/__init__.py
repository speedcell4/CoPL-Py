from base.util import generate_unittest

from base.derivation import Solver
from Nat.parser import assertion
from Nat.rule import nat_system

Nat = Solver(assertion, nat_system)

if __name__ == '__main__':
    import unittest

    miao = generate_unittest(Nat, range(1, 9))
    unittest.main()
