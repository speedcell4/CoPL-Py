from EvalNatExp.data import ExpNat, ExpPlus, ExpTimes
from EvalNatExp.rule import EvalTo
from Nat.parser import nat
from bases.parser import Parser, pure, sstrings, bracket, infix

with Parser() as exp:
    exp1 = bracket(r'(', exp, r')') | (pure(ExpNat) + nat)
    exp2 = infix(exp1, ExpTimes)
    exp3 = infix(exp2, ExpPlus)
    exp.define(exp3)

with Parser() as assertion:
    assertion.define(pure(lambda e: lambda n: EvalTo(e, n)) + exp + (sstrings(r'evalto') >> nat))

if __name__ == '__main__':
    print(exp.run(r'S(S(S(Z))) + S(S(Z)) * S(Z)'))
