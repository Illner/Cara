# Import
from typing import Set
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class NoneHeuristic(PreselectionHeuristicAbstract):
    """
    None - preselection heuristic
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def preselect_variables(self, variable_restriction_set: Set[int], incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        return variable_restriction_set
    # endregion
