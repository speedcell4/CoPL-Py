import os
import unittest
from typing import Iterable

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

ANSWER = os.path.join(PROJECT_DIR, r'answer', r'A{:03}.txt')
PROBLEM = os.path.join(PROJECT_DIR, r'problem', r'P{:03}.txt')


def type_checking(fn):
    type_error_info = r'{} should be {} instead of {}.'
    range_error_info = r'{} is out of range {}.'

    def wrapper(*args, **kwargs):
        for vari, varname in enumerate(fn.__code__.co_varnames):
            argtype = fn.__annotations__.get(varname)
            if isinstance(argtype, type):
                if 0 <= vari < len(args):
                    assert isinstance(args[vari], argtype), \
                        type_error_info.format(varname, argtype.__name__, type(args[vari]).__name__)
                elif varname in kwargs:
                    assert isinstance(kwargs[varname], argtype), \
                        type_error_info.format(varname, argtype.__name__, type(kwargs[varname]).__name__)
                else:
                    raise TypeError('what is {}?'.format(varname))
        rval = fn(*args, **kwargs)
        rtype = fn.__annotations__.get('return')
        if isinstance(rtype, type):
            assert isinstance(rval, rtype), type_error_info.format('return value', rtype.__name__, type(rval).__name__)
        return rval

    return wrapper


@type_checking
def generate_unittest(name: str, solver, indices: Iterable[int]) -> type(unittest.TestCase):
    def test_method(index):
        def wrapper(self):
            self.maxDiff = None
            self.assertEqual(load_answer(index), solver(load_problem(index)))

        return wrapper

    return type('Test{}'.format(name.capitalize()), (unittest.TestCase,), {
        'test_p{:03}'.format(index): test_method(index) for index in indices
        })


@type_checking
def load_problem(index: int) -> str:
    with open(PROBLEM.format(index), 'r') as reader:
        return ''.join(reader.readlines())


@type_checking
def load_answer(index: int) -> str:
    with open(ANSWER.format(index), 'r') as reader:
        return ''.join(reader.readlines())


@type_checking
def dump_answer(answer: str, index: int) -> None:
    with open(ANSWER.format(index), 'w') as writer:
        writer.write(answer)


if __name__ == '__main__':
    pass
