# Import
from enum import IntEnum, unique


@unique
class CircuitTypeEnum(IntEnum):
    NNF = 1
    BDMC = 2
    D_BDMC = 3
    S_NNF = 4
    S_BDMC = 5
    SD_BDMC = 6


circuit_type_enum_names = [ct.name for ct in CircuitTypeEnum]
circuit_type_enum_values = [ct.value for ct in CircuitTypeEnum]
