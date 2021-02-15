# Import
from enum import IntEnum, unique


@unique
class HypergraphSoftwareEnum(IntEnum):
    HMETIS = 1


hs_enum_names = [hs.name for hs in HypergraphSoftwareEnum]
hs_enum_values = [hs.value for hs in HypergraphSoftwareEnum]
