# Import
from typing import List
from compiler.solver import Solver
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract

# Import enum
import compiler.enum.decision_heuristic_preselection_enum as dhp_enum


class JeroslowWangHeuristic(DecisionHeuristicAbstract):
    """
    Jeroslow-Wang - decision heuristic
    """

    def __init__(self):
        super().__init__(preselection_heuristic_enum=dhp_enum.DecisionHeuristicPreselectionEnum.NONE)

    # region Override method
    def get_decision_variable(self, incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int]) -> int:
        # TODO
        pass
    # endregion
