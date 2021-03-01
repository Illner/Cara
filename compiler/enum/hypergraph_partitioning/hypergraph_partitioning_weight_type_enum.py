# Import
from enum import IntEnum, unique


@unique
class HypergraphPartitioningNodeWeightEnum(IntEnum):
    NONE = 1
    STATIC = 2
    DYNAMIC = 3


hpnw_enum_names = [hpnw.name for hpnw in HypergraphPartitioningNodeWeightEnum]
hpnw_enum_values = [hpnw.value for hpnw in HypergraphPartitioningNodeWeightEnum]


@unique
class HypergraphPartitioningHyperedgeWeightEnum(IntEnum):
    NONE = 1
    STATIC = 2
    DYNAMIC = 3


hphw_enum_names = [hphw.name for hphw in HypergraphPartitioningHyperedgeWeightEnum]
hphw_enum_values = [hphw.value for hphw in HypergraphPartitioningHyperedgeWeightEnum]
