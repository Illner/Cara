# Import
from typing import Set
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class PropZHeuristic(PreselectionHeuristicAbstract):
    """
    Prop_z - preselection heuristic
    """

    """
    Private int depth_threshold
    Private int number_of_variables_lower_bound
    """

    def __init__(self, depth_threshold: int, number_of_variables_lower_bound: int):
        super().__init__()

        self.__depth_threshold: int = depth_threshold
        self.__number_of_variables_lower_bound: int = number_of_variables_lower_bound

    # region Override method
    def preselect_variables(self, incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        # Near the root of the search tree => return all variables
        if depth <= self.__depth_threshold:
            return incidence_graph.variable_set(copy=False)

        literal_set = incidence_graph.get_literals_in_binary_clauses()

        # Get variables that occur both positive and negative in binary clauses
        variable_set = set([abs(lit) for lit in literal_set if -lit in literal_set])

        if len(variable_set) >= self.__number_of_variables_lower_bound:
            return variable_set

        self._fill_variable_set(incidence_graph, variable_set, self.__number_of_variables_lower_bound)
        return variable_set
    # endregion
