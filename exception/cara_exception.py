class CaraException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SomethingWrongException(CaraException):
    """
    Something wrong
    """

    def __init__(self, message_extension: str = ""):
        self.message = "Something wrong"
        if message_extension:
            self.message += f" ({message_extension})"
        super().__init__(self.message)


class FunctionNotImplementedException(CaraException):
    """
    The function is not implemented
    """

    def __init__(self, function_name: str, message_extension: str = ""):
        self.message = f"The function ({function_name}) is not implemented!"
        if message_extension:
            self.message += f" ({message_extension})"
        super().__init__(self.message)


class InvalidConfigurationException(CaraException):
    """
    Invalid configuration
    """

    def __init__(self, message_extension: str):
        self.message = f"Invalid configuration ({message_extension})"
        super().__init__(self.message)
