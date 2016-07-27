from EvalML1.data import ValueInt, ValueBool
from bases.parser import Parser, pure, string, digits

with Parser() as value:
    int_ = (pure(lambda ds: ValueInt(int(ds)))) + digits
    bool_ = (string(r'true') >> pure(ValueBool(True))) | (string(r'false') >> pure(ValueBool(False)))

    value.define(int_ | bool_)

with Parser() as exp:
    pass

if __name__ == '__main__':
    print(value.run(r'true'))
