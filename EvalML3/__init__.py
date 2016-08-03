from EvalML3.parser import assertion
from EvalML3.rule import EvalML3
from bases.derivation import Solver
from bases.util import load_problem, dump_answer

eval_ml_3 = Solver(assertion, EvalML3)

if __name__ == '__main__':
    dump_answer(eval_ml_3(load_problem(41)), 41)
