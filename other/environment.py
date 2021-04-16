# Import
import platform

# Import enum
import other.os_enum as os_enum


# region system/OS
def get_os() -> os_enum.OsEnum:
    """
    :return: the system/OS
    """

    os = platform.system()
    result = os_enum.OsEnum.UNDEFINED

    if os == "Windows":
        result = os_enum.OsEnum.WINDOWS
    elif os == "Linux":
        result = os_enum.OsEnum.LINUX
    elif os == "Darwin":
        result = os_enum.OsEnum.MAC_OS

    return result


def is_windows() -> bool:
    """
    :return: True if the system/OS is Windows. Otherwise, False is returned.
    """

    os = get_os()
    if os == os_enum.OsEnum.WINDOWS:
        return True

    return False


def is_linux() -> bool:
    """
    :return: True if the system/OS is Linux. Otherwise, False is returned.
    """

    os = get_os()
    if os == os_enum.OsEnum.LINUX:
        return True

    return False


def is_mac_os() -> bool:
    """
    :return: True if the system/OS is MacOS. Otherwise, False is returned.
    """

    os = get_os()
    if os == os_enum.OsEnum.MAC_OS:
        return True

    return False
# endregion


def is_64bit() -> bool:
    """
    :return: True if the system/OS is 64 bit. Otherwise, False is returned.
    """

    return platform.architecture()[0] == "64bit"
