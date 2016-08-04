from Nat.parser import assertion
from Nat.rule import nat
from bases.derivation import Solver
from bases.util import load_problem, dump_answer

Nat = Solver(assertion, nat)

if __name__ == '__main__':
    dump_answer(Nat(load_problem(7)), 7)
