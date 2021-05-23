# Import
import time as sys_time
from typing import Union
from datetime import timedelta

# Import exception
import exception.compiler_statistics.statistics_exception as s_exception


class StatisticsComponentTimer:
    """
    Statistics component (timer)
    """

    """
    Private str name
    Private bool active
    Private bool show_only_sum_time

    Private int number_of_calls
    Private float sum_time              # nanoseconds
    Private float min_time              # nanoseconds
    Private float max_time              # nanoseconds
    
    Private float stopwatch_time        # nanoseconds
    """

    def __init__(self, name: str, active: bool = True, show_only_sum_time: bool = False):
        self.__name: str = name
        self.__active: bool = active
        self.__show_only_sum_time: bool = show_only_sum_time

        self.__number_of_calls: int = 0
        self.__sum_time: float = 0
        self.__min_time: Union[float, None] = None
        self.__max_time: Union[float, None] = None

        self.__stopwatch_time: Union[float, None] = None

    # region Public method
    def add_call(self, time: Union[float, None]) -> None:
        """
        It is assumed that the time is in nanoseconds!
        None is considered as 0.
        """

        if time is None:
            time = 0

        self.__number_of_calls += 1
        self.__sum_time += time

        # min_time
        if (self.__min_time is None) or (time < self.__min_time):
            self.__min_time = time

        # max_time
        if (self.__max_time is None) or (self.__max_time < time):
            self.__max_time = time

    def reset_stopwatch(self) -> None:
        """
        Reset the stopwatch
        :return: None
        """

        self.__stopwatch_time = None

    def start_stopwatch(self) -> None:
        """
        Start the stopwatch
        :return: None
        :raises StopwatchIsAlreadyRunningException: if the stopwatch is already running
        """

        # The statistic is not active
        if not self.__active:
            return

        # The stopwatch is already running
        if self.__stopwatch_time is not None:
            raise s_exception.StopwatchIsAlreadyRunningException(self.name)

        self.__stopwatch_time = sys_time.process_time_ns()

    def stop_stopwatch(self) -> None:
        """
        Stop the stopwatch and call add_call
        :return: None
        :raises StopwatchHasNotBeenStartedException: if the stopwatch has not been started
        """

        # The statistic is not active
        if not self.__active:
            return

        # The stopwatch has not been started
        if self.__stopwatch_time is None:
            raise s_exception.StopwatchHasNotBeenStartedException(self.name)

        time = sys_time.process_time_ns() - self.__stopwatch_time
        self.add_call(time)

        # Reset
        self.__stopwatch_time = None
    # endregion

    # region Static method
    @staticmethod
    def convert_to_datetime(time: Union[float, None]) -> Union[timedelta, None]:
        """
        It is assumed that the time is in nanoseconds!
        """

        if time is None:
            return None

        return timedelta(microseconds=time * 0.001)
    # endregion

    # region Magic function
    def __str__(self):
        if self.__show_only_sum_time:
            string_temp = "\n".join((f"\tName: {self.name} (timer)",
                                     f"\t\tTime: {self.convert_to_datetime(self.sum_time)}"))

        else:
            string_temp = "\n".join((f"\tName: {self.name} (timer)",
                                     f"\t\tNumber of calls: {self.number_of_calls}",
                                     f"\t\tAverage time: {self.convert_to_datetime(self.average_time)}",
                                     f"\t\tSum time: {self.convert_to_datetime(self.sum_time)}",
                                     f"\t\tMin time: {self.convert_to_datetime(self.min_time)}",
                                     f"\t\tMax time: {self.convert_to_datetime(self.max_time)}"))

        return string_temp
    # endregion

    # region Property
    @property
    def name(self) -> str:
        return self.__name

    @property
    def number_of_calls(self) -> int:
        return self.__number_of_calls

    @property
    def sum_time(self) -> float:
        return self.__sum_time

    @property
    def min_time(self) -> Union[float, None]:
        return self.__min_time

    @property
    def max_time(self) -> Union[float, None]:
        return self.__max_time

    @property
    def average_time(self) -> Union[float, None]:
        if self.__number_of_calls == 0:
            return None

        return self.__sum_time / self.__number_of_calls

    @property
    def active(self) -> bool:
        return self.__active
    # endregion
