# Import
from enum import IntEnum, unique


@unique
class BaseClassEnum(IntEnum):
    TWO_CNF = 1
    RENAMABLE_HORN_CNF = 2


base_class_enum_names = [bs.name for bs in BaseClassEnum]
base_class_enum_values = [bs.value for bs in BaseClassEnum]
