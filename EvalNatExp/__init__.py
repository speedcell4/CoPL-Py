from EvalNatExp.parser import exp, assertion
from EvalNatExp.rule import eval_nat_exp
from bases.derivation import Solver

EvalNatExp = Solver(assertion, eval_nat_exp)

if __name__ == '__main__':
    pass
