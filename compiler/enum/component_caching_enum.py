# Import
from enum import IntEnum, unique


@unique
class ComponentCachingEnum(IntEnum):
    NONE = 1
    STANDARD_CACHING_SCHEME = 2     # Cachet
    HYBRID_CACHING_SCHEME = 3       # sharpSAT
    BASIC_CACHING_SCHEME = 4
    CARA_CACHING_SCHEME = 5


component_caching_enum_names = [cc.name for cc in ComponentCachingEnum]
component_caching_enum_values = [cc.value for cc in ComponentCachingEnum]
