class HypergraphException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SomethingWrongException(HypergraphException):
    """
    Something wrong
    """

    def __init__(self, message_extension: str = ""):
        self.message = "Something wrong"
        if message_extension:
            self.message += f" ({message_extension})"
        super().__init__(self.message)


class FileIsMissingException(HypergraphException):
    """
    The file is missing
    """

    def __init__(self, file_path: str):
        self.message = f"The file ({file_path}) is missing!"
        super().__init__(self.message)


class SoftwareIsNotSupportedOnSystemException(HypergraphException):
    """
    The software is not supported on the system
    """

    def __init__(self, software_name: str):
        self.message = f"The software ({software_name}) is not supported on the system!"
        super().__init__(self.message)
