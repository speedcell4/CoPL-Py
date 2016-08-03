from EvalML1.parser import value, exp_int, exp_bool, plus_is, minus_is, times_is, lt_is
from EvalML2.data import Var, EnvItem, Env, ExpVar, ExpPlus, ExpMinus, ExpTimes, ExpLt, ExpLet, ExpIf
from EvalML2.rule import EvalToEnv
from bases.parser import Parser, alphas, pure, string2, sep_until, infixes, bracket

with Parser() as var:
    var.define(pure(Var) + alphas)

with Parser() as env:
    env_item = (pure(lambda a: lambda b: EnvItem(a, b)) + var + (string2(r'=') >> value))

    env.define(pure(Env) + sep_until(env_item, ','))

with Parser() as exp:
    exp_var = (pure(ExpVar)) + var

    exp_if = (pure(lambda a: lambda b: lambda c: ExpIf(a, b, c))) + \
             (string2(r'if') >> exp) + \
             (string2(r'then') >> exp) + \
             (string2(r'else') >> exp)

    exp_let = (pure(lambda a: lambda b: lambda c: ExpLet(a, b, c))) + \
              (string2(r'let') >> var) + \
              (string2(r'=') >> exp) + \
              (string2(r'in') >> exp)
    exp_term = bracket(r'(', exp, r')') | exp_int | exp_bool | exp_if | exp_let | exp_var

    exp.define(infixes(exp_term, ExpPlus, ExpMinus, ExpTimes, ExpLt))

with Parser() as assertion:
    eval_to_env = (pure(lambda env: lambda e: lambda v: EvalToEnv(env, e, v))) + \
                  (env << string2(r'|-')) + (exp << string2(r'evalto')) + value
    assertion.define(eval_to_env | plus_is | minus_is | times_is | lt_is)

if __name__ == '__main__':
    print(exp_let.run(r'let x = 1 + 2 in x * 4'))
