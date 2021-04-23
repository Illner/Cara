# Import
from compiler.solver import Solver
from abc import ABC, abstractmethod
from typing import Set, List, Union
from formula.incidence_graph import IncidenceGraph

from compiler.decision_heuristic.preselection_heuristic.none_heuristic import NoneHeuristic
from compiler.decision_heuristic.preselection_heuristic.prop_z_heuristic import PropZHeuristic
from compiler.decision_heuristic.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract
from compiler.decision_heuristic.preselection_heuristic.clause_reduction_approximation_heuristic import ClauseReductionApproximationHeuristic

# Import exception
import exception.cara_exception as ca_exception

# Import enum
import compiler.enum.decision_heuristic_preselection_enum as dhp_enum


class DecisionHeuristicAbstract(ABC):
    """
    Decision heuristic
    """

    """
    Private DecisionHeuristicPreselectionAbstract preselection_heuristic
    """

    def __init__(self, preselection_heuristic_enum: dhp_enum.DecisionHeuristicPreselectionEnum):
        # Preselection heuristic
        self.__preselection_heuristic: Union[PreselectionHeuristicAbstract, None] = None
        # None
        if preselection_heuristic_enum == dhp_enum.DecisionHeuristicPreselectionEnum.NONE:
            self.__preselection_heuristic = NoneHeuristic()
        # Prop_z
        elif preselection_heuristic_enum == dhp_enum.DecisionHeuristicPreselectionEnum.PROP_Z:
            self.__preselection_heuristic = PropZHeuristic()
        # CRA
        elif preselection_heuristic_enum == dhp_enum.DecisionHeuristicPreselectionEnum.CRA:
            self.__preselection_heuristic = ClauseReductionApproximationHeuristic()
        # Not supported
        else:
            raise ca_exception.FunctionNotImplementedException("__init__ (DecisionHeuristicAbstract)",
                                                               f"this type of preselection heuristic ({preselection_heuristic_enum.name}) is not implemented")

    # region Protected method
    def _get_preselected_variables(self, incidence_graph: IncidenceGraph) -> Set[int]:
        """
        Return a set of preselected variables based on the preselected heuristic
        :param incidence_graph: an incidence graph
        :return: a set of preselected variables
        """

        return self.__preselection_heuristic.preselect_variables(incidence_graph)
    # endregion

    # region Abstract method
    @abstractmethod
    def get_decision_variable(self, incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int]) -> int:
        """
        Compute a decision variable
        :param incidence_graph: an incidence graph
        :param solver: a solver
        :param assignment_list: a partial assignment for the solver
        """

        pass
    # endregion
