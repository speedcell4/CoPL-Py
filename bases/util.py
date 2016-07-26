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


def type_checking(fn):
    type_error_info = r'{} should be {} instead of {}.'

    def wrapper(*args, **kwargs):
        for vari, varname in enumerate(fn.__code__.co_varnames):
            argtype = fn.__annotations__.get(varname)
            if isinstance(argtype, type):
                if vari < len(args):
                    assert isinstance(args[vari], argtype), \
                        type_error_info.format(varname, argtype.__name__, type(args[vari]).__name__)
                elif varname in vari:
                    assert isinstance(args[varname], argtype), \
                        type_error_info.format(varname, argtype.__name__, type(args[vari]).__name__)
                else:
                    raise TypeError('what is this?')
        rval = fn(*args, **kwargs)
        rtype = fn.__annotations__.get('return')
        if isinstance(rtype, type):
            assert isinstance(rval, rtype), type_error_info.format('return value', rtype.__name__, type(rval).__name__)
        return rval

    return wrapper
