# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter


class RenamableHornFormulaLpFormulationStatistics(StatisticsTemplateAbstract):
    """
    Renamable Horn formula - LP formulation - statistics
    """

    """
    Private StatisticsComponentTimer create_lp_formulation
    Private StatisticsComponentTimer solve_lp_problem

    Private StatisticsComponentCounter switching_average
    Private StatisticsComponentCounter horn_clauses_after_switching_average
    Private StatisticsComponentCounter horn_clauses_after_switching_length
    """

    def __init__(self, active: bool):
        super().__init__("Renamable Horn formula - LP formulation")

        self.__create_lp_formulation: StatisticsComponentTimer = StatisticsComponentTimer(name="create LP formulation", active=active)
        self._component_list.append(self.__create_lp_formulation)

        self.__solve_lp_problem: StatisticsComponentTimer = StatisticsComponentTimer(name="solve LP problem", active=active)
        self._component_list.append(self.__solve_lp_problem)

        self.__switching_average: StatisticsComponentCounter = StatisticsComponentCounter(name="switching - average (1/|V| * sum_i s_i)", active=active)
        self._component_list.append(self.__switching_average)

        self.__horn_clauses_after_switching_average: StatisticsComponentCounter = StatisticsComponentCounter(name="Horn clauses after switching - average (1/|C| * sum_i z_i)", active=active)
        self._component_list.append(self.__horn_clauses_after_switching_average)

        self.__horn_clauses_after_switching_length: StatisticsComponentCounter = StatisticsComponentCounter(name="Horn clauses after switching - length (1/|C| * sum_i z_i * |C_i|)", active=active)
        self._component_list.append(self.__horn_clauses_after_switching_length)

    # region Property
    @property
    def create_lp_formulation(self) -> StatisticsComponentTimer:
        return self.__create_lp_formulation

    @property
    def solve_lp_problem(self) -> StatisticsComponentTimer:
        return self.__solve_lp_problem

    @property
    def switching_average(self) -> StatisticsComponentCounter:
        return self.__switching_average

    @property
    def horn_clauses_after_switching_average(self) -> StatisticsComponentCounter:
        return self.__horn_clauses_after_switching_average

    @property
    def horn_clauses_after_switching_length(self) -> StatisticsComponentCounter:
        return self.__horn_clauses_after_switching_length
    # endregion
