import logging
from typing import List

from bases.parser import Parser, EOF, eof


class Assertion(object):
    args = ()
    template = ''

    def __str__(self):
        return self.template.format(*self.args)

    def __repr__(self):
        return str(self)


class Rule(object):
    name = ''

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        raise NotImplementedError

    def __str__(self):
        return self.name


class System(object):
    def __init__(self, rules: List[Rule]):
        assert isinstance(rules, list)
        self.rules = rules

    def __call__(self, assertion: Assertion, depth=0) -> str:
        def indent(n, char=r' '):
            return char * n * 2

        for rule in self.rules:
            try:
                logging.debug(r'{}try {} by using {}'.format(indent(depth), assertion, rule))
                subs = rule(assertion)
                logging.debug(r'{}fet {} by using {}'.format(indent(depth), subs, rule))
                if subs is None:
                    continue
                else:
                    head = indent(depth) + '{} by {} {{\n'.format(assertion, rule.name)
                    middle = ';\n'.join(self(sub, depth + 1) for sub in subs)
                    return head + middle + '\n' + indent(depth) + '}'
            except AssertionError:
                pass


class Solver(object):
    def __init__(self, parser: 'Parser', system: 'System'):
        self.parser = parser << eof
        self.system = system

    def __call__(self, raw: str) -> str:
        ast = self.parser.run(raw + EOF)
        logging.debug('parsing: {}'.format(ast))
        return self.system(ast)


class DeductionError(Exception):
    pass
