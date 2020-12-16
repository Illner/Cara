# Import
from enum import IntEnum, unique


@unique
class CircuitTypeEnum(IntEnum):
    D_BDMC = 1
    SD_BDMC = 2


circuit_type_enum_names = [ct.name for ct in CircuitTypeEnum]
circuit_type_enum_values = [ct.value for ct in CircuitTypeEnum]
