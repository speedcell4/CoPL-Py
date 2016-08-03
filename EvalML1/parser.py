import logging

from EvalML1.data import ValueInt, ValueBool, ExpInt, ExpBool, ExpPlus, ExpMinus, ExpTimes, ExpLt, ExpIf
from EvalML1.rule import EvalTo, PlusIs, MinusIs, TimesIs, LtIs
from bases.parser import Parser, pure, string, stringr, string2, digits, bracket, infixes

with Parser() as value:
    value_pos = (pure(lambda ds: ValueInt(int(ds)))) + digits
    value_neg = (pure(lambda ds: ValueInt(-int(ds)))) + (string(r'-') >> digits)
    value_int = value_neg | value_pos
    value_bool = (string(r'true') >> pure(ValueBool(True))) | (string(r'false') >> pure(ValueBool(False)))

    value.define(value_int | value_bool)

with Parser() as exp:
    exp_int = (pure(lambda v: ExpInt(v.i))) + value_int
    exp_bool = (pure(lambda v: ExpBool(v.b))) + value_bool
    exp_if = (pure(lambda a: lambda b: lambda c: ExpIf(a, b, c))) + \
             (stringr(r'if') >> exp) + \
             (string2(r'then') >> exp) + \
             (string2(r'else') >> exp)
    exp_term = bracket(r'(', exp, r')') | exp_int | exp_bool | exp_if

    exp.define(infixes(exp_term, ExpPlus, ExpMinus, ExpTimes, ExpLt))

with Parser() as assertion:
    eval_to = (pure(lambda a: lambda b: EvalTo(a, b))) + \
              (exp << string2(r'evalto')) + \
              value
    plus_is = (pure(lambda a: lambda b: lambda c: PlusIs(a, b, c))) + \
              value_int + (string2(r'plus') >> value_int) + (string2(r'is') + value_int)

    minus_is = (pure(lambda a: lambda b: lambda c: MinusIs(a, b, c))) + \
               value_int + (string2(r'minus') >> value_int) + (string2(r'is') + value_int)

    times_is = (pure(lambda a: lambda b: lambda c: TimesIs(a, b, c))) + \
               value_int + (string2(r'times') >> value_int) + (string2(r'is') + value_int)

    lt_is = (pure(lambda a: lambda b: lambda c: LtIs(a, b, c))) + \
            value_int + (string2(r'less than') >> value_int) + (string2(r'is') + value_bool)

    assertion.define(eval_to | plus_is | minus_is | times_is | lt_is)

logging.basicConfig(
    format=r'[%(levelname)s]%(asctime)s: %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S',
    level=logging.DEBUG,
)

if __name__ == '__main__':
    print(assertion.run(r'3+4 evalto 7'))
