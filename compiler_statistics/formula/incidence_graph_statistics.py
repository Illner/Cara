# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter


class IncidenceGraphStatistics(StatisticsTemplateAbstract):
    """
    Incidence graph - statistics
    """

    """
    Private StatisticsComponentTimer create_incidence_graphs_for_components
    Private StatisticsComponentTimer get_connected_components
    Private StatisticsComponentTimer copy_incidence_graph
    Private StatisticsComponentTimer is_connected
    Private StatisticsComponentTimer number_of_components
    Private StatisticsComponentTimer subsumption_variable
    Private StatisticsComponentTimer renamable_horn_formula_recognition_initialization
    Private StatisticsComponentTimer renamable_horn_formula_recognition_check
    Private StatisticsComponentTimer renamable_horn_formula_recognition_implication_graph_check
    Private StatisticsComponentTimer convert_to_cnf
    Private StatisticsComponentTimer convert_to_2_cnf
    Private StatisticsComponentTimer convert_to_horn_cnf
    Private StatisticsComponentTimer get_redundant_clauses
    
    Private StatisticsComponentCounter renamable_horn_formula_ratio
    Private StatisticsComponentCounter two_cnf_ratio
    Private StatisticsComponentCounter get_redundant_clauses_size
    """

    def __init__(self, active: bool):
        super().__init__("Incidence graph")

        self.__create_incidence_graphs_for_components: StatisticsComponentTimer = StatisticsComponentTimer(name="create components", active=active)
        self._component_list.append(self.__create_incidence_graphs_for_components)

        self.__get_connected_components: StatisticsComponentTimer = StatisticsComponentTimer(name="get connected components", active=active)
        self._component_list.append(self.__get_connected_components)

        self.__copy_incidence_graph: StatisticsComponentTimer = StatisticsComponentTimer(name="copy", active=active)
        self._component_list.append(self.__copy_incidence_graph)

        self.__is_connected: StatisticsComponentTimer = StatisticsComponentTimer(name="is connected", active=active)
        self._component_list.append(self.__is_connected)

        self.__number_of_components: StatisticsComponentTimer = StatisticsComponentTimer(name="get number of components", active=active)
        self._component_list.append(self.__number_of_components)

        self.__subsumption_variable: StatisticsComponentTimer = StatisticsComponentTimer(name="subsumption - variable", active=active)
        self._component_list.append(self.__subsumption_variable)

        self.__renamable_horn_formula_recognition_initialization: StatisticsComponentTimer = StatisticsComponentTimer(name="renamable Horn formula recognition - initialization", active=active)
        self._component_list.append(self.__renamable_horn_formula_recognition_initialization)

        self.__renamable_horn_formula_recognition_check: StatisticsComponentTimer = StatisticsComponentTimer(name="renamable Horn formula recognition - check", active=active)
        self._component_list.append(self.__renamable_horn_formula_recognition_check)

        self.__renamable_horn_formula_recognition_implication_graph_check: StatisticsComponentTimer = StatisticsComponentTimer(name="renamable Horn formula recognition (implication graph) - check", active=active)
        self._component_list.append(self.__renamable_horn_formula_recognition_implication_graph_check)

        self.__renamable_horn_formula_ratio: StatisticsComponentCounter = StatisticsComponentCounter(name="renamable Horn formula - ratio", active=active)
        self._component_list.append(self.__renamable_horn_formula_ratio)

        self.__two_cnf_ratio: StatisticsComponentCounter = StatisticsComponentCounter(name="2-CNF - ratio", active=active)
        self._component_list.append(self.__two_cnf_ratio)

        self.__convert_to_cnf: StatisticsComponentTimer = StatisticsComponentTimer(name="convert - CNF", active=active)
        self._component_list.append(self.__convert_to_cnf)

        self.__convert_to_2_cnf: StatisticsComponentTimer = StatisticsComponentTimer(name="convert - 2-CNF", active=active)
        self._component_list.append(self.__convert_to_2_cnf)

        self.__convert_to_horn_cnf: StatisticsComponentTimer = StatisticsComponentTimer(name="convert - HornCNF", active=active)
        self._component_list.append(self.__convert_to_horn_cnf)

        self.__get_redundant_clauses: StatisticsComponentTimer = StatisticsComponentTimer(name="get redundant clauses", active=active)
        self._component_list.append(self.__get_redundant_clauses)

        self.__get_redundant_clauses_size: StatisticsComponentCounter = StatisticsComponentCounter(name="get redundant clauses - size", active=active)
        self._component_list.append(self.__get_redundant_clauses_size)

    # region Property
    @property
    def create_incidence_graphs_for_components(self) -> StatisticsComponentTimer:
        return self.__create_incidence_graphs_for_components

    @property
    def get_connected_components(self) -> StatisticsComponentTimer:
        return self.__get_connected_components

    @property
    def copy_incidence_graph(self) -> StatisticsComponentTimer:
        return self.__copy_incidence_graph

    @property
    def is_connected(self) -> StatisticsComponentTimer:
        return self.__is_connected

    @property
    def number_of_components(self) -> StatisticsComponentTimer:
        return self.__number_of_components

    @property
    def subsumption_variable(self) -> StatisticsComponentTimer:
        return self.__subsumption_variable

    @property
    def renamable_horn_formula_recognition_initialization(self) -> StatisticsComponentTimer:
        return self.__renamable_horn_formula_recognition_initialization

    @property
    def renamable_horn_formula_recognition_check(self) -> StatisticsComponentTimer:
        return self.__renamable_horn_formula_recognition_check

    @property
    def renamable_horn_formula_recognition_implication_graph_check(self) -> StatisticsComponentTimer:
        return self.__renamable_horn_formula_recognition_implication_graph_check

    @property
    def renamable_horn_formula_ratio(self) -> StatisticsComponentCounter:
        return self.__renamable_horn_formula_ratio

    @property
    def two_cnf_ratio(self) -> StatisticsComponentCounter:
        return self.__two_cnf_ratio

    @property
    def convert_to_cnf(self) -> StatisticsComponentTimer:
        return self.__convert_to_cnf

    @property
    def convert_to_2_cnf(self) -> StatisticsComponentTimer:
        return self.__convert_to_2_cnf

    @property
    def convert_to_horn_cnf(self) -> StatisticsComponentTimer:
        return self.__convert_to_horn_cnf

    @property
    def get_redundant_clauses(self) -> StatisticsComponentTimer:
        return self.__get_redundant_clauses

    @property
    def get_redundant_clauses_size(self) -> StatisticsComponentCounter:
        return self.__get_redundant_clauses_size
    # endregion
