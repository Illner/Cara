# Import
from typing import Set, Union
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract
from compiler_statistics.compiler.preselection_heuristic_statistics import PreselectionHeuristicStatistics


class PropZHeuristic(PreselectionHeuristicAbstract):
    """
    Prop_z - preselection heuristic
    """

    """
    Private int depth_threshold
    Private int number_of_variables_lower_bound
    """

    def __init__(self, depth_threshold: int, number_of_variables_lower_bound: Union[int, None],
                 statistics: Union[PreselectionHeuristicStatistics, None] = None):
        super().__init__(statistics)

        self.__depth_threshold: int = depth_threshold
        self.__number_of_variables_lower_bound: Union[int, None] = number_of_variables_lower_bound

    # region Override method
    def preselect_variables(self, variable_restriction_set: Union[Set[int], None], incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        self._statistics.get_preselected_variables.start_stopwatch()    # timer (start)

        variable_restriction_set = incidence_graph._variable_set if variable_restriction_set is None else variable_restriction_set

        # Near the root of the search tree => return all (restricted) variables
        if depth <= self.__depth_threshold:
            self._update_statistics(preselected_variable_set=variable_restriction_set,
                                    variable_restriction_set=variable_restriction_set)

            self._statistics.get_preselected_variables.stop_stopwatch()     # timer (stop)
            return variable_restriction_set

        literal_set = incidence_graph.get_literals_in_binary_clauses()

        # Get variables that occur both positive and negative in binary clauses
        variable_set = set(filter(lambda var: (var in literal_set) and (-var in literal_set), variable_restriction_set))
        self._statistics.prop_z_number_of_variables_occur_both_positive_and_negative_in_binary_clauses.add_count(len(variable_set))    # counter

        # The lower bound is not set
        if self.__number_of_variables_lower_bound is None:
            if not len(variable_set):
                PreselectionHeuristicAbstract._fill_variable_set(current_variable_set=variable_set,
                                                                 all_variable_set=variable_restriction_set,
                                                                 required_number_of_variables=1)

        # The lower bound is set
        else:
            if len(variable_set) < self.__number_of_variables_lower_bound:
                PreselectionHeuristicAbstract._fill_variable_set(current_variable_set=variable_set,
                                                                 all_variable_set=variable_restriction_set,
                                                                 required_number_of_variables=self.__number_of_variables_lower_bound)

        self._update_statistics(preselected_variable_set=variable_set,
                                variable_restriction_set=variable_restriction_set)

        self._statistics.get_preselected_variables.stop_stopwatch()     # timer (stop)
        return variable_set
    # endregion
