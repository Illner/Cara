# Import
from typing import Set, List
from hdtgraph.DynamicGraph import Graph


class DynamicGraph(Graph):
    def __init__(self):
        super().__init__()

    def is_connected(self) -> bool:
        """
        :return: True if the graph is connected, otherwise False is returned
        """

        if len(self.levels[0].forest) <= 1:
            return True

        return False

    def get_all_components(self) -> List[Set[int]]:
        """
        Return a list that contains all components.
        Every component is represented as a set that contains nodes in the component.
        :return: a list of all components
        """

        component_list = []

        for ett in self.levels[0].forest:
            component_list.append(set(ett.ET_to_list()))

        return component_list
