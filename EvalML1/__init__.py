from EvalML1.parser import assertion
from EvalML1.rule import eval_ml_1
from bases.derivation import Solver
from bases.util import load_problem, dump_answer

EvalML1 = Solver(assertion, eval_ml_1)

if __name__ == '__main__':
    dump_answer(EvalML1(load_problem(30)), 30)
