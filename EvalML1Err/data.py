from EvalML1.data import Value, ValueInt, ValueBool
from bases.util import type_checking


class Res(Value):
    pass


class ResInt(Res, ValueInt):
    pass


class ResBool(Res, ValueBool):
    pass


class ResError(Res):
    @type_checking
    def __str__(self) -> str:
        return r'error'

    @type_checking
    def __eq__(self, other: 'Res') -> bool:
        return NotImplementedError
