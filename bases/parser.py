import logging
from functools import reduce
from typing import Tuple, Any, Callable, Union

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
            return self(raw) or other(raw)

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


sstrings = lambda const: spaces >> string(const) << spaces

EOF = '<EOF>'
eof = string(EOF)


@type_checking
def chainl(token: Parser, *ops) -> Parser:
    os = [sstrings(op.operator) for op in ops]
    opts = [pure(lambda a: lambda b: op(a, b)) for op in ops]
    with Parser() as expr:
        subs = [opt + token + (o >> token) for opt, o in zip(opts, os)]
        deeps = [opt + sub + (o >> expr) for opt, o, sub in zip(opts, os, subs)]
        expr.define(reduce(lambda a, b: a | b, deeps) | reduce(lambda a, b: a | b, subs) | token)
        return expr


@type_checking
def chainr(token: Parser, *ops) -> Parser:
    os = [sstrings(op.operator) for op in ops]
    opts = [pure(lambda a: lambda b: op(a, b)) for op in ops]
    with Parser() as expr:
        subs = [opt + (token << o) + expr for opt, o in zip(opts, os)]
        deeps = [opt + (token << o) + sub for opt, o, sub in zip(opts, os, subs)]
        expr.define(reduce(lambda a, b: a | b, deeps) | reduce(lambda a, b: a | b, subs) | token)
        return expr


# TODO how to write the type annotation of *args
@type_checking
def infix(token: Parser, *ops) -> Parser:
    assert all(op.associate == ops[0].associate and op.precedence == ops[0].precedence for op in
               ops), 'every op should have same precedence and associate'
    ps = [chainl, chainr]
    return ps[ops[0].associate](token, *ops)


def bracket(l: Union[str, Parser], parser: Parser, r: Union[str, Parser]) -> Parser:
    l = l if isinstance(l, Parser) else string(l)
    r = r if isinstance(r, Parser) else string(r)
    return l >> spaces >> parser << spaces << r


if __name__ == '__main__':
    from ReduceNatExp.data import ExpPlus

    infix(Parser(), ExpPlus)
