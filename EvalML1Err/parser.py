import EvalML1.parser as EvalML1
from EvalML1.parser import exp
from EvalML1Err.data import ResErr
from EvalML1Err.rule import EvalToErr
from bases.parser import Parser, string, pure, string2

with Parser() as res:
    res_err = string(r'error') >> pure(ResErr())
    res.define(res_err)

with Parser() as assertion:
    eval_to_err = pure(lambda a: lambda b: EvalToErr(a, b)) + exp + (string2(r'evalto') >> res)
    assertion.define(eval_to_err | EvalML1.assertion)

if __name__ == '__main__':
    print(assertion.run(r'1 + true + 2 evalto error'))
