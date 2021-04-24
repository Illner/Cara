# Import
from typing import Set
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class ClauseReductionApproximationHeuristic(PreselectionHeuristicAbstract):
    """
    Clause reduction approximation (CRA) - preselection heuristic
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def preselect_variables(self, incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        # TODO
        pass
    # endregion
