# Import
import random
from typing import Set, List
from compiler.solver import Solver
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class WeightedBinariesHeuristic(DecisionHeuristicAbstract):
    """
    Weighted binaries - decision heuristic
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract):
        super().__init__(preselection_heuristic)

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int) -> int:
        # TODO

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)
        decision_variable = random.sample(preselected_variable_set, 1)[0]

        return decision_variable
    # endregion
