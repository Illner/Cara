# Import
from hdtgraph.DynamicGraph import Graph
from typing import Set, Dict, List, Tuple


class DynamicGraph(Graph):
    """
    Dynamic graph
    !!! NOT USED !!!!
    """

    """
    Private Dict<int, Set<int>> neighbour_dictionary        # key: node, value: a set of neighbours
    Private Dict<Tuple<int, int>, int> counter_dictionary   # key: <node, node>, value: the number of edges between the nodes (>0)
    Private Set<int> isolated_node_set                      # a set that contains all satisfied nodes (does not count into components)
    """

    def __init__(self):
        self.__neighbour_dictionary: Dict[int, Set[int]] = dict()
        self.__counter_dictionary: Dict[Tuple[int, int], int] = dict()
        self.__isolated_node_set: Set[int] = set()

        super().__init__()

    # region Protected method
    def _generate_key(self, node_1: int, node_2: int) -> Tuple[int, int]:
        """
        Generate a key
        Structure: counter_dictionary
        :param node_1: the first node
        :param node_2: the second node
        :return: the generated key
        """

        node_1, node_2 = self.order_nodes(node_1, node_2)
        return node_1, node_2
    # endregion

    # region Override method
    def insert_node(self, node: int) -> None:
        # The node already exists
        if node in self.__neighbour_dictionary:
            return

        super().insert_node(node)
        self.__neighbour_dictionary[node] = set()

    def insert_edge(self, node_1: int, node_2: int, number_of_edges: int = 1) -> None:
        super().insert_edge(node_1, node_2)     # duplicated edges are ignored

        # The nodes are not isolated anymore
        if node_1 in self.__isolated_node_set:
            self.__isolated_node_set.remove(node_1)
        if node_2 in self.__isolated_node_set:
            self.__isolated_node_set.remove(node_2)

        # node_1 has not been seen yet
        if node_1 not in self.__neighbour_dictionary:
            self.__neighbour_dictionary[node_1] = set()
        self.__neighbour_dictionary[node_1].add(node_2)

        # node_2 has not been seen yet
        if node_2 not in self.__neighbour_dictionary:
            self.__neighbour_dictionary[node_2] = set()
        self.__neighbour_dictionary[node_2].add(node_1)

        counter_key = self._generate_key(node_1, node_2)
        # new edge
        if counter_key not in self.__counter_dictionary:
            self.__counter_dictionary[counter_key] = number_of_edges
        # duplicated edge
        else:
            self.__counter_dictionary[counter_key] += number_of_edges

    def delete_edge(self, node_1: int, node_2: int) -> None:
        counter_key = self._generate_key(node_1, node_2)

        # The edge does not exist
        if counter_key not in self.__counter_dictionary:
            return

        count = self.__counter_dictionary[counter_key]

        # At least one more edge remains
        if count > 1:
            self.__counter_dictionary[counter_key] -= 1
            return

        # The last edge
        del self.__counter_dictionary[counter_key]
        super().delete_edge(node_1, node_2)

        self.__neighbour_dictionary[node_1].remove(node_2)
        self.__neighbour_dictionary[node_2].remove(node_1)
    # endregion

    # region Public method
    def order_nodes(self, node_1: int, node_2: int) -> Tuple[int, int]:
        """
        Order the nodes
        :param node_1: the first node
        :param node_2: the second node
        :return: (node_a, node_b), where node_a < node_b
        """

        if node_1 > node_2:
            node_1, node_2 = node_2, node_1

        return node_1, node_2

    def is_connected(self) -> bool:
        """
        Isolated nodes (satisfied clauses) are ignored
        :return: True if the graph is connected. Otherwise, False is returned
        """

        if self.get_number_of_components() == 1:
            return True

        return False

    def get_number_of_components(self) -> int:
        """
        Return the number of components.
        Isolated nodes (satisfied clauses) are ignored.
        :return: the number of components
        """

        return len(self.levels[0].forest) - len(self.__isolated_node_set)

    def get_all_components(self) -> List[Set[int]]:
        """
        Return a list that contains all components.
        Every component is represented as a set that includes nodes in the component.
        Isolated nodes (satisfied clauses) are ignored.
        :return: a list of all components
        """

        component_list = []

        for ett in self.levels[0].forest:
            node_in_component_set_temp = set(ett.ET_to_list())

            # An isolated node
            if (len(node_in_component_set_temp) == 1) and (node_in_component_set_temp.intersection(self.__isolated_node_set)):
                continue

            component_list.append(node_in_component_set_temp)

        return component_list

    def get_size_components(self) -> List[int]:
        """
        Return a list that contains sizes of all components.
        Isolated nodes (satisfied clauses) are ignored.
        :return: a list of sizes of all components
        """

        component_list = self.get_all_components()
        component_size_list = []

        for component in component_list:
            component_size_list.append(len(component))

        return component_size_list

    def get_neighbour_set(self, node: int, copy: bool = False) -> Set[int]:
        """
        Return a set of neighbours of the node.
        If the node does not exist, an empty set is returned.
        :param node: the node
        :param copy: True if a copy is returned
        :return: a set of neighbours
        """

        # The node does not exist
        if node not in self.__neighbour_dictionary:
            return set()

        if copy:
            return self.__neighbour_dictionary[node].copy()

        return self.__neighbour_dictionary[node]

    def delete_all_neighbours(self, node: int) -> None:
        """
        Delete all edges which are incident with the node.
        If the node does not exist, nothing happens.
        Isolate the node (the clause is satisfied).
        :param node: the node
        :return: None
        """

        # The node does not exist
        if node not in self.__neighbour_dictionary:
            return

        neighbour_set = self.get_neighbour_set(node)
        for neighbour in neighbour_set:
            super().delete_edge(node, neighbour)
            self.__neighbour_dictionary[neighbour].remove(node)

            counter_key = self._generate_key(node, neighbour)
            del self.__counter_dictionary[counter_key]

        self.__neighbour_dictionary[node] = set()
        self.__isolated_node_set.add(node)

    def get_number_of_edges(self, node_1: int, node_2: int) -> int:
        """
        Return the number of edges between the nodes.
        If one of the nodes does not exist, 0 is returned.
        If none edge exists between the nodes, 0 is returned.
        :param node_1: the first node
        :param node_2: the second node
        :return: the number of edges
        """

        # One of the nodes does not exist
        if (node_1 not in self.__neighbour_dictionary) or (node_2 not in self.__neighbour_dictionary):
            return 0

        counter_key = self._generate_key(node_1, node_2)

        # None edge exists
        if counter_key not in self.__counter_dictionary:
            return 0

        return self.__counter_dictionary[counter_key]
    # endregion
