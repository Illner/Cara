# Import
from typing import Set
from abc import ABC, abstractmethod
from formula.incidence_graph import IncidenceGraph


class PreselectionHeuristicAbstract(ABC):
    """
    Preselection heuristic
    """

    def __init__(self):
        pass

    # region Abstract method
    @abstractmethod
    def preselect_variables(self, incidence_graph: IncidenceGraph) -> Set[int]:
        """
        Compute a set of preselected variables
        :param incidence_graph: an incidence graph
        :return: a set of preselected variables
        """

        pass
    # endregion
