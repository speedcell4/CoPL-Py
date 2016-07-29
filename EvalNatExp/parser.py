from EvalNatExp.data import ExpNat, ExpPlus, ExpTimes
from EvalNatExp.rule import EvalTo
from Nat.parser import nat
from bases.parser import Parser, pure, string2, bracket, infixes

with Parser() as exp:
    exp_term = bracket(r'(', exp, r')') | (pure(ExpNat) + nat)
    exp.define(infixes(exp_term, ExpPlus, ExpTimes))

with Parser() as assertion:
    assertion.define(pure(lambda e: lambda n: EvalTo(e, n)) + exp + (string2(r'evalto') >> nat))

if __name__ == '__main__':
    print(exp.run(r'(S(S(S(Z))) + (S(S(Z)) + S(Z))) * Z'))
