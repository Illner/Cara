# Import
import random
from typing import Set, Union
from abc import ABC, abstractmethod
from formula.incidence_graph import IncidenceGraph
from compiler_statistics.compiler.preselection_heuristic_statistics import PreselectionHeuristicStatistics


class PreselectionHeuristicAbstract(ABC):
    """
    Preselection heuristic
    """

    """
    Protected PreselectionHeuristicStatistics statistics
    """

    def __init__(self, statistics: Union[PreselectionHeuristicStatistics, None] = None):
        # Statistics
        if statistics is None:
            self._statistics: PreselectionHeuristicStatistics = PreselectionHeuristicStatistics(active=False)
        else:
            self._statistics: PreselectionHeuristicStatistics = statistics

    # region Abstract method
    @abstractmethod
    def preselect_variables(self, variable_restriction_set: Union[Set[int], None], incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        """
        Compute a set of preselected variables
        :param variable_restriction_set: a set of variables that will be taken into account (None for all variables in the incidence graph)
        :param incidence_graph: an incidence graph
        :param depth: depth of the node where this preselection is used
        :return: a set of preselected variables
        """

        pass
    # endregion

    # region Protected method
    def _fill_variable_set(self, current_variable_set: Set[int], all_variable_set: Set[int], required_number_of_variables: int):
        """
        Randomly select variables from the all_variable_set to fill the current_variable_set
        :return: None
        """

        number_of_missing_variables = required_number_of_variables - len(current_variable_set)
        if number_of_missing_variables <= 0:
            return

        complement_variable_set = all_variable_set.difference(current_variable_set)

        if number_of_missing_variables >= len(complement_variable_set):
            current_variable_set.update(complement_variable_set)
        else:
            randomly_picked_variable_set = set(random.sample(complement_variable_set, number_of_missing_variables))
            current_variable_set.update(randomly_picked_variable_set)

    def _update_statistics(self, preselected_variable_set: Set[int], variable_restriction_set: Set[int]) -> None:
        preselected_variable_set_len = len(preselected_variable_set)
        variable_restriction_set_len = len(variable_restriction_set)

        # All variables are preselected
        if preselected_variable_set_len == variable_restriction_set_len:
            self._statistics.all_variables_preselected.add_count(1)
        else:
            self._statistics.all_variables_preselected.add_count(0)

        self._statistics.number_of_preselected_variables.add_count(preselected_variable_set_len)
        self._statistics.ratio_of_preselected_variables.add_count(preselected_variable_set_len / variable_restriction_set_len)
    # endregion
