# Import
from typing import List

# Import exception
from exception.cara_exception import CaraException


class HeuristicException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class ClauseIsNotBinaryException(HeuristicException):
    """
    The clause is not binary
    """

    def __init__(self, clause: List[int]):
        self.message = f"The clause ({clause}) is not binary!"
        super().__init__(self.message)


class PreselectedVariableSetIsEmptyException(HeuristicException):
    """
    The preselected variable set is empty
    """

    def __init__(self):
        self.message = "The preselected variable set is empty!"
        super().__init__(self.message)
