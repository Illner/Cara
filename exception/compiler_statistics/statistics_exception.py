# Import exception
from exception.cara_exception import CaraException


class StatisticsException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class StopwatchHasNotBeenStartedException(StatisticsException):
    """
    The stopwatch has not been started
    """

    def __init__(self, name: str):
        self.message = f"The stopwatch ({name}) has not been started!"
        super().__init__(self.message)


class StopwatchIsAlreadyRunningException(StatisticsException):
    """
    The stopwatch is already running
    """

    def __init__(self, name: str):
        self.message = f"The stopwatch ({name}) is already running!"
        super().__init__(self.message)
