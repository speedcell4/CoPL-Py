from CompareNat.rule import IsLessThan
from Nat.miao import nat
from bases.parser import string, spaces, pure

assertion = pure(lambda a: lambda b: IsLessThan(a, b)) + nat + (spaces >> string(r'is less than') >> spaces >> nat)
