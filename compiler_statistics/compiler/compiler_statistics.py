# Import
from datetime import timedelta
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

    def __init__(self, active: bool):
        super().__init__("Compiler")

        self.__create_circuit: StatisticsComponentTimer = StatisticsComponentTimer(name="create circuit",
                                                                                   active=active,
                                                                                   show_only_sum_time=True,
                                                                                   one_process=False)
        self._component_list.append(self.__create_circuit)

        self.__smooth: StatisticsComponentTimer = StatisticsComponentTimer(name="smooth",
                                                                           active=active,
                                                                           show_only_sum_time=True)
        self._component_list.append(self.__smooth)

    # region Public method
    def get_time(self) -> timedelta:
        """
        :return: the time of creating the circuit
        """

        return StatisticsComponentTimer.convert_to_datetime(self.__create_circuit.sum_time)
    # endregion

    # region Property
    @property
    def create_circuit(self) -> StatisticsComponentTimer:
        return self.__create_circuit

    @property
    def smooth(self) -> StatisticsComponentTimer:
        return self.__smooth
    # endregion
