# Import
from enum import IntEnum, unique


@unique
class BaseClassEnum(IntEnum):
    LITERAL = 1
    QUADRATIC = 2
    MATCHED = 3
    HORN = 4
    HIDDEN_HORN = 5
    Q_HORN = 6


base_class_enum_names = [bs.name for bs in BaseClassEnum]
base_class_enum_values = [bs.value for bs in BaseClassEnum]
