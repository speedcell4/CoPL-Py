from CompareNat.parser import assertion
from CompareNat.rule import compareNat1, compareNat2, compareNat3
from base.derivation import Solver

CompareNat1 = Solver(assertion, compareNat1)
CompareNat2 = Solver(assertion, compareNat2)
CompareNat3 = Solver(assertion, compareNat3)
