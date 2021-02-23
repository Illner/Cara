# Import
from enum import IntEnum, unique


@unique
class ImpliedLiteralsEnum(IntEnum):
    BCP = 1
    IMPLICIT_BCP = 2
    BACKBONE = 3
    NONE = 4


implied_literals_enum_names = [il.name for il in ImpliedLiteralsEnum]
implied_literals_enum_values = [il.value for il in ImpliedLiteralsEnum]
