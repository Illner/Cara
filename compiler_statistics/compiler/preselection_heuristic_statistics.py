# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract


class PreselectionHeuristicStatistics(StatisticsTemplateAbstract):
    """
    Preselection heuristic - statistics
    """

    """
    Private StatisticsComponentTimer get_preselected_variables
    Private StatisticsComponentCounter all_variables_preselected
    Private StatisticsComponentCounter ratio_of_preselected_variables
    Private StatisticsComponentCounter number_of_preselected_variables
    Private StatisticsComponentCounter prop_z_number_of_variables_occur_both_positive_and_negative_in_binary_clauses
    """

    def __init__(self, name: str = ""):
        if name == "":
            temp = "Preselection heuristic"
        else:
            temp = f"Preselection heuristic - {name}"

        super().__init__(temp)

        self.__get_preselected_variables: StatisticsComponentTimer = StatisticsComponentTimer("get preselected variables")
        self._component_list.append(self.__get_preselected_variables)

        self.__all_variables_preselected: StatisticsComponentCounter = StatisticsComponentCounter("all variables preselected")
        self._component_list.append(self.__all_variables_preselected)

        self.__ratio_of_preselected_variables: StatisticsComponentCounter = StatisticsComponentCounter("ratio of preselected variables")
        self._component_list.append(self.__ratio_of_preselected_variables)

        self.__number_of_preselected_variables: StatisticsComponentCounter = StatisticsComponentCounter("number of preselected variables")
        self._component_list.append(self.__number_of_preselected_variables)

        self.__prop_z_number_of_variables_occur_both_positive_and_negative_in_binary_clauses: StatisticsComponentCounter = \
            StatisticsComponentCounter("prop_z - number of variables that occur both positive and negative in binary clauses")
        self._component_list.append(self.__prop_z_number_of_variables_occur_both_positive_and_negative_in_binary_clauses)

    # region Property
    @property
    def get_preselected_variables(self) -> StatisticsComponentTimer:
        return self.__get_preselected_variables

    @property
    def all_variables_preselected(self) -> StatisticsComponentCounter:
        return self.__all_variables_preselected

    @property
    def ratio_of_preselected_variables(self) -> StatisticsComponentCounter:
        return self.__ratio_of_preselected_variables

    @property
    def number_of_preselected_variables(self) -> StatisticsComponentCounter:
        return self.__number_of_preselected_variables

    @property
    def prop_z_number_of_variables_occur_both_positive_and_negative_in_binary_clauses(self) -> StatisticsComponentCounter:
        return self.__prop_z_number_of_variables_occur_both_positive_and_negative_in_binary_clauses
    # endregion
