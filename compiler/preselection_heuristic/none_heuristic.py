# Import
from typing import Set, Union
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class NoneHeuristic(PreselectionHeuristicAbstract):
    """
    None - preselection heuristic
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def preselect_variables(self, variable_restriction_set: Union[Set[int], None], incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        variable_restriction_set = incidence_graph.variable_set(copy=False) if variable_restriction_set is None else variable_restriction_set

        return variable_restriction_set
    # endregion
