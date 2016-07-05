from typing import List

TYPE_NOT_SAME = '{} and {} is not the same type'
TYPE_NOT_MATCH = 'the value of {} is not {} type'

NOT_IN_ENVIRONMENT = '{} is not in environment'


class Value(object):
    def __str__(self):
        raise NotImplementedError


class ValInt(Value):
    def __init__(self, i: int):
        assert isinstance(i, int)
        self.i = i

    def __str__(self):
        return '{}'.format(self.i)

    def __eq__(self, other: 'Value') -> bool:
        if isinstance(other, ValInt):
            return self.i == other.i
        else:
            raise TypeError(TYPE_NOT_SAME.format(self, other))

    def __add__(self, other: 'Value') -> 'ValInt':
        if isinstance(other, ValInt):
            return ValInt(self.i + other.i)
        else:
            raise TypeError(TYPE_NOT_SAME.format(self, other))

    def __sub__(self, other: 'Value') -> 'ValInt':
        if isinstance(other, ValInt):
            return ValInt(self.i - other.i)
        else:
            raise TypeError(TYPE_NOT_SAME.format(self, other))

    def __mul__(self, other: 'Value') -> 'ValInt':
        if isinstance(other, ValInt):
            return ValInt(self.i - other.i)
        else:
            raise TypeError(TYPE_NOT_SAME.format(self, other))

    def __lt__(self, other: 'Value') -> 'ValBool':
        if isinstance(other, ValInt):
            return ValBool(self.i < other.i)
        else:
            raise TypeError(TYPE_NOT_SAME.format(self, other))


class ValBool(Value):
    def __init__(self, b: bool):
        assert isinstance(b, bool)
        self.b = b

    def __str__(self):
        return '{}'.format(self.b).lower()

    def __eq__(self, other: 'Value') -> bool:
        if isinstance(other, ValBool):
            return self.b == other.b
        else:
            raise TypeError(TYPE_NOT_SAME.format(self, other))


class Var(Value):
    def __init__(self, x: str):
        assert isinstance(x, str)
        self.x = x

    def __str__(self):
        return '{}'.format(self.x)


class ValFn(Value):
    def __init__(self, env: 'Env', x: 'Var', e: 'Exp'):
        assert isinstance(env, Env)
        assert isinstance(x, Var)
        assert isinstance(e, Exp)
        self.env = env
        self.x = x
        self.e = e

    def __str__(self):
        return '({})[fun {} -> {}]'.format(self.env, self.x, self.env)


class ValRec(Value):
    def __init__(self, env: 'Env', x: 'Var', y: 'Var', e: 'Exp'):
        assert isinstance(env, Env)
        assert isinstance(x, Var)
        assert isinstance(y, Var)
        assert isinstance(e, Exp)
        self.env = env
        self.x = x
        self.y = y
        self.e = e

    def __str__(self):
        return 'let rec {} = fun {} -> {} in {}'.format(self.env, self.x, self.y, self.e)


class Exp(object):
    posterior = []  # type: List[Exp]

    # TODO use priority? or posterior list?
    def _parameter(self, a: 'Exp'):
        if isinstance(a, self.posterior):
            return '({})'.format(a)
        else:
            return '{}'.format(a)

    def eval(self, env: 'Env') -> 'Value':
        raise NotImplementedError


class ExpInt(Exp):
    def __init__(self, i: 'ValInt'):
        assert isinstance(i, ValInt)
        self.i = i

    def eval(self, env: 'Env') -> 'Value':
        return ValInt(self.i.i)


class ExpBool(Exp):
    def __init__(self, b: 'ValBool'):
        assert isinstance(b, ValBool)
        self.b = b

    def eval(self, env: 'Env') -> 'Value':
        return ValBool(self.b.b)


class ExpVar(Exp):
    def __init__(self, x: 'Var'):
        assert isinstance(x, Var)
        self.x = x

    def eval(self, env: 'Env') -> 'Value':
        for item in env.env_items.reverse():  # type: EnvItem
            if item.x.x == self.x:
                return item.v
        raise IndexError(NOT_IN_ENVIRONMENT.format(self.x))


class ExpPlus(Exp):
    def __init__(self, a: 'Exp', b: 'Exp'):
        assert isinstance(a, Exp)
        assert isinstance(b, Exp)
        self.a = a
        self.b = b

    def __str__(self):
        return '{} + {}'.format(self.a, self.b)

    def eval(self, env: 'Env') -> 'ValInt':
        av = self.a.eval(env)
        bv = self.b.eval(env)
        if isinstance(av, ValInt) and isinstance(bv, ValInt):
            return av + bv
        else:
            raise TypeError(TYPE_NOT_SAME.format(av, bv))


class ExpMinus(Exp):
    def __init__(self, a: 'Exp', b: 'Exp'):
        assert isinstance(a, Exp)
        assert isinstance(b, Exp)
        self.a = a
        self.b = b

    def __str__(self):
        return '{} - {}'.format(self.a, self.b)

    def eval(self, env: 'Env') -> 'ValInt':
        av = self.a.eval(env)
        bv = self.b.eval(env)
        if isinstance(av, ValInt) and isinstance(bv, ValInt):
            return av - bv
        else:
            raise TypeError(TYPE_NOT_SAME.format(av, bv))


class ExpTimes(Exp):
    def __init__(self, a: 'Exp', b: 'Exp'):
        assert isinstance(a, Exp)
        assert isinstance(b, Exp)
        self.a = a
        self.b = b

    def __str__(self):
        return '{} * {}'.format(self.a, self.b)

    def eval(self, env: 'Env') -> 'ValInt':
        av = self.a.eval(env)
        bv = self.b.eval(env)
        if isinstance(av, ValInt) and isinstance(bv, ValInt):
            return av * av
        else:
            raise TypeError(TYPE_NOT_SAME.format(av, bv))


class ExpLt(Exp):
    def __init__(self, a: 'Exp', b: 'Exp'):
        assert isinstance(a, Exp)
        assert isinstance(b, Exp)
        self.a = a
        self.b = b

    def __str__(self):
        return '{} < {}'.format(self.a, self.b)

    def eval(self, env: 'Env') -> 'ValBool':
        av = self.a.eval(env)
        bv = self.b.eval(env)
        if isinstance(av, ValInt) and isinstance(bv, ValInt):
            return av < bv
        else:
            raise TypeError(TYPE_NOT_SAME.format(av, bv))


class ExpIf(Exp):
    def __init__(self, e1: 'Exp', e2: 'Exp', e3: 'Exp'):
        assert isinstance(e1, Exp)
        assert isinstance(e2, Exp)
        assert isinstance(e3, Exp)
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3

    def __str__(self):
        return 'if {} then {} else {}'.format(self.e1, self.e2, self.e3)

    def eval(self, env: 'Env') -> 'Value':
        ev1 = self.e1.eval(env)
        if isinstance(ev1, ValBool):
            if ev1.b:
                return self.e2.eval(env)
            else:
                return self.e3.eval(env)
        raise TypeError(TYPE_NOT_MATCH.format(self.e1, ValBool.__name__))


class ExpLet(Exp):
    def eval(self, env: 'Env') -> 'Value':
        return self.e2.eval(env + EnvItem(self.x, self.e1.eval(env)))

    def __init__(self, x: 'Var', e1: 'Exp', e2: 'Exp'):
        assert isinstance(x, Var)
        assert isinstance(e1, Exp)
        assert isinstance(e2, Exp)
        self.x = x
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return 'let {} = {} in {}'.format(self.x, self.e1, self.e2)


class ExpFn(Exp):
    def eval(self, env: 'Env') -> 'ValFn':
        return ValFn(env, self.x, self.e)

    def __init__(self, x: 'Var', e: 'Exp'):
        assert isinstance(x, Var)
        assert isinstance(e, Exp)
        self.x = x
        self.e = e

    def __str__(self):
        return 'fun {} -> {}'.format(self.x, self.e)


class ExpCall(Exp):
    def eval(self, env: 'Env') -> 'Value':
        v1 = self.e1.eval(env)
        v2 = self.e1.eval(env)
        if isinstance(v1, ValFn):
            env2, x, e0 = v1.env, v1.x, v1.e
            return e0.eval(env2 + EnvItem(x, v2))
        elif isinstance(v1, ValRec):
            env2, x, y, e0 = v1.env, v1.x, v1.y, v1.e
            return e0.eval(env2 + EnvItem(x, ValRec(env2, x, y, e0)) + EnvItem(y, v2))
        else:
            raise TypeError(TYPE_NOT_MATCH.format(v1, '{} or {}'.format(ValFn.__name__, ValRec.__name__)))

    def __init__(self, e1: 'Exp', e2: 'Exp'):
        assert isinstance(e1, Exp)
        assert isinstance(e2, Exp)
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return '{} {}'.format(self.e1, self.e2)


class ExpRec(Exp):
    def eval(self, env: 'Env') -> 'Value':
        pass

    def __init__(self, x: 'Var', y: 'Var', e1: 'Exp', e2: 'Exp'):
        assert isinstance(x, Var)
        assert isinstance(y, Var)
        assert isinstance(e1, Exp)
        assert isinstance(e2, Exp)
        self.x = x
        self.y = y
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return 'let rec {} = fun {} -> {} in {}'.format(self.x, self.y, self.e1, self.e2)


class EnvItem(object):
    def __init__(self, x: 'Var', v: 'Value'):
        assert isinstance(x, Var)
        assert isinstance(v, Value)
        self.x = x
        self.v = v

    def __str__(self):
        return '{} = {}'.format(self.x, self.v)

    def __eq__(self, other: 'EnvItem') -> bool:
        assert isinstance(other, EnvItem)
        return self.x == other.x and self.v == other.v


class Env(object):
    def __init__(self, env_items: List['EnvItem']):
        assert isinstance(env_items, list) and all(isinstance(item, EnvItem) for item in env_items)
        self.env_items = env_items

    def __str__(self):
        return ', '.join(str(item) for item in self.env_items)

    def __eq__(self, other: 'Env') -> bool:
        assert isinstance(other, Env)
        a = dict({item.x: item.v for item in self.env_items})
        b = dict({item.x: item.v for item in other.env_items})
        return a == b

    def __add__(self, other: 'EnvItem') -> 'Env':
        assert isinstance(other, EnvItem)
        if self.env_items and self.env_items[-1].x == other.x:
            return Env(self.env_items[:-1] + [other])
        else:
            return Env(self.env_items[:] + [other])
