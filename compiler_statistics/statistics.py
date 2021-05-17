# Import
from typing import List, Union
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract

from compiler_statistics.formula.cnf_statistics import CnfStatistics
from compiler_statistics.compiler.solver_statistics import SolverStatistics
from compiler_statistics.compiler.compiler_statistics import CompilerStatistics
from compiler_statistics.compiler.component_statistics import ComponentStatistics
from compiler_statistics.formula.incidence_graph_statistics import IncidenceGraphStatistics
from compiler_statistics.compiler.preselection_heuristic_statistics import PreselectionHeuristicStatistics
from compiler_statistics.compiler.hypergraph_partitioning_statistics import HypergraphPartitioningStatistics


class Statistics:
    """
    Statistics
    """

    """
    Private List<StatisticsTemplateAbstract> template_list
    
    Private CnfStatistics cnf_statistics
    Private SolverStatistics solver_statistics
    Private CompilerStatistics compiler_statistics
    Private ComponentStatistics component_statistics
    Private IncidenceGraphStatistics incidence_graph_statistics
    Private HypergraphPartitioningStatistics hypergraph_partitioning_statistics
    Private PreselectionHeuristicStatistics preselection_heuristic_implied_literals_statistics
    Private PreselectionHeuristicStatistics preselection_heuristic_first_implied_literals_statistics
    """

    def __init__(self, cnf_statistics: Union[CnfStatistics, None] = None,
                 incidence_graph_statistics: Union[IncidenceGraphStatistics, None] = None):
        self.__template_list: List[StatisticsTemplateAbstract] = []

        # Compiler
        self.__compiler_statistics: CompilerStatistics = CompilerStatistics()
        self.__template_list.append(self.__compiler_statistics)

        # CNF
        if cnf_statistics is None:
            self.__cnf_statistics: CnfStatistics = CnfStatistics()
        else:
            self.__cnf_statistics: CnfStatistics = cnf_statistics
        self.__template_list.append(self.__cnf_statistics)

        # Incidence graph
        if incidence_graph_statistics is None:
            self.__incidence_graph_statistics: IncidenceGraphStatistics = IncidenceGraphStatistics()
        else:
            self.__incidence_graph_statistics: IncidenceGraphStatistics = incidence_graph_statistics
        self.__template_list.append(self.__incidence_graph_statistics)

        # Solver
        self.__solver_statistics: SolverStatistics = SolverStatistics()
        self.__template_list.append(self.__solver_statistics)

        # Hypergraph partitioning
        self.__hypergraph_partitioning_statistics: HypergraphPartitioningStatistics = HypergraphPartitioningStatistics()
        self.__template_list.append(self.__hypergraph_partitioning_statistics)

        # Component
        self.__component_statistics: ComponentStatistics = ComponentStatistics()
        self.__template_list.append(self.__component_statistics)

        # Preselection heuristic - implied literals
        self.__preselection_heuristic_implied_literals_statistics: PreselectionHeuristicStatistics = PreselectionHeuristicStatistics(name="implied literals")
        self.__template_list.append(self.__preselection_heuristic_implied_literals_statistics)

        # Preselection heuristic - first implied literals
        self.__preselection_heuristic_first_implied_literals_statistics: PreselectionHeuristicStatistics = PreselectionHeuristicStatistics(name="first implied literals")
        self.__template_list.append(self.__preselection_heuristic_first_implied_literals_statistics)

    # region Magic method
    def __str__(self):
        string_temp = ""

        for template in self.__template_list:
            string_temp = "\n".join((string_temp, str(template), ""))

        return string_temp
    # endregion

    # region Property
    @property
    def compiler_statistics(self) -> CompilerStatistics:
        return self.__compiler_statistics

    @property
    def cnf_statistics(self) -> CnfStatistics:
        return self.__cnf_statistics

    @property
    def incidence_graph_statistics(self) -> IncidenceGraphStatistics:
        return self.__incidence_graph_statistics

    @property
    def solver_statistics(self) -> SolverStatistics:
        return self.__solver_statistics

    @property
    def hypergraph_partitioning_statistics(self) -> HypergraphPartitioningStatistics:
        return self.__hypergraph_partitioning_statistics

    @property
    def component_statistics(self) -> ComponentStatistics:
        return self.__component_statistics

    @property
    def preselection_heuristic_implied_literals_statistics(self) -> PreselectionHeuristicStatistics:
        return self.__preselection_heuristic_implied_literals_statistics

    @property
    def preselection_heuristic_first_implied_literals_statistics(self) -> PreselectionHeuristicStatistics:
        return self.__preselection_heuristic_first_implied_literals_statistics
    # endregion
