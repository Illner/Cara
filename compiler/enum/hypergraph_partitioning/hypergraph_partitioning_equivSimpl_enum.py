# Import
from enum import IntEnum, unique


@unique
class HypergraphPartitioningEquivSimplEnum(IntEnum):
    NONE = 1
    STANDARD = 2
    EXTENDED = 3


hpes_enum_names = [hpes.name for hpes in HypergraphPartitioningEquivSimplEnum]
hpes_enum_values = [hpes.value for hpes in HypergraphPartitioningEquivSimplEnum]
