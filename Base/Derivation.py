from typing import List
from Base.Parser import Parser, EOF
from Base import util


class Assertion(object):
    args = ()
    template = ''

    def __str__(self):
        return self.template.format(*self.args)


class Rule(object):
    name = ''

    def __call__(self, assertion: Assertion) -> List[Assertion]:
        raise NotImplementedError


class System(object):
    def __init__(self, rules: List[Rule]):
        assert isinstance(rules, list)
        self.rules = rules

    def __call__(self, assertion: Assertion, depth=0) -> str:
        def indent(depth):
            return ' ' * depth * 2

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
            except AssertionError as e:
                pass


class Solver(object):
    def __init__(self, parser: 'Parser', system: 'System'):
        self.parser = parser
        self.system = system

    def __call__(self, raw: str) -> str:
        ast = self.parser.run(raw)
        if util.DEBUG:
            print('ast: {}'.format(ast))
        return self.system(ast)
