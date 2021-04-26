# Import
from typing import Set, List
from compiler.solver import Solver
from abc import ABC, abstractmethod
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.compiler.heuristic_exception as h_exception


class DecisionHeuristicAbstract(ABC):
    """
    Decision heuristic
    """

    """
    Private PreselectionHeuristicAbstract preselection_heuristic
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract):
        self.__preselection_heuristic: PreselectionHeuristicAbstract = preselection_heuristic

    # region Abstract method
    @abstractmethod
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int) -> int:
        """
        Compute a decision variable
        :param cut_set: a cut set
        :param incidence_graph: an incidence graph
        :param solver: a solver
        :param assignment_list: a partial assignment for the solver
        :param depth: depth of the node
        :return: a decision variable
        """

        pass
    # endregion

    # region Protected method
    def _get_preselected_variables(self, cut_set: Set[int], incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        """
        Return a set of preselected variables based on the preselection heuristic
        :param cut_set: a cut set
        :param incidence_graph: an incidence graph
        :param depth: depth of the node where the preselection is used
        :return: a set of preselected variables
        :raises PreselectedVariableSetIsEmptyException: if the preselected variable set is empty
        """

        preselected_variable_set = self.__preselection_heuristic.preselect_variables(variable_restriction_set=cut_set,
                                                                                     incidence_graph=incidence_graph,
                                                                                     depth=depth)

        # The preselected variable set is empty
        if not preselected_variable_set:
            raise h_exception.PreselectedVariableSetIsEmptyException()

        return preselected_variable_set
    # endregion
