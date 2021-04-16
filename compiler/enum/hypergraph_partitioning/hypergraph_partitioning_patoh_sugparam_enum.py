# Import
from enum import IntEnum, unique


@unique
class PatohSugparamEnum(IntEnum):
    PATOH_SUGPARAM_SPEED = 1
    PATOH_SUGPARAM_QUALITY = 2


patoh_sugparam_enum_names = [ps.name for ps in PatohSugparamEnum]
patoh_sugparam_enum_values = [ps.value for ps in PatohSugparamEnum]
