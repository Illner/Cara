# Import
from enum import IntEnum, unique


@unique
class HypergraphPartitioningCacheEnum(IntEnum):
    NONE = 1
    ISOMORFISM = 2


hpc_enum_names = [hpc.name for hpc in HypergraphPartitioningCacheEnum]
hpc_enum_values = [hpc.value for hpc in HypergraphPartitioningCacheEnum]
