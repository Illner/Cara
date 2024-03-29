# Import
from compiler.solver import Solver
from typing import List, Set, Dict, Union, Tuple
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.compiler.heuristic_exception as h_exception


class VsidsHeuristic(DecisionHeuristicAbstract):
    """
    VSIDS - decision heuristic
    """

    """
    Private bool d4_version
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, d4_version: bool = True):
        super().__init__(preselection_heuristic)

        self.__d4_version: bool = d4_version

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int,
                              additional_score_dictionary: Union[Dict[int, int], None] = None, max_number_of_returned_decision_variables: Union[int, None] = 1,
                              return_score: bool = False) -> Union[Union[int, List[int]], Tuple[Union[int, List[int]], int]]:
        # Additional score is used
        if additional_score_dictionary is not None:
            raise h_exception.AdditionalScoreIsNotSupportedException()

        # Returning more decision variables is not supported
        if max_number_of_returned_decision_variables != 1:
            raise h_exception.DecisionHeuristicDoesNotSupportReturningMoreDecisionVariablesException()

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            decision_variable = list(preselected_variable_set)[0]
            return (decision_variable, 0) if return_score else decision_variable

        vsids_score_list = solver.get_vsids_score(d4_version=self.__d4_version)

        score_dictionary: Dict[int, int] = dict()   # key: a variable, value: score of the variable

        # Compute score
        for variable in preselected_variable_set:
            score_dictionary[variable] = vsids_score_list[variable - 1]

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return (decision_variable, score_dictionary[decision_variable]) if return_score else decision_variable
    # endregion
