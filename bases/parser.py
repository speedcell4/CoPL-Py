import functools
import itertools
import logging
from typing import Tuple, Any, Callable, Union

from bases.mixins import BinaryOp
from bases.util import type_checking


# TODO
class ParsingError(Exception):
    pass


class Parser(object):
    def __init__(self, fn=None):
        self.fn = fn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @type_checking
    def define(self, parser: 'Parser'):
        self.fn = parser.fn

    @type_checking
    def run(self, raw: str):
        logging.debug(r'raw: {}'.format(raw))
        return self(raw)[1]

    def __call__(self, raw: str) -> Tuple[str, Any]:
        return self.fn(raw)

    @type_checking
    def __add__(self, other: 'Parser') -> 'Parser':
        def wrapper(raw: str) -> Tuple[str, Any]:
            try:
                raw1, ans1 = self(raw)
                raw2, ans2 = other(raw1)
                return raw2, ans1(ans2)
            except TypeError:
                return None

        return Parser(wrapper)

    @type_checking
    def __or__(self, other: 'Parser') -> 'Parser':
        def wrapper(raw: str) -> Tuple[str, Any]:
            try:
                raw1, ans1 = self(raw)
                return raw1, ans1
            except (TypeError, ValueError) as error:
                logging.debug(r'or {}'.format(error))
                return other(raw)

        return Parser(wrapper)

    @type_checking
    def __lshift__(self, other: 'Parser') -> 'Parser':
        def wrapper(raw: str) -> Tuple[str, Any]:
            try:
                raw1, ans1 = self(raw)
                raw2, ans2 = other(raw1)
                return raw2, ans1
            except TypeError:
                return None

        return Parser(wrapper)

    @type_checking
    def __rshift__(self, other: 'Parser') -> 'Parser':
        def wrapper(raw: str) -> Tuple[str, Any]:
            try:
                raw1, ans1 = self(raw)
                raw2, ans2 = other(raw1)
                return raw2, ans2
            except TypeError:
                return None

        return Parser(wrapper)


def pure(_: Any) -> Parser:
    @Parser
    def wrapper(raw: str):
        return raw, _

    return wrapper


def satisfy(condition: Callable[[str], bool]) -> Parser:
    @Parser
    def wrapper(raw: str):
        if raw and condition(raw[0]):
            return raw[1:], raw[0]

    return wrapper


space = satisfy(str.isspace)
digit = satisfy(str.isdigit)
alpha = satisfy(str.isalpha)


def many(item: Parser) -> Parser:
    with Parser() as parser:
        collection = pure(lambda a: lambda b: a + b) + item + parser
        empty = pure('')  # TODO [] or ''
        parser.define(collection | empty)
        return parser


spaces = many(space)
digits = many(digit)
alphas = many(alpha)


@type_checking
def regex(pattern: str) -> Parser:
    import re
    pattern = re.compile(pattern if pattern.startswith(r'^') else r'^' + pattern)

    @Parser
    def wrapper(raw: str):
        match = pattern.match(raw)
        if match:
            return raw[match.span()[1]:], match.group()

    return wrapper


@type_checking
def string(const: str) -> Parser:
    assert isinstance(const, str)

    @Parser
    def wrapper(raw: str):
        if raw.startswith(const):
            return raw[len(const):], raw[:len(const)]

    return wrapper


stringl = lambda const: spaces >> string(const)
stringr = lambda const: string(const) << spaces
string2 = lambda const: spaces >> string(const) << spaces

EOF = '<EOF>'
eof = string(EOF)


@type_checking
def chainl(token: Parser, op: type(BinaryOp), expr: Parser) -> Parser:
    o = string2(op.operator)
    opt = pure(lambda a: lambda b: op(a, b))
    with expr or Parser() as exp:
        sub = opt + token + (o >> token)
        exp.define(opt + sub + (o >> exp) | sub | token)
        return exp


@type_checking
def chainr(token: Parser, op: type(BinaryOp), expr: Parser) -> Parser:
    o = string2(op.operator)
    opt = pure(lambda a: lambda b: op(a, b))
    with expr or Parser() as exp:
        sub = opt + (token << o) + exp
        exp.define(opt + (token << o) + sub | sub | token)
        return exp


@type_checking
def chain(token: Parser, op: type(BinaryOp), expr: Parser = None) -> Parser:
    return [chainl, chainr][op.associate](token, op, expr)


@type_checking
def infixes(token: Parser, *ops: type(BinaryOp)) -> Parser:
    key = lambda n: (n.precedence, n.associate)

    with Parser() as exp:
        terms = [bracket(r'(', exp, r')') | token]
        for (precedence, associate), operators in itertools.groupby(sorted(ops, reverse=True, key=key), key=key):
            operators = list(operators)
            logging.debug(r'{}'.format(operators))
            with Parser() as temp:
                temp.define(functools.reduce(lambda a, b: a | b, [chain(terms[-1], op, temp) for op in operators]))
                terms.append(temp)
        exp.define(terms[-1])
        return exp


def bracket(l: Union[str, Parser], parser: Parser, r: Union[str, Parser]) -> Parser:
    l = l if isinstance(l, Parser) else string(l)
    r = r if isinstance(r, Parser) else string(r)
    return l >> spaces >> parser << spaces << r


logging.basicConfig(
    format=r'[%(levelname)s]%(asctime)s: %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S',
    level=logging.DEBUG,
)

if __name__ == '__main__':
    from EvalML1.data import ExpPlus, ExpMinus, ExpTimes

    exp = infixes(Parser(), ExpTimes, ExpPlus, ExpMinus)
