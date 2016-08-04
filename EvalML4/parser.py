from EvalML3.parser import value_rec, value_fn, value_int, value_bool, var, exp_int, exp_bool, exp_var, env
from EvalML4.data import *
from EvalML4.rule import EvalToEnv
from bases.parser import Parser, pure, string, curry2, curry5, string2, stringl, stringr, bracket, infixes, spaces

with Parser() as value:
    value_nil = pure(ValueNil()) << string(r'[]')

    value_cons = pure(curry2(ValueCons)) + (value_nil | value_rec | value_fn | value_int | value_bool) + (
        string2(r'::') >> value)

    value.define(value_nil | value_cons | value_rec | value_fn | value_int | value_bool)

with Parser() as exp:
    exp_fn = pure(lambda x: lambda e: ExpFn(x, e)) + \
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

    exp_call = (stringr(r'{') >> pure(lambda e1: lambda e2: ExpCall(e1, e2))) + \
               (exp << spaces) + \
               (exp << stringl(r'}'))

    exp_rec = pure(lambda x: lambda y: lambda e1: lambda e2: ExpRec(x, y, e1, e2)) + \
              (stringr(r'let rec') >> var) + \
              (string2(r'= fun') >> var) + \
              (string2(r'->') >> exp) + \
              (string2(r'in') >> exp)

    exp_nil = pure(ExpNil()) << string(r'[]')

    exp_match = pure(curry5(ExpMatch)) + \
                (stringr(r'match') >> exp) + \
                (string2(r'with') >> string2(r'[]') >> string2(r'->') >> exp) + \
                (string2(r'|') >> var) + \
                (string2(r'::') >> var) + \
                (string2(r'->') >> exp)

    exp_term = bracket(r'(', exp, r')') | exp_nil | exp_match | \
               exp_int | exp_bool | exp_fn | exp_rec | exp_let | exp_if | exp_call | exp_var

    exp.define(infixes(exp_term, ExpPlus, ExpMinus, ExpTimes, ExpLt, ExpCons))

with Parser() as assertion:
    eval_to_env = (pure(lambda env: lambda e: lambda v: EvalToEnv(env, e, v))) + \
                  (env << string2(r'|-')) + (exp << string2(r'evalto')) + value
    assertion.define(eval_to_env)

if __name__ == '__main__':
    print(value.run(r'5'))
