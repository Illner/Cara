# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract


class IncidenceGraphStatistics(StatisticsTemplateAbstract):
    """
    Incidence graph - statistics
    """

    """
    Private StatisticsComponentTimer remove_literal
    Private StatisticsComponentTimer restore_backup_literal
    Private StatisticsComponentTimer merge_variable_simplification
    Private StatisticsComponentTimer restore_backup_variable_simplification
    Private StatisticsComponentTimer remove_subsumed_clause
    Private StatisticsComponentTimer restore_backup_subsumption
    Private StatisticsComponentTimer create_incidence_graphs_for_components
    Private StatisticsComponentTimer copy_incidence_graph
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

        self.__remove_subsumed_clause: StatisticsComponentTimer = StatisticsComponentTimer("remove subsumed clause")
        self._component_list.append(self.__remove_subsumed_clause)

        self.__restore_backup_subsumption: StatisticsComponentTimer = StatisticsComponentTimer("restore backup - subsumption")
        self._component_list.append(self.__restore_backup_subsumption)

        self.__create_incidence_graphs_for_components: StatisticsComponentTimer = StatisticsComponentTimer("create components")
        self._component_list.append(self.__create_incidence_graphs_for_components)

        self.__copy_incidence_graph: StatisticsComponentTimer = StatisticsComponentTimer("copy")
        self._component_list.append(self.__copy_incidence_graph)

    # region Property
    @property
    def remove_literal(self):
        return self.__remove_literal

    @property
    def restore_backup_literal(self):
        return self.__restore_backup_literal

    @property
    def merge_variable_simplification(self):
        return self.__merge_variable_simplification

    @property
    def restore_backup_variable_simplification(self):
        return self.__restore_backup_variable_simplification

    @property
    def remove_subsumed_clause(self):
        return self.__remove_subsumed_clause

    @property
    def restore_backup_subsumption(self):
        return self.__restore_backup_subsumption

    @property
    def create_incidence_graphs_for_components(self):
        return self.__create_incidence_graphs_for_components

    @property
    def copy_incidence_graph(self):
        return self.__copy_incidence_graph
    # endregion
