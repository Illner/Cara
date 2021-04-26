# Import
from typing import List, Set
from compiler.solver import Solver
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class MostOccurrencesHeuristic(DecisionHeuristicAbstract):
    """
    Most occurrences - decision heuristic
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract):
        super().__init__(preselection_heuristic)

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int) -> int:
        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        decision_variable = incidence_graph.variable_with_most_occurrences(variable_restriction_set=preselected_variable_set)

        return decision_variable
    # endregion
