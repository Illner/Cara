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
