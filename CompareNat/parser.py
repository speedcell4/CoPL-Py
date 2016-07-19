from CompareNat.rule import IsLessThan
from Nat.parser import nat
from base.parser import string, spaces, pure

assertion = pure(lambda a: lambda b: IsLessThan(a, b)) + nat + (spaces >> string(r'is less than') >> spaces >> nat)
