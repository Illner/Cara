# Import
from typing import Union


class BackbonesException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidChunkSizeException(BackbonesException):
    """
    Invalid chunk size
    """

    def __init__(self, chunk_size: Union[int, float]):
        self.message = f"The chunk size ({chunk_size}) is invalid!"
        super().__init__(self.message)
