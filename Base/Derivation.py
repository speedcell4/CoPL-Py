from typing import List
from Base.Parser import Parser, EOF


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
        assert all(issubclass(rule, Rule) for rule in rules)
        self.rules = rules

    def __call__(self, assertion: Assertion, depth=0) -> str:
        def indent():
            return ' ' * depth * 2

        for rule in self.rules:
            subs = rule(assertion)
            if subs is None:
                continue
            else:
                head = indent() + '{} by {} {\n'.format(assertion, rule)
                mild = ';\n'.join(self(sub, depth + 1) for sub in subs)
                return head + mild + indent() + '\n}'


class Solver(object):
    def __init__(self, parser: 'Parser', system: 'System'):
        self.parser = parser
        self.system = system

    def __call__(self, raw: str) -> str:
        return self.system(self.parser.run(raw + EOF))
