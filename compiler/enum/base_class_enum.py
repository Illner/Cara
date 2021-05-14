# Import
from enum import IntEnum, unique


@unique
class BaseClassEnum(IntEnum):
    TWO_CNF = 1
    RENAMABLE_HORN_CNF = 2


base_class_enum_names = [bc.name for bc in BaseClassEnum]
base_class_enum_values = [bc.value for bc in BaseClassEnum]
