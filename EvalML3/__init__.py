from EvalML3.parser import assertion
from EvalML3.rule import eval_ml_3
from bases.derivation import Solver
from bases.util import load_problem, dump_answer

EvalML3 = Solver(assertion, eval_ml_3)

if __name__ == '__main__':
    dump_answer(EvalML3(load_problem(53)), 53)
