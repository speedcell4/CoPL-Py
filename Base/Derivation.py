from typing import List
from base.parser import Parser, EOF, eof
from base import util


class Assertion(object):
    args = ()
    template = ''

    def __str__(self):
        return self.template.format(*self.args)


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
        def indent(n):
            return ' ' * n * 2

        for rule in self.rules:
            if util.DEBUG:
                print('rule: {}, assertion: {}'.format(rule, assertion))
            try:
                subs = rule(assertion)
                if subs is None:
                    continue
                else:
                    head = indent(depth) + '{} by {} {{\n'.format(assertion, rule.name)
                    mild = ';\n'.join(self(sub, depth + 1) for sub in subs)
                    return head + mild + '\n' + indent(depth) + '}'
            except AssertionError as _:
                pass


class Solver(object):
    def __init__(self, parser: 'Parser', system: 'System'):
        self.parser = parser << eof
        self.system = system

    def __call__(self, raw: str) -> str:
        ast = self.parser.run(raw + EOF)
        if util.DEBUG:
            print('ast: {}'.format(ast))
        return self.system(ast)
