from EvalML4.parser import var, exp
from TypingML4.data import TypesInt, TypesBool, TypesFun, TypesList, EnvItem, Env
from TypingML4.rule import EvalToType
from bases.parser import Parser, string, pure, infixes, bracket, stringr, string2, sep_until

# __all__ = [
#     'value', 'value_int', 'value_bool', 'value_fn', 'value_rec', 'value_nil', 'value_cons',
#     'exp', 'exp_int', 'exp_bool', 'exp_if', 'exp_var', 'exp_let', 'exp_call', 'exp_fn', 'exp_rec', 'exp_match',
#     'exp_nil,'
#     'var',
#     'env_item', 'env',
#     'types', 'types_int', 'types_bool', 'types_list',
#     'assertion', 'eval_to_env', 'plus_is', 'minus_is', 'times_is', 'lt_is',
# ]

with Parser() as types:
    types_int = pure(TypesInt()) << string(r'int')

    types_bool = pure(TypesBool()) << string(r'bool')

    types_list = (pure(TypesList) << stringr(r'{')) + (types << string2(r'list') << string2(r'}'))

    types_term = bracket('(', types, ')') | types_list | types_int | types_bool

    types.define(infixes(types_term, TypesFun))

with Parser() as env:
    env_item = (pure(lambda a: lambda b: EnvItem(a, b)) + var + (string2(r':') >> types))

    env.define(pure(Env) + sep_until(env_item, ','))

with Parser() as assertion:
    eval_to_env = (pure(lambda env: lambda e: lambda t: EvalToType(env, e, t))) + \
                  (env << string2(r'|-')) + (exp << string2(r':')) + types
    assertion.define(eval_to_env)

if __name__ == '__main__':
    a = eval_to_env.run(r'|- 3 + 5 : int')
    print(a.args[0])
