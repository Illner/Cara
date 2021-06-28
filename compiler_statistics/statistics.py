# Import
from typing import List, Union, Dict
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract

from compiler_statistics.formula.cnf_statistics import CnfStatistics
from compiler_statistics.compiler.solver_statistics import SolverStatistics
from compiler_statistics.compiler.compiler_statistics import CompilerStatistics
from compiler_statistics.compiler.component_statistics import ComponentStatistics
from compiler_statistics.formula.incidence_graph_statistics import IncidenceGraphStatistics
from compiler_statistics.compiler.preselection_heuristic_statistics import PreselectionHeuristicStatistics
from compiler_statistics.compiler.hypergraph_partitioning_statistics import HypergraphPartitioningStatistics

# Import enum
import circuit.node.node_type_enum as nt_enum


class Statistics:
    """
    Statistics
    """

    """
    Private bool active
    Private List<StatisticsTemplateAbstract> template_list
    
    Private str name
    Private int size
    Private bool compiled
    Private int number_of_nodes
    Private int number_of_variables
    Private Dict<NodeTypeEnum, int> node_type_dictionary
    
    Private CnfStatistics cnf_statistics
    Private SolverStatistics solver_statistics
    Private CompilerStatistics compiler_statistics
    Private ComponentStatistics component_statistics
    Private IncidenceGraphStatistics incidence_graph_statistics
    Private HypergraphPartitioningStatistics hypergraph_partitioning_statistics
    Private PreselectionHeuristicStatistics preselection_heuristic_implied_literals_statistics
    Private PreselectionHeuristicStatistics preselection_heuristic_first_implied_literals_statistics
    """

    def __init__(self, active: bool,
                 cnf_statistics: Union[CnfStatistics, None] = None,
                 incidence_graph_statistics: Union[IncidenceGraphStatistics, None] = None):
        self.__active: bool = active
        self.__template_list: List[StatisticsTemplateAbstract] = []

        self.__name: str = ""
        self.__compiled: bool = False
        self.__size: Union[int, None] = None
        self.__number_of_nodes: Union[int, None] = None
        self.__number_of_variables: Union[int, None] = None
        self.__node_type_dictionary: Dict[nt_enum.NodeTypeEnum, int] = dict()

        # Compiler
        self.__compiler_statistics: CompilerStatistics = CompilerStatistics(active=True)
        self.__template_list.append(self.__compiler_statistics)

        # CNF
        if cnf_statistics is None:
            self.__cnf_statistics: CnfStatistics = CnfStatistics(active=active)
        else:
            self.__cnf_statistics: CnfStatistics = cnf_statistics
        self.__template_list.append(self.__cnf_statistics)

        # Incidence graph
        if incidence_graph_statistics is None:
            self.__incidence_graph_statistics: IncidenceGraphStatistics = IncidenceGraphStatistics(active=active)
        else:
            self.__incidence_graph_statistics: IncidenceGraphStatistics = incidence_graph_statistics
        self.__template_list.append(self.__incidence_graph_statistics)

        # Solver
        self.__solver_statistics: SolverStatistics = SolverStatistics(active=active)
        self.__template_list.append(self.__solver_statistics)

        # Hypergraph partitioning
        self.__hypergraph_partitioning_statistics: HypergraphPartitioningStatistics = HypergraphPartitioningStatistics(active=active)
        self.__template_list.append(self.__hypergraph_partitioning_statistics)

        # Component
        self.__component_statistics: ComponentStatistics = ComponentStatistics(active=active)
        self.__template_list.append(self.__component_statistics)

        # Preselection heuristic - implied literals
        self.__preselection_heuristic_implied_literals_statistics: PreselectionHeuristicStatistics = PreselectionHeuristicStatistics(name="implied literals", active=active)
        self.__template_list.append(self.__preselection_heuristic_implied_literals_statistics)

        # Preselection heuristic - first implied literals
        self.__preselection_heuristic_first_implied_literals_statistics: PreselectionHeuristicStatistics = PreselectionHeuristicStatistics(name="first implied literals", active=active)
        self.__template_list.append(self.__preselection_heuristic_first_implied_literals_statistics)

    # region Magic method
    def __str__(self):
        string_temp = "\n".join((f"Compiled: {self.__compiled}",
                                 f"Name: {self.__name}",
                                 f"Number of nodes: {self.__number_of_nodes}",
                                 f"Size: {self.__size}",
                                 f"Number of variables: {self.__number_of_variables}"))

        string_temp = "\n".join((string_temp, ""))

        # node_type_dictionary
        for node_type in self.__node_type_dictionary:
            value = self.__node_type_dictionary[node_type]
            string_temp = "\n".join((string_temp, f"{node_type.name}: {value}"))

        string_temp = "\n".join((string_temp, ""))

        for template in self.__template_list:
            string_temp = "\n".join((string_temp, str(template), ""))

        return string_temp
    # endregion

    # region Public method
    def set_compiled(self) -> None:
        self.__compiled = True

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_size(self, size: int) -> None:
        self.__size = size

    def set_number_of_nodes(self, number_of_nodes: int) -> None:
        self.__number_of_nodes = number_of_nodes

    def set_number_of_variables(self, number_of_variables: int) -> None:
        self.__number_of_variables = number_of_variables

    def set_node_type_dictionary(self, node_type_dictionary: Dict[nt_enum.NodeTypeEnum, int]) -> None:
        self.__node_type_dictionary = node_type_dictionary

    def get_node_type_counter(self, node_type: nt_enum.NodeTypeEnum) -> int:
        return self.__node_type_dictionary[node_type]
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

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def size(self) -> int:
        return self.__size

    @property
    def compiled(self) -> bool:
        return self.__compiled
    # endregion
