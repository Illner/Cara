# Import
from enum import IntEnum, unique


@unique
class CircuitTypeEnum(IntEnum):
    NNF = 1
    DNNF = 2
    D_DNNF = 3
    S_DNNF = 4
    SD_DNNF = 5

    BDMC = 6
    D_BDMC = 7
    S_BDMC = 8
    SD_BDMC = 9

    CARA = 10
    D_CARA = 11
    S_CARA = 12
    SD_CARA = 13

    UNDEFINED = 14


circuit_type_enum_names = [ct.name for ct in CircuitTypeEnum]
circuit_type_enum_values = [ct.value for ct in CircuitTypeEnum]
