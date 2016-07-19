from Nat import Nat
from CompareNat import CompareNat1
from CompareNat import CompareNat2
from CompareNat import CompareNat3
from base.util import load_problem, dump_answer

if __name__ == '__main__':
    dump_answer(CompareNat3(load_problem(14)), 14)
