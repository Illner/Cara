# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter


class IncidenceGraphStatistics(StatisticsTemplateAbstract):
    """
    Incidence graph - statistics
    """

    """
    Private StatisticsComponentTimer remove_literal
    Private StatisticsComponentTimer restore_backup_literal
    Private StatisticsComponentTimer merge_variable_simplification
    Private StatisticsComponentTimer restore_backup_variable_simplification
    Private StatisticsComponentTimer remove_subsumed_clause_variable
    Private StatisticsComponentTimer restore_backup_subsumption_variable
    Private StatisticsComponentTimer create_incidence_graphs_for_components
    Private StatisticsComponentTimer copy_incidence_graph
    Private StatisticsComponentTimer get_clause
    Private StatisticsComponentTimer clause_id_set
    Private StatisticsComponentTimer is_connected
    Private StatisticsComponentTimer number_of_components
    Private StatisticsComponentTimer variable_set
    Private StatisticsComponentTimer subsumption_variable
    Private StatisticsComponentTimer renamable_horn_formula_recognition_initialization
    Private StatisticsComponentTimer renamable_horn_formula_recognition_check
    Private StatisticsComponentTimer convert_to_cnf
    Private StatisticsComponentTimer convert_to_2_cnf
    Private StatisticsComponentTimer convert_to_horn_cnf
    Private StatisticsComponentTimer get_redundant_clauses
    
    Private StatisticsComponentCounter renamable_horn_formula_ratio
    Private StatisticsComponentCounter two_cnf_ratio
    Private StatisticsComponentCounter get_redundant_clauses_size
    """

    def __init__(self):
        super().__init__("Incidence graph")

        self.__remove_literal: StatisticsComponentTimer = StatisticsComponentTimer("remove literal")
        self._component_list.append(self.__remove_literal)

        self.__restore_backup_literal: StatisticsComponentTimer = StatisticsComponentTimer("restore backup - literal")
        self._component_list.append(self.__restore_backup_literal)

        self.__merge_variable_simplification: StatisticsComponentTimer = StatisticsComponentTimer("merge variable simplification")
        self._component_list.append(self.__merge_variable_simplification)

        self.__restore_backup_variable_simplification: StatisticsComponentTimer = StatisticsComponentTimer("restore backup - variable simplification")
        self._component_list.append(self.__restore_backup_variable_simplification)

        self.__remove_subsumed_clause_variable: StatisticsComponentTimer = StatisticsComponentTimer("remove subsumed clause - variable")
        self._component_list.append(self.__remove_subsumed_clause_variable)

        self.__restore_backup_subsumption_variable: StatisticsComponentTimer = StatisticsComponentTimer("restore backup - subsumption - variable")
        self._component_list.append(self.__restore_backup_subsumption_variable)

        self.__create_incidence_graphs_for_components: StatisticsComponentTimer = StatisticsComponentTimer("create components")
        self._component_list.append(self.__create_incidence_graphs_for_components)

        self.__copy_incidence_graph: StatisticsComponentTimer = StatisticsComponentTimer("copy")
        self._component_list.append(self.__copy_incidence_graph)

        self.__is_connected: StatisticsComponentTimer = StatisticsComponentTimer("is connected")
        self._component_list.append(self.__is_connected)

        self.__number_of_components: StatisticsComponentTimer = StatisticsComponentTimer("get number of components")
        self._component_list.append(self.__number_of_components)

        self.__get_clause: StatisticsComponentTimer = StatisticsComponentTimer("get clause")
        self._component_list.append(self.__get_clause)

        self.__clause_id_set: StatisticsComponentTimer = StatisticsComponentTimer("get clauses")
        self._component_list.append(self.__clause_id_set)

        self.__variable_set: StatisticsComponentTimer = StatisticsComponentTimer("get variables")
        self._component_list.append(self.__variable_set)

        self.__subsumption_variable: StatisticsComponentTimer = StatisticsComponentTimer("subsumption - variable")
        self._component_list.append(self.__subsumption_variable)

        self.__renamable_horn_formula_recognition_initialization: StatisticsComponentTimer = StatisticsComponentTimer("renamable Horn formula recognition - initialization")
        self._component_list.append(self.__renamable_horn_formula_recognition_initialization)

        self.__renamable_horn_formula_recognition_check: StatisticsComponentTimer = StatisticsComponentTimer("renamable Horn formula recognition - check")
        self._component_list.append(self.__renamable_horn_formula_recognition_check)

        self.__renamable_horn_formula_ratio: StatisticsComponentCounter = StatisticsComponentCounter("renamable Horn formula - ratio")
        self._component_list.append(self.__renamable_horn_formula_ratio)

        self.__two_cnf_ratio: StatisticsComponentCounter = StatisticsComponentCounter("2-CNF - ratio")
        self._component_list.append(self.__two_cnf_ratio)

        self.__convert_to_cnf: StatisticsComponentTimer = StatisticsComponentTimer("convert - CNF")
        self._component_list.append(self.__convert_to_cnf)

        self.__convert_to_2_cnf: StatisticsComponentTimer = StatisticsComponentTimer("convert - 2-CNF")
        self._component_list.append(self.__convert_to_2_cnf)

        self.__convert_to_horn_cnf: StatisticsComponentTimer = StatisticsComponentTimer("convert - HornCNF")
        self._component_list.append(self.__convert_to_horn_cnf)

        self.__get_redundant_clauses: StatisticsComponentTimer = StatisticsComponentTimer("get redundant clauses")
        self._component_list.append(self.__get_redundant_clauses)

        self.__get_redundant_clauses_size: StatisticsComponentCounter = StatisticsComponentCounter("get redundant clauses - size")
        self._component_list.append(self.__get_redundant_clauses_size)

    # region Property
    @property
    def remove_literal(self) -> StatisticsComponentTimer:
        return self.__remove_literal

    @property
    def restore_backup_literal(self) -> StatisticsComponentTimer:
        return self.__restore_backup_literal

    @property
    def merge_variable_simplification(self) -> StatisticsComponentTimer:
        return self.__merge_variable_simplification

    @property
    def restore_backup_variable_simplification(self) -> StatisticsComponentTimer:
        return self.__restore_backup_variable_simplification

    @property
    def remove_subsumed_clause_variable(self) -> StatisticsComponentTimer:
        return self.__remove_subsumed_clause_variable

    @property
    def restore_backup_subsumption_variable(self) -> StatisticsComponentTimer:
        return self.__restore_backup_subsumption_variable

    @property
    def create_incidence_graphs_for_components(self) -> StatisticsComponentTimer:
        return self.__create_incidence_graphs_for_components

    @property
    def copy_incidence_graph(self) -> StatisticsComponentTimer:
        return self.__copy_incidence_graph

    @property
    def get_clause(self) -> StatisticsComponentTimer:
        return self.__get_clause

    @property
    def clause_id_set(self) -> StatisticsComponentTimer:
        return self.__clause_id_set

    @property
    def is_connected(self) -> StatisticsComponentTimer:
        return self.__is_connected

    @property
    def number_of_components(self) -> StatisticsComponentTimer:
        return self.__number_of_components

    @property
    def variable_set(self) -> StatisticsComponentTimer:
        return self.__variable_set

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
