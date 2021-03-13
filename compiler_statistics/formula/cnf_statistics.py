# Import
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

        self.__create: StatisticsComponentTimer = StatisticsComponentTimer("create")
        self._component_list.append(self.__create)

    # region Property
    @property
    def create(self):
        return self.__create
    # endregion
