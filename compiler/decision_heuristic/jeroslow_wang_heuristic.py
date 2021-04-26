# Import
from typing import List, Dict, Set
from compiler.solver import Solver
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class JeroslowWangHeuristic(DecisionHeuristicAbstract):
    """
    Jeroslow-Wang - decision heuristic
    """

    """
    Private bool one_sided
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, one_sided: bool):
        super().__init__(preselection_heuristic)

        self.__one_sided: bool = one_sided

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int) -> int:
        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)
        score_dictionary: Dict[int, int] = dict()       # key: variable, value: score of the variable

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        # Compute score
        for variable in preselected_variable_set:
            positive_score = incidence_graph.literal_sum_lengths_clauses(variable, jeroslow_wang=True)
            negative_score = incidence_graph.literal_sum_lengths_clauses(-variable, jeroslow_wang=True)

            # One-sided
            if self.__one_sided:
                score = max(positive_score, negative_score)
            # Two-sided
            else:
                score = positive_score + negative_score

            score_dictionary[variable] = score

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return decision_variable
    # endregion
