# Import
from typing import Set, Union
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

    def __init__(self, depth_threshold: int, number_of_variables_lower_bound: Union[int, None]):
        super().__init__()

        self.__depth_threshold: int = depth_threshold
        self.__number_of_variables_lower_bound: Union[int, None] = number_of_variables_lower_bound

    # region Override method
    def preselect_variables(self, variable_restriction_set: Union[Set[int], None], incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        variable_restriction_set = incidence_graph.variable_set(copy=False) if variable_restriction_set is None else variable_restriction_set

        # Near the root of the search tree => return all (restricted) variables
        if depth <= self.__depth_threshold:
            return variable_restriction_set

        literal_set = incidence_graph.get_literals_in_binary_clauses()

        # Get variables that occur both positive and negative in binary clauses
        # variable_set = set([abs(lit) for lit in literal_set if (-lit in literal_set) and (abs(lit) in variable_restriction_set)])
        variable_set = set(filter(lambda var: (var in literal_set) and (-var in literal_set), variable_restriction_set))

        # The lower bound is not set
        if self.__number_of_variables_lower_bound is None:
            if not len(variable_set):
                self._fill_variable_set(current_variable_set=variable_set,
                                        all_variable_set=variable_restriction_set,
                                        required_number_of_variables=1)

            return variable_set

        # The lower bound is set
        if len(variable_set) >= self.__number_of_variables_lower_bound:
            return variable_set

        self._fill_variable_set(current_variable_set=variable_set,
                                all_variable_set=variable_restriction_set,
                                required_number_of_variables=self.__number_of_variables_lower_bound)
        return variable_set
    # endregion
