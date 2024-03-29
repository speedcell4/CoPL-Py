from EvalML2.parser import *
from EvalML2.rule import EvalToEnv
from EvalML3.data import *
from bases.parser import Parser, string2, stringr, stringl, pure, spaces, bracket, infixes

__all__ = [
    'value', 'value_int', 'value_bool', 'value_fn', 'value_rec',
    'exp', 'exp_int', 'exp_bool', 'exp_if', 'exp_var', 'exp_let', 'exp_app', 'exp_fun', 'exp_let_rec',
    'var',
    'env_item', 'env',
    'assertion', 'eval_to', 'plus_is', 'minus_is', 'times_is', 'lt_is',
]

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

    value.define(value_fn | value_rec | value_int | value_int)

with Parser() as exp:
    exp_fun = pure(lambda x: lambda e: ExpFun(x, e)) + \
              (stringr(r'fun') >> var) + \
              (string2(r'->') >> exp)

    exp_if = (pure(lambda a: lambda b: lambda c: ExpIf(a, b, c))) + \
             (string2(r'if') >> exp) + \
             (string2(r'then') >> exp) + \
             (string2(r'else') >> exp)

    exp_let = (pure(lambda a: lambda b: lambda c: ExpLet(a, b, c))) + \
              (string2(r'let') >> var) + \
              (string2(r'=') >> exp) + \
              (string2(r'in') >> exp)

    exp_app = (stringr(r'{') >> pure(lambda e1: lambda e2: ExpApp(e1, e2))) + \
              (exp << spaces) + \
              (exp << stringl(r'}'))

    exp_let_rec = pure(lambda x: lambda y: lambda e1: lambda e2: ExpLetRec(x, y, e1, e2)) + \
                  (stringr(r'let rec') >> var) + \
                  (string2(r'= fun') >> var) + \
                  (string2(r'->') >> exp) + \
                  (string2(r'in') >> exp)

    exp_term = bracket(r'(', exp,
                       r')') | exp_int | exp_bool | exp_fun | exp_let_rec | exp_let | exp_if | exp_app | exp_var

    exp.define(infixes(exp_term, ExpPlus, ExpMinus, ExpTimes, ExpLt))

with Parser() as assertion:
    eval_to_env = (pure(lambda env: lambda e: lambda v: EvalToEnv(env, e, v))) + \
                  (env << string2(r'|-')) + (exp << string2(r'evalto')) + value
    assertion.define(eval_to_env | plus_is | minus_is | times_is | lt_is)

if __name__ == '__main__':
    print(exp.run(r'let y = 2 in fun x -> x + y'))
