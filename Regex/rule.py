import logging
from typing import Iterable

from Regex.data import Regex, RegexEmpty, RegexLiteral, RegexConcatenation, RegexAlternation, RegexKleene
from bases.derivation import Assertion, Rule
from bases.util import type_checking

DerivationError = TypeError


class Matches(Assertion):
    template = r'{} matches {}'

    @type_checking
    def __init__(self, regex: Regex, string: str):
        self.args = (regex, string)

    @type_checking
    def __str__(self) -> str:
        return r'{} matches {}'.format(*self.args)

    @type_checking
    def __repr__(self) -> str:
        return str(self)


class REmpty(Rule):
    name = r'R-Empty'

    @type_checking
    def __call__(self, assertion: Matches) -> Iterable[Assertion]:
        regex, string = assertion.args
        logging.debug(r'{} {} {}'.format(self.__class__.__name__, regex, string))
        if isinstance(regex, RegexEmpty) and string == r'':
            yield []
        raise DerivationError(self.__class__.__name__)


class RLiteral(Rule):
    name = r'R-Literal'

    @type_checking
    def __call__(self, assertion: Matches) -> Iterable[Assertion]:
        regex, string = assertion.args
        logging.debug(r'{} {} {}'.format(self.__class__.__name__, regex, string))
        if isinstance(regex, RegexLiteral):
            if regex.char == string:
                yield []
        raise DerivationError(self.__class__.__name__)


class RConcatenation(Rule):
    name = r'R-Concatenation'

    @type_checking
    def __call__(self, assertion: Matches) -> Iterable[Assertion]:
        regex, string = assertion.args
        logging.debug(r'{} {} {}'.format(self.__class__.__name__, regex, string))
        if isinstance(regex, RegexConcatenation):
            r1, r2 = regex.r1, regex.r2
            for pivot in range(0, len(string) + 1):
                yield [
                    Matches(r1, string[:pivot]),
                    Matches(r2, string[pivot:]),
                ]
        raise DerivationError(self.__class__.__name__)


class RAlternationL(Rule):
    name = r'R-AlternationL'

    @type_checking
    def __call__(self, assertion: Matches) -> Iterable[Assertion]:
        regex, string = assertion.args
        logging.debug(r'{} {} {}'.format(self.__class__.__name__, regex, string))
        if isinstance(regex, RegexAlternation):
            r1, r2 = regex.r1, regex.r2
            yield [Matches(r1, string)]
        raise DerivationError(self.__class__.__name__)


class RAlternationR(Rule):
    name = r'R-AlternationR'

    @type_checking
    def __call__(self, assertion: Matches) -> Iterable[Assertion]:
        regex, string = assertion.args
        logging.debug(r'{} {} {}'.format(self.__class__.__name__, regex, string))
        if isinstance(regex, RegexAlternation):
            r1, r2 = regex.r1, regex.r2
            yield [Matches(r2, string)]
        raise DerivationError(self.__class__.__name__)


class RKleene0(Rule):
    name = r'R-Kleene0'

    @type_checking
    def __call__(self, assertion: Assertion) -> Iterable[Assertion]:
        regex, string = assertion.args
        logging.debug(r'{} {} {}'.format(self.__class__.__name__, regex, string))
        if isinstance(regex, RegexKleene):
            if string == '':
                yield []
        raise DerivationError(self.__class__.__name__)


class RKleene1(Rule):
    name = r'R-Kleene1'

    @type_checking
    def __call__(self, assertion: Assertion) -> Iterable[Assertion]:
        regex, string = assertion.args
        logging.debug(r'{} {} {}'.format(self.__class__.__name__, regex, string))
        if isinstance(regex, RegexKleene):
            regex0 = regex.r
            for pivot in range(1, len(string) + 1):
                yield [
                    Matches(regex0, string[:pivot]),
                    Matches(regex, string[pivot:]),
                ]
        raise DerivationError(self.__class__.__name__)


class DerivationSystem(object):
    rules = [REmpty(), RLiteral(), RConcatenation(), RAlternationL(), RAlternationR(), RKleene0(), RKleene1()]

    def __call__(self, assertion: Assertion, depth=0) -> str:
        def indent(n, char=r' '):
            return char * n * 2

        for rule in self.rules:
            try:
                for subs in rule(assertion):
                    try:
                        logging.warning(r'{}try {} by using {}'.format(indent(depth), assertion, rule))
                        # subs = rule(assertion)
                        logging.debug(r'{}fet {} by using {}'.format(indent(depth), subs, rule))
                        if subs is None:
                            continue
                        else:
                            head = indent(depth) + '{} by {} {{\n'.format(assertion, rule.name)
                            middle = ',\n'.join(self(sub, depth + 1) for sub in subs)
                            return head + middle + '\n' + indent(depth) + '}'
                    except AssertionError:
                        pass
                    except Exception as error:
                        logging.error('{}'.format(error))
            except TypeError:
                pass


derivation_system = DerivationSystem()

logging.basicConfig(
    format=r'[%(levelname)s- %(funcName)s]%(asctime)s: %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S',
    level=logging.WARNING,
)

if __name__ == '__main__':
    r1 = RegexConcatenation(
        RegexLiteral('a'),
        RegexKleene(RegexConcatenation(RegexLiteral('b'), RegexLiteral('c'))))

    match1 = Matches(r1, 'abcbcbc')

    r2 = RegexEmpty()

    match2 = Matches(r2, '')

    r3 = RegexConcatenation(
        RegexKleene(RegexAlternation(
            RegexConcatenation(RegexLiteral('a'), RegexLiteral('a')),
            RegexConcatenation(RegexLiteral('b'), RegexLiteral('b'))
        )),
        RegexLiteral('c'))

    match3 = Matches(r3, 'bbaac')

    print(derivation_system(match3))
