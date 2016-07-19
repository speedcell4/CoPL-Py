from typing import Tuple, Any, Callable

# TODO can not be parsed correctly now
EOF = '<EOF>'


# TODO
class ParsingError(Exception):
    pass


class Parser(object):
    def __init__(self, fn=None):
        self.fn = [fn]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def define(self, parser: 'Parser') -> None:
        self.fn = parser.fn

    def run(self, raw: str) -> Any:
        return self(raw)[1]

    def __call__(self, raw: str) -> Tuple[str, Any]:
        return self.fn[0](raw)

    def __add__(self, other: 'Parser') -> 'Parser':
        assert isinstance(other, Parser)

        def wrapper(raw: str) -> Tuple[str, Any]:
            try:
                raw1, ans1 = self(raw)
                raw2, ans2 = other(raw1)
                return raw2, ans1(ans2)
            except TypeError:
                return None

        return Parser(wrapper)

    def __or__(self, other: 'Parser') -> 'Parser':
        assert isinstance(other, Parser)

        def wrapper(raw: str) -> Tuple[str, Any]:
            return self(raw) or other(raw)

        return Parser(wrapper)

    def __lshift__(self, other: 'Parser') -> 'Parser':
        assert isinstance(other, Parser)

        def wrapper(raw: str) -> Tuple[str, Any]:
            try:
                raw1, ans1 = self(raw)
                raw2, ans2 = other(raw1)
                return raw2, ans1
            except TypeError:
                return None

        return Parser(wrapper)

    def __rshift__(self, other: 'Parser') -> 'Parser':
        assert isinstance(other, Parser)

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
        assert isinstance(raw, str)
        return raw, _

    return wrapper


def satisfy(condition: Callable[[str], bool]) -> Parser:
    @Parser
    def wrapper(raw: str):
        assert isinstance(raw, str)
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


def regex(pattern: str) -> Parser:
    import re
    pattern = re.compile(pattern if pattern.startswith(r'^') else r'^' + pattern)

    @Parser
    def wrapper(raw: str):
        match = pattern.match(raw)
        if match:
            return raw[match.span()[1]:], match.group()

    return wrapper


def string(const: str) -> Parser:
    assert isinstance(const, str)

    @Parser
    def wrapper(raw: str):
        assert isinstance(raw, str), raw

        if raw.startswith(const):
            return raw[len(const):], raw[:len(const)]

    return wrapper


eof = string(EOF)
