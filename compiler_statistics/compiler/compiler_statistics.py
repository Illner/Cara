# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract


class CompilerStatistics(StatisticsTemplateAbstract):
    """
    Compiler - statistics
    """

    """
    Private StatisticsComponentTimer create_circuit
    Private StatisticsComponentTimer smooth
    """

    def __init__(self):
        super().__init__("Compiler")

        self.__create_circuit: StatisticsComponentTimer = StatisticsComponentTimer("create circuit")
        self._component_list.append(self.__create_circuit)

        self.__smooth: StatisticsComponentTimer = StatisticsComponentTimer("smooth")
        self._component_list.append(self.__smooth)

    # region Property
    @property
    def create_circuit(self):
        return self.__create_circuit

    @property
    def smooth(self):
        return self.__smooth
    # endregion
