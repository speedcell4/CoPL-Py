from EvalML4.parser import assertion
from EvalML4.rule import eval_ml_4
from bases.derivation import Solver
from bases.util import load_problem, dump_answer

EvalML4 = Solver(assertion, eval_ml_4)

if __name__ == '__main__':
    dump_answer(EvalML4(load_problem(71)), 71)
