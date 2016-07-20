import unittest
from typing import Iterable

DEBUG = False

ANSWER = r'/Users/admin/PycharmProjects/CoPL/answer/A{:03}.txt'
PROBLEM = r'/Users/admin/PycharmProjects/CoPL/problem/P{:03}.txt'


def load_answer(index: int) -> str:
    with open(ANSWER.format(index), 'r') as reader:
        return ''.join(reader.readlines()).strip()


def dump_answer(answer: str, index: int) -> None:
    with open(ANSWER.format(index), 'w') as writer:
        writer.write(answer.strip())


def load_problem(index: int) -> str:
    with open(PROBLEM.format(index), 'r') as reader:
        return ''.join(reader.readlines()).strip()


def generate_unittest(name: str, solver, indices: Iterable[int]) -> unittest.TestCase:
    def test_method(index):
        def wrapper(self):
            self.assertEqual(load_answer(index), solver(load_problem(index)))

        return wrapper

    return type('Test{}'.format(name.capitalize()), (unittest.TestCase,), {
        'test_p{:03}'.format(index): test_method(index) for index in indices
        })
