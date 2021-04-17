# Import
from enum import IntEnum, unique


@unique
class HypergraphPartitioningSoftwareEnum(IntEnum):
    HMETIS = 1
    PATOH = 2
    KAHYPAR = 3
    NONE = 4


hps_enum_names = [hps.name for hps in HypergraphPartitioningSoftwareEnum]
hps_enum_values = [hps.value for hps in HypergraphPartitioningSoftwareEnum]
