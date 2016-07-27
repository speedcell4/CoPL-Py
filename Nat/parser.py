from Nat.data import Z, S
from Nat.rule import PlusIs, TimesIs
from bases.parser import string, string2, pure, Parser

with Parser() as nat:
    z = string('Z') >> pure(Z())
    s = string('S(') >> (pure(S) + nat) << string(')')
    nat.define(s | z)

with Parser() as assertion:
    plus_is = pure(lambda a: lambda b: lambda c: PlusIs(a, b, c)) \
              + nat + (string2('plus') >> nat) + (string2('is') >> nat)
    times_is = pure(lambda a: lambda b: lambda c: TimesIs(a, b, c)) \
               + nat + (string2('times') >> nat) + (string2('is') >> nat)
    assertion.define(plus_is | times_is)
