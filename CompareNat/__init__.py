from CompareNat.parser import assertion
from CompareNat.rule import compare_nat1, compare_nat2, compare_nat3
from bases.deduction import Solver

CompareNat1 = Solver(assertion, compare_nat1)
CompareNat2 = Solver(assertion, compare_nat2)
CompareNat3 = Solver(assertion, compare_nat3)

if __name__ == '__main__':
    pass
