# Import
from abc import ABC
from typing import List
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter


class StatisticsTemplateAbstract(ABC):
    """
    Statistics template
    """

    """
    Private str name
    Protected List<StatisticsComponent> component_list
    """

    def __init__(self, name: str):
        self.__name: str = name
        self._component_list: List[StatisticsComponentTimer, StatisticsComponentCounter] = []

    # region Magic function
    def __str__(self):
        string_temp = f"Name: {self.name}"

        for component in self._component_list:
            string_temp = "\n".join((string_temp, str(component)))

        return string_temp
    # endregion

    # region Property
    @property
    def name(self):
        return self.__name
    # endregion
