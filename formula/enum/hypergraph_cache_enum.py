# Import
from enum import IntEnum, unique


@unique
class HypergraphCacheEnum(IntEnum):
    NONE = 1


hc_enum_names = [hc.name for hc in HypergraphCacheEnum]
hc_enum_values = [hc.value for hc in HypergraphCacheEnum]
