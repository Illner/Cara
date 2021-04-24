# Import
from typing import List
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
    def get_decision_variable(self, incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int]) -> int:
        # TODO
        pass
    # endregion
