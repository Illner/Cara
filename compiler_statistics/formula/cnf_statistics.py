# Import
from datetime import timedelta
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract


class CnfStatistics(StatisticsTemplateAbstract):
    """
    CNF - statistics
    """

    """
    Private StatisticsComponentTimer create
    """

    def __init__(self):
        super().__init__("CNF")

        self.__create: StatisticsComponentTimer = StatisticsComponentTimer("create", True)
        self._component_list.append(self.__create)

    # region Public method
    def get_time(self) -> timedelta:
        """
        :return: the time of creating the CNF
        """

        return StatisticsComponentTimer.convert_to_datetime(self.__create.sum_time)
    # endregion

    # region Property
    @property
    def create(self) -> StatisticsComponentTimer:
        return self.__create
    # endregion
