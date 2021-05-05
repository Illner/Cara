# Import
from typing import List, Set, Dict
from compiler.solver import Solver
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class VsadsHeuristic(DecisionHeuristicAbstract):
    """
    VSADS - decision heuristic
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract):
        super().__init__(preselection_heuristic)

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int) -> int:
        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        vsids_score_list = solver.get_vsids_score()
        score_dictionary: Dict[int, int] = dict()   # key: a variable, value: score of the variable

        # Compute score
        for variable in preselected_variable_set:
            # DLCS
            positive_score = incidence_graph.literal_number_of_occurrences(variable)
            negative_score = incidence_graph.literal_number_of_occurrences(-variable)
            score = positive_score + negative_score

            # VSIDS
            score += vsids_score_list[variable - 1]

            score_dictionary[variable] = score

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return decision_variable
    # endregion
