from TypingML4.parser import assertion
from TypingML4.rule import typing_ml_4
from bases.deduction import Solver
from bases.util import load_problem, dump_answer

TypingML4 = Solver(assertion, typing_ml_4)

if __name__ == '__main__':
    dump_answer(TypingML4(load_problem(97)), 97)
