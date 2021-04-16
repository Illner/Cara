# Import
from enum import IntEnum, unique


@unique
class OsEnum(IntEnum):
    WINDOWS = 1
    LINUX = 2
    MAC_OS = 3
    UNDEFINED = 4


os_enum_names = [os.name for os in OsEnum]
os_enum_values = [os.value for os in OsEnum]
