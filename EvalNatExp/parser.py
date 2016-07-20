from EvalNatExp.data import ExpNat, ExpPlus, ExpTimes
from Nat.parser import nat
from bases.parser import Parser, spaces, pure, string, eof, EOF

with Parser() as exp:
    exp_nat = Parser()
    exp_plus = Parser()
    exp_times = Parser()

    exp_nat.define(
        (string(r'(') >> spaces >> exp << spaces << string(r')'))
        | (pure(ExpNat) + nat))
    exp_times.define(
        ((pure(lambda a: lambda b: ExpTimes(a, b))) +
         exp_nat +
         (spaces >> string(r'*') >> spaces >> exp_times))
        | exp_nat)
    exp_plus.define(
        ((pure(lambda a: lambda b: ExpPlus(a, b))) +
         exp_times +
         (spaces >> string(r'+') >> spaces >> exp_plus))
        | exp_times)

    exp.define(exp_plus)

if __name__ == '__main__':
    print((exp << eof).run(r'S(Z) + S(S(Z)) + Z' + EOF))
    print((exp << eof).run(r'S(Z) + S(S(Z)) * Z' + EOF))
    print((exp << eof).run(r'S(Z) * S(S(Z)) + Z' + EOF))
    print((exp << eof).run(r'S(Z) * S(S(Z)) * Z' + EOF))

    print((exp << eof).run(r'(S(Z) + S(S(Z))) + Z' + EOF))
    print((exp << eof).run(r'(S(Z) + S(S(Z))) * Z' + EOF))
    print((exp << eof).run(r'(S(Z) * S(S(Z))) + Z' + EOF))
    print((exp << eof).run(r'(S(Z) * S(S(Z))) * Z' + EOF))

    print((exp << eof).run(r'S(Z) + (S(S(Z)) + Z)' + EOF))
    print((exp << eof).run(r'S(Z) + (S(S(Z)) * Z)' + EOF))
    print((exp << eof).run(r'S(Z) * (S(S(Z)) + Z)' + EOF))
    print((exp << eof).run(r'S(Z) * (S(S(Z)) * Z)' + EOF))
