# Import
from typing import Set
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class PropZHeuristic(PreselectionHeuristicAbstract):
    """
    Prop_z - preselection heuristic
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def preselect_variables(self, incidence_graph: IncidenceGraph) -> Set[int]:
        # TODO
        pass
    # endregion
