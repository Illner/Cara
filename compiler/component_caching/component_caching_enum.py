# Import
from enum import IntEnum, unique


@unique
class ComponentCachingEnum(IntEnum):
    C2D = 1
    NONE = 2


component_caching_enum_names = [cc.name for cc in ComponentCachingEnum]
component_caching_enum_values = [cc.value for cc in ComponentCachingEnum]
