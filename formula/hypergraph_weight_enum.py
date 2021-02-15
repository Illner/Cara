# Import
from enum import IntEnum, unique


@unique
class HypergraphWeightEnum(IntEnum):
    NONE = 1
    STATIC = 2
    DYNAMIC = 3


hw_enum_names = [hw.name for hw in HypergraphWeightEnum]
hw_enum_values = [hw.value for hw in HypergraphWeightEnum]
