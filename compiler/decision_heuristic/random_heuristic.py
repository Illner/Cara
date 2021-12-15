# Import
import random
from compiler.solver import Solver
from typing import List, Set, Union, Dict
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.compiler.heuristic_exception as h_exception


class RandomHeuristic(DecisionHeuristicAbstract):
    """
    Random - decision heuristic
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract):
        super().__init__(preselection_heuristic)

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int],
                              depth: int, additional_score_dictionary: Union[Dict[int, int], None] = None,
                              max_number_of_returned_decision_variables: Union[int, None] = 1) -> Union[int, List[int]]:
        # Additional score is not used
        if additional_score_dictionary is not None:
            raise h_exception.AdditionalScoreIsNotSupportedException()

        # Returning more decision variables is not supported
        if max_number_of_returned_decision_variables != 1:
            raise h_exception.DecisionHeuristicDoesNotSupportReturningMoreDecisionVariablesException()

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)
        decision_variable = random.sample(preselected_variable_set, 1)[0]

        return decision_variable
    # endregion
