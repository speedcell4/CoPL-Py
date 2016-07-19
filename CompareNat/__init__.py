from CompareNat.parser import assertion
from CompareNat.rule import compareNat1, compareNat2, compareNat3
from base.derivation import Solver

from base.util import generate_unittest

CompareNat1 = Solver(assertion, compareNat1)
CompareNat2 = Solver(assertion, compareNat2)
CompareNat3 = Solver(assertion, compareNat3)

if __name__ == '__main__':
    import unittest

    a = generate_unittest(CompareNat1, [9, 12])
    b = generate_unittest(CompareNat2, [10, 13])
    c = generate_unittest(CompareNat3, [11, 14])
    unittest.main()
