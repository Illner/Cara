# Import
from enum import IntEnum, unique


@unique
class HypergraphPartitioningVariableSimplificationEnum(IntEnum):
    NONE = 1
    EQUIV_SIMPL = 2


hpvs_enum_names = [hpvs.name for hpvs in HypergraphPartitioningVariableSimplificationEnum]
hpvs_enum_values = [hpvs.value for hpvs in HypergraphPartitioningVariableSimplificationEnum]
