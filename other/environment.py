# Import
import platform

# Import enum
import other.os_enum as os_enum


# region system/OS
def get_os() -> os_enum.OsEnum:
    """
    Return the system/OS
    """

    os = platform.system()
    result = os_enum.OsEnum.UNDEFINED

    if os == "Windows":
        result = os_enum.OsEnum.WINDOWS
    elif os == "Linux":
        result = os_enum.OsEnum.LINUX
    elif os == "Darwin":
        result = os_enum.OsEnum.MAC

    return result


def is_windows() -> bool:
    """
    Return True if the system/OS is Windows, otherwise False is returned
    """

    os = get_os()
    if os == os_enum.OsEnum.WINDOWS:
        return True

    return False


def is_linux() -> bool:
    """
    Return True if the system/OS is Linux, otherwise False is returned
    """

    os = get_os()
    if os == os_enum.OsEnum.LINUX:
        return True

    return False


def is_mac() -> bool:
    """
    Return True if the system/OS is MacOS, otherwise False is returned
    """

    os = get_os()
    if os == os_enum.OsEnum.MAC:
        return True

    return False
# endregion


def is_64bit() -> bool:
    """
    Return True if the system/OS is 64 bit, otherwise False is returned
    """

    return platform.architecture()[0] == "64bit"
