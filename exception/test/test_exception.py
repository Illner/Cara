# Import exception
from exception.cara_exception import CaraException


class TestException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class OriginalResultDoesNotExistException(TestException):
    """
    The file with the original result does not exist
    """

    def __init__(self, test_name: str, file_path: str):
        self.message = f"The file ({file_path}) with the original result is missing. Test: {test_name}!"
        super().__init__(self.message)
