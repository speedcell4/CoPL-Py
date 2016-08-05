from EvalML1Err.parser import assertion
from EvalML1Err.rule import eval_ml_1_err
from bases.derivation import Solver
from bases.util import load_problem, dump_answer

EvalML1Err = Solver(assertion, eval_ml_1_err)

if __name__ == '__main__':
    dump_answer(EvalML1Err(load_problem(33)), 33)
