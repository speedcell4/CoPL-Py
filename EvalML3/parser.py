import EvalML2.parser as EvalML2
from EvalML2.parser import env, var, exp, exp_int, exp_bool, exp_var, exp_if, exp_let, EvalToEnv, plus_is, minus_is, \
    times_is, lt_is
from EvalML3.data import ExpPlus, ExpMinus, ExpTimes, ExpLt, \
    ValueFn, ValueRec, ExpCall, ExpFn, ExpRec
from bases.parser import Parser, string2, stringr, stringl, pure, spaces, bracket, infixes

with Parser() as value:
    value_fn = pure(lambda env: lambda x: lambda e: ValueFn(env, x, e)) + \
               (stringr(r'(') >> env << stringl(r')')) + \
               (stringr(r'[fun') >> var) + \
               (string2(r'->') >> exp << stringl(r']'))

    value_rec = pure(lambda env: lambda x: lambda y: lambda e: ValueRec(env, x, y, e)) + \
                (stringr(r'(') >> env << stringl(r')')) + \
                (stringr(r'[rec') >> var) + \
                (stringr(r'= fun') >> var) + \
                (string2(r'->') >> exp << stringl(r']'))

    value.define(value_fn | value_rec | EvalML2.value)

with Parser() as exp:
    exp_fn = pure(lambda x: lambda e: ExpFn(x, e)) + \
             (stringr(r'fun') >> var) + \
             (string2(r'->') >> exp)

    exp_call = (stringr(r'{') >> pure(lambda e1: lambda e2: ExpCall(e1, e2))) + \
               (exp << spaces) + \
               (exp << stringl(r'}'))

    exp_rec = pure(lambda x: lambda y: lambda e1: lambda e2: ExpRec(x, y, e1, e2)) + \
              (stringr(r'let rec') >> var) + \
              (string2(r'= fun') >> var) + \
              (string2(r'->') >> exp) + \
              (string2(r'in') >> exp)

    exp_term = bracket(r'(', exp,
                       r')') | exp_int | exp_bool | exp_rec | exp_let | exp_fn | exp_if | exp_call | exp_var

    exp.define(infixes(exp_term, ExpPlus, ExpMinus, ExpTimes, ExpLt))

with Parser() as assertion:
    eval_to_env = (pure(lambda env: lambda e: lambda v: EvalToEnv(env, e, v))) + \
                  (env << string2(r'|-')) + (exp << string2(r'evalto')) + value
    assertion.define(eval_to_env | plus_is | minus_is | times_is | lt_is)

import logging

logging.basicConfig(
    format=r'[%(levelname)s]%(asctime)s: %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S',
    level=logging.DEBUG,
)

if __name__ == '__main__':
    print(assertion.run(r'|- fun x -> x + 1 evalto ()[fun x -> x + 1]'))
