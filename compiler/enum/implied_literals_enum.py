# Import
from enum import IntEnum, unique


@unique
class ImpliedLiteralsEnum(IntEnum):
    BCP = 1
    IMPLICIT_BCP = 2
    IMPLICIT_BCP_ITERATION = 3
    BACKBONE = 4
    NONE = 5


implied_literals_enum_names = [il.name for il in ImpliedLiteralsEnum]
implied_literals_enum_values = [il.value for il in ImpliedLiteralsEnum]


@unique
class FirstImpliedLiteralsEnum(IntEnum):
    IMPLICIT_BCP = 1
    IMPLICIT_BCP_ITERATION = 2
    BACKBONE = 3


first_implied_literals_enum_names = [fil.name for fil in FirstImpliedLiteralsEnum]
first_implied_literals_enum_values = [fil.value for fil in FirstImpliedLiteralsEnum]
