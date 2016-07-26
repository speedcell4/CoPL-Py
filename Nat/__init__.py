from Nat.parser import assertion
from Nat.rule import nat
from bases.derivation import Solver

Nat = Solver(assertion, nat)

if __name__ == '__main__':
    print(Nat(r'S(Z) times S(Z) is S(S(Z))'))
