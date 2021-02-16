# Import
from enum import IntEnum, unique


@unique
class HypergraphNodeWeightEnum(IntEnum):
    NONE = 1
    STATIC = 2
    DYNAMIC = 3


hnw_enum_names = [hnw.name for hnw in HypergraphNodeWeightEnum]
hnw_enum_values = [hnw.value for hnw in HypergraphNodeWeightEnum]


@unique
class HypergraphHyperedgeWeightEnum(IntEnum):
    NONE = 1
    STATIC = 2
    DYNAMIC = 3


hhw_enum_names = [hhw.name for hhw in HypergraphHyperedgeWeightEnum]
hhw_enum_values = [hhw.value for hhw in HypergraphHyperedgeWeightEnum]
