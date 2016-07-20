from base.derivation import Solver

from CompareNat.parser import assertion
from CompareNat.rule import compare_nat1, compare_nat2, compare_nat3
from bases.util import generate_unittest

CompareNat1 = Solver(assertion, compare_nat1)
CompareNat2 = Solver(assertion, compare_nat2)
CompareNat3 = Solver(assertion, compare_nat3)

if __name__ == '__main__':
    import unittest

    a = generate_unittest(r'CompareNat1', CompareNat1, [9, 12])
    b = generate_unittest(r'CompareNat2', CompareNat2, [10, 13])
    c = generate_unittest(r'CompareNat13', CompareNat3, [11, 14])
    unittest.main()
