import logging

from EvalML1.data import ValueInt, ValueBool, ExpInt, ExpBool, ExpPlus, ExpMinus, ExpTimes, ExpLt, ExpIf
from bases.parser import Parser, pure, string, stringr, string2, digits, bracket, infixes

with Parser() as value:
    value_int = (pure(lambda ds: ValueInt(int(ds)))) + digits
    value_bool = (string(r'true') >> pure(ValueBool(True))) | (string(r'false') >> pure(ValueBool(False)))

    value.define(value_int | value_bool)

with Parser() as exp:
    exp_int = (pure(lambda v: ExpInt(v.i))) + value_int
    exp_bool = (pure(lambda v: ExpBool(v.b))) + value_bool
    exp_if = (pure(lambda a: lambda b: lambda c: ExpIf(a, b, c))) + \
             (stringr(r'if') >> exp) + \
             (string2(r'then') >> exp) + \
             (string2(r'else') >> exp)
    exp_term = bracket(r'(', exp, r')') | exp_int | exp_bool

    exp.define(infixes(exp_term, ExpPlus, ExpMinus, ExpTimes, ExpLt))

logging.basicConfig(
    format=r'[%(levelname)s]%(asctime)s: %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S',
    level=logging.DEBUG,
)

if __name__ == '__main__':
    print(exp.run(r'1+2+3+4+5+6'))
