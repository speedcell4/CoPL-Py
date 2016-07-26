from bases.derivation import Solver
from ReduceNatExp.parser import assertion
from ReduceNatExp.rule import reduce_nat_exp
from bases.util import load_problem, dump_answer

ReduceNatExp = Solver(assertion, reduce_nat_exp)

if __name__ == '__main__':
    pass
