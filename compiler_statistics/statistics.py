# Import
from typing import List
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract

from compiler_statistics.formula.cnf_statistics import CnfStatistics
from compiler_statistics.compiler.solver_statistics import SolverStatistics
from compiler_statistics.compiler.hypergraph_partitioning_statistics import HypergraphPartitioningStatistics


class Statistics:
    """
    Statistics
    """

    """
    Private List<StatisticsTemplateAbstract> template_list
    
    Private CnfStatistics cnf_statistics
    Private SolverStatistics solver_statistics
    Private HypergraphPartitioningStatistics hypergraph_partitioning_statistics
    """

    def __init__(self):
        self.__template_list: List[StatisticsTemplateAbstract] = []

        # CNF
        self.__cnf_statistics: CnfStatistics = CnfStatistics()
        self.__template_list.append(self.__cnf_statistics)

        # Solver
        self.__solver_statistics: SolverStatistics = SolverStatistics()
        self.__template_list.append(self.__solver_statistics)

        # Hypergraph partitioning
        self.__hypergraph_partitioning_statistics: HypergraphPartitioningStatistics = HypergraphPartitioningStatistics()
        self.__template_list.append(self.__hypergraph_partitioning_statistics)

    # region Magic method
    def __str__(self):
        string_temp = ""

        for template in self.__template_list:
            string_temp = "\n".join((string_temp, str(template), ""))

        return string_temp
    # endregion

    # region Property
    @property
    def cnf_statistics(self):
        return self.__cnf_statistics

    @property
    def solver_statistics(self):
        return self.__solver_statistics

    @property
    def hypergraph_partitioning_statistics(self):
        return self.__hypergraph_partitioning_statistics
    # endregion
