from EvalML2.parser import assertion
from EvalML2.rule import eval_ml_2
from bases.derivation import Solver
from bases.util import load_problem, dump_answer

EvalML2 = Solver(assertion, eval_ml_2)

if __name__ == '__main__':
    dump_answer(EvalML2(load_problem(37)), 37)
