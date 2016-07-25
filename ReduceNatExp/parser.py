from ReduceNatExp.rule import Reduce1, Reduce0, ReduceD
from EvalNatExp.parser import exp, nat
from bases.parser import Parser, pure, sstrings

with Parser() as assertion:
    reduce = pure(lambda a: lambda b: Reduce1(a, b)) + exp + (sstrings(r'--->') >> exp)
    reduce0 = pure(lambda a: lambda b: Reduce0(a, b)) + exp + (sstrings(r'-*->') >> exp)
    reduced = pure(lambda a: lambda b: ReduceD(a, b)) + exp + (sstrings(r'-d->') >> exp)
    assertion.define(reduce | reduce0 | reduced)

if __name__ == '__main__':
    print(assertion.run(r'Z + S(S(Z)) -*-> S(S(Z))'))
