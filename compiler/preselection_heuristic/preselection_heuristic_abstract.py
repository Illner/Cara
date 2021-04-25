# Import
import random
from typing import Set
from abc import ABC, abstractmethod
from formula.incidence_graph import IncidenceGraph


class PreselectionHeuristicAbstract(ABC):
    """
    Preselection heuristic
    """

    def __init__(self):
        pass

    # region Abstract method
    @abstractmethod
    def preselect_variables(self, incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        """
        Compute a set of preselected variables
        :param incidence_graph: an incidence graph
        :param depth: depth of the node where this preselection is used
        :return: a set of preselected variables
        """

        pass
    # endregion

    # region Protected method
    def _fill_variable_set(self, incidence_graph: IncidenceGraph, variable_set: Set[int], required_number_of_variables: int):
        """
        Randomly select variables to fill the variable_set
        :return: None
        """

        number_of_missing_variables = required_number_of_variables - len(variable_set)
        if number_of_missing_variables <= 0:
            return

        complement_variable_set = incidence_graph.variable_set(copy=False).difference(variable_set)

        if number_of_missing_variables >= len(complement_variable_set):
            variable_set.update(complement_variable_set)
        else:
            randomly_picked_variable_set = set(random.sample(complement_variable_set, number_of_missing_variables))
            variable_set.update(randomly_picked_variable_set)
    # endregion
