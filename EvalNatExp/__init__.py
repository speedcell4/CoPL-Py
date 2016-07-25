from EvalNatExp.parser import exp, assertion
from EvalNatExp.rule import eval_nat_exp
from bases.derivation import Solver
from bases.util import generate_unittest

EvalNatExp = Solver(assertion, eval_nat_exp)

if __name__ == '__main__':
    import unittest

    _ = generate_unittest('EvalNatExp', EvalNatExp, range(15, 21))
    unittest.main()
