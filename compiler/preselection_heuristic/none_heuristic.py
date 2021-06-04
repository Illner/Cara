# Import
from typing import Set, Union
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract
from compiler_statistics.compiler.preselection_heuristic_statistics import PreselectionHeuristicStatistics


class NoneHeuristic(PreselectionHeuristicAbstract):
    """
    None - preselection heuristic
    """

    def __init__(self, statistics: Union[PreselectionHeuristicStatistics, None] = None):
        super().__init__(statistics)

    # region Override method
    def preselect_variables(self, variable_restriction_set: Union[Set[int], None], incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        self._statistics.get_preselected_variables.start_stopwatch()    # timer (start)

        variable_restriction_set = incidence_graph._variable_set if variable_restriction_set is None else variable_restriction_set

        self._update_statistics(preselected_variable_set=variable_restriction_set,
                                variable_restriction_set=variable_restriction_set)

        self._statistics.get_preselected_variables.stop_stopwatch()     # timer (stop)
        return variable_restriction_set
    # endregion
