from Nat.data import Z, S
from Nat.rule import PlusIs, TimesIs
from bases.parser import string, pure, Parser, spaces

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
