import logging

from CompareNat import CompareNat1
from CompareNat import CompareNat2
from CompareNat import CompareNat3
from EvalNatExp import EvalNatExp
from Nat import Nat
from ReduceNatExp import ReduceNatExp
from bases.util import load_problem

logging.basicConfig(
    format=r'[%(levelname)s]%(asctime)s: %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S',
    level=logging.DEBUG,
)

systems = {
    'Nat'.lower(): Nat,
    'CompareNat1'.lower(): CompareNat1,
    'CompareNat2'.lower(): CompareNat2,
    'CompareNat3'.lower(): CompareNat3,
    'EvalNatExp'.lower(): EvalNatExp,
    'ReduceNatExp'.lower(): ReduceNatExp,
}

if __name__ == '__main__':
    print(load_problem(21))
