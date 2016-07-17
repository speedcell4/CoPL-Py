from Base.Parser import string, pure, Parser, space, spaces, eof
from Nat.Types import Z, S
from Nat.Rules import PlusIs, TimesIs

with Parser() as nat:
    z = string('Z') >> pure(Z())
    s = string('S(') >> pure(S) + nat << string(')')
    nat.define(s | z)

with Parser() as assertion:
    plus_is = pure(lambda a: lambda b: lambda c: PlusIs(a, b, c)) \
              + nat \
              + (spaces >> string('plus') >> spaces >> nat) \
              + (spaces >> string('is') >> spaces >> nat)
    times_is = pure(lambda a: lambda b: lambda c: TimesIs(a, b, c)) \
               + nat \
               + (spaces >> string('times') >> spaces >> nat) \
               + (spaces >> string('is') >> spaces >> nat)
    assertion.define(plus_is | times_is)

# assertion = assertion + eof
