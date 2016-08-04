from ReduceNatExp.parser import assertion
from ReduceNatExp.rule import reduce_nat_exp
from bases.deduction import Solver

ReduceNatExp = Solver(assertion, reduce_nat_exp)

if __name__ == '__main__':
    pass
