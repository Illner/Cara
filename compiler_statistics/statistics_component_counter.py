# Import
from typing import Union


class StatisticsComponentCounter:
    """
    Statistics component (counter)
    """

    """
    Private str name
    Private bool show_only_number_of_calls
    
    Private int number_of_calls
    Private float sum_count
    Private float min_count
    Private float max_count
    """

    def __init__(self, name: str, show_only_number_of_calls: bool = False):
        self.__name: str = name
        self.__show_only_number_of_calls: bool = show_only_number_of_calls

        self.__number_of_calls: int = 0
        self.__sum_count: float = 0
        self.__min_count: Union[float, None] = None
        self.__max_count: Union[float, None] = None

    # region Public method
    def add_count(self, count: float) -> None:

        self.__number_of_calls += 1
        self.__sum_count += count

        # min_count
        if (self.__min_count is None) or (count < self.__min_count):
            self.__min_count = count

        # max_count
        if (self.__max_count is None) or (self.__max_count < count):
            self.__max_count = count
    # endregion

    # region Magic method
    def __str__(self):
        if self.__show_only_number_of_calls:
            string_temp = "\n".join((f"\tName: {self.name} (counter)",
                                     f"\t\tNumber: {self.number_of_calls}"))

        else:
            string_temp = "\n".join((f"\tName: {self.name} (counter)",
                                     f"\t\tNumber of calls: {self.number_of_calls}",
                                     f"\t\tAverage count: {self.average_count}",
                                     f"\t\tSum count: {self.sum_count}",
                                     f"\t\tMin count: {self.min_count}",
                                     f"\t\tMax count: {self.max_count}"))

        return string_temp
    # endregion

    # region Property
    @property
    def name(self):
        return self.__name

    @property
    def number_of_calls(self):
        return self.__number_of_calls

    @property
    def sum_count(self):
        return self.__sum_count

    @property
    def min_count(self):
        return self.__min_count

    @property
    def max_count(self):
        return self.__max_count

    @property
    def average_count(self):
        if self.__number_of_calls == 0:
            return None

        return self.__sum_count / self.__number_of_calls
    # endregion
