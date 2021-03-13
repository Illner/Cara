# Import
from typing import List
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract

import compiler_statistics.compiler.solver_statistics as s_statistics


class Statistics:
    """
    Statistics
    """

    """
    Private List<StatisticsTemplateAbstract> template_list
    
    Private SolverStatistics solver_statistics
    """

    def __init__(self):
        self.__template_list: List[StatisticsTemplateAbstract] = []

        # Solver
        self.__solver_statistics = s_statistics.SolverStatistics("Solver")
        self.__template_list.append(self.__solver_statistics)

    # region Magic method
    def __str__(self):
        string_temp = ""

        for template in self.__template_list:
            string_temp = "\n".join((string_temp, str(template), ""))

        return string_temp
    # endregion

    # region Property
    @property
    def solver_statistics(self):
        return self.__solver_statistics
    # endregion
