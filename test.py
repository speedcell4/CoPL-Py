import unittest

from CompareNat import CompareNat1, CompareNat2, CompareNat3
from EvalML1 import EvalML1
from EvalML1Err import EvalML1Err
from EvalNatExp import EvalNatExp
from Nat import Nat
from ReduceNatExp import ReduceNatExp
from bases.util import generate_unittest

nat = generate_unittest(r'Nat', Nat, range(1, 9))
compare_nat_1 = generate_unittest(r'CompareNat1', CompareNat1, [9, 12])
compare_nat_2 = generate_unittest(r'CompareNat2', CompareNat2, [10, 13])
compare_nat_3 = generate_unittest(r'CompareNat3', CompareNat3, [11, 14])
eval_nat_exp = generate_unittest(r'EvalNatExp', EvalNatExp, range(15, 21))
reduce_nat_exp = generate_unittest(r'ReduceNatExp', ReduceNatExp, range(21, 25))
eval_ml_1 = generate_unittest(r'EvalML1', EvalML1, range(25, 31))
eval_ml_1_err = generate_unittest(r'EvalML1Err', EvalML1Err, range(31, 34))

if __name__ == '__main__':
    unittest.main()
