from EvalNatExp.parser import exp
from ReduceNatExp.rule import Reduce1, Reduce0, ReduceD
from bases.parser import Parser, pure, string2

with Parser() as assertion:
    reduce1 = pure(lambda a: lambda b: Reduce1(a, b)) + exp + (string2(r'--->') >> exp)
    reduce0 = pure(lambda a: lambda b: Reduce0(a, b)) + exp + (string2(r'-*->') >> exp)
    reduced = pure(lambda a: lambda b: ReduceD(a, b)) + exp + (string2(r'-d->') >> exp)
    assertion.define(reduce1 | reduce0 | reduced)

if __name__ == '__main__':
    print(assertion.run(r'Z + S(S(Z)) -*-> S(S(Z))'))
