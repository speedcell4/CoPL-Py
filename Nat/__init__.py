from Nat.Parser import assertion
from Nat.Rules import nat_system
from Base.Derivation import Solver

Nat = Solver(assertion, nat_system)
