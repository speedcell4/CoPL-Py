import logging

from EvalML1.data import ValueInt, ValueBool, ExpInt, ExpBool, ExpPlus, ExpMinus, ExpIf
from bases.parser import Parser, pure, string, stringr, string2, digits, bracket, infixes

with Parser() as value:
    _value_int_ = (pure(lambda ds: ValueInt(int(ds)))) + digits
    _value_bool_ = (string(r'true') >> pure(ValueBool(True))) | (string(r'false') >> pure(ValueBool(False)))

    value.define(_value_int_ | _value_bool_)

with Parser() as exp:
    _exp_int_ = (pure(lambda v: ExpInt(v.i))) + _value_int_
    _exp_bool_ = (pure(lambda v: ExpBool(v.b))) + _value_bool_
    _exp_if_ = (pure(lambda a: lambda b: lambda c: ExpIf(a, b, c))) + \
               (stringr(r'if') >> exp) + \
               (string2(r'then') >> exp) + \
               (string2(r'else') >> exp)
    _exp_term_ = bracket(r'(', exp, r')') | _exp_int_ | _exp_bool_
    exp.define(infixes(_exp_term_, ExpPlus, ExpMinus))

logging.basicConfig(
    format=r'[%(levelname)s]%(asctime)s: %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S',
    level=logging.DEBUG,
)

if __name__ == '__main__':
    print(exp.run(r'5'))
