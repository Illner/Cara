# Import
import os
from other.sorted_list import SortedList
from other.dynamic_graph import DynamicGraph
from tests.test_abstract import TestAbstract

# Import exception
import exception.cara_exception as c_exception


class DynamicGraphTest(TestAbstract):
    __DIRECTORY: str = os.path.join("compiler", "dynamic_graph")

    def __init__(self):
        super().__init__(DynamicGraphTest.__DIRECTORY, test_name="Dynamic graph test")

    # region Static method
    @staticmethod
    def dynamic_graph_str(dynamic_graph_func: DynamicGraph) -> str:
        is_connected = dynamic_graph_func.is_connected()
        number_of_components = dynamic_graph_func.get_number_of_components()
        size_of_components = SortedList(dynamic_graph_func.get_size_components())

        result = f"Is connected: {is_connected}, number of components: {number_of_components}, " \
                 f"size of components: {size_of_components.str_delimiter(', ')}"

        components = dynamic_graph_func.get_all_components()
        sorted_components = SortedList([SortedList(component) for component in components])

        result = "\n".join((result, "Components"))
        for sorted_component in sorted_components:
            result = "\n".join((result, sorted_component.str_delimiter(', ')))

        result = "\n".join((result, "Number of edges"))
        edge_list_temp = [(i, j) for i in range(1, 6) for j in range(1, 6) if i < j]
        for node_a, node_b in edge_list_temp:
            result = "\n".join(
                (result, f"({node_a} - {node_b}): {dynamic_graph_func.get_number_of_edges(node_a, node_b)}"))

        result = "\n".join((result, "Neighbours"))
        node_list_temp = [1, 2, 3, 4, 5, 6]
        for node in node_list_temp:
            neighbour_sorted_list = SortedList(dynamic_graph_func.get_neighbour_set(node, copy=False))
            result = "\n".join((result, f"{node}: {neighbour_sorted_list}"))

        result = "\n".join((result, ""))
        return result
    # endregion

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        try:
            dynamic_graph = DynamicGraph()

            # Insert nodes
            actual_result = "\n".join((actual_result, "Add nodes (1 and 2)"))
            dynamic_graph.insert_node(1)
            dynamic_graph.insert_node(2)
            actual_result = "\n".join((actual_result, DynamicGraphTest.dynamic_graph_str(dynamic_graph)))

            actual_result = "\n".join((actual_result, "Add a duplicated node (1)"))
            dynamic_graph.insert_node(1)
            actual_result = "\n".join((actual_result, DynamicGraphTest.dynamic_graph_str(dynamic_graph)))

            # Insert edges
            edge_list = [(1, 2), (1, 3), (4, 5)]
            for node_1, node_2 in edge_list:
                actual_result = "\n".join((actual_result, f"Add an edge ({node_1} - {node_2})"))
                dynamic_graph.insert_edge(node_1, node_2)
                actual_result = "\n".join((actual_result, DynamicGraphTest.dynamic_graph_str(dynamic_graph)))

            # Duplicated edges (insert)
            edge_list = [(1, 2), (1, 2), (3, 4), (1, 3), (1, 2)]
            for node_1, node_2 in edge_list:
                actual_result = "\n".join((actual_result, f"Add an edge ({node_1} - {node_2})"))
                dynamic_graph.insert_edge(node_1, node_2)
                actual_result = "\n".join((actual_result, DynamicGraphTest.dynamic_graph_str(dynamic_graph)))

            # Duplicated edges (delete)
            edge_list = [(1, 3), (1, 2), (1, 3), (4, 5), (1, 2), (5, 1), (6, 7)]
            for node_1, node_2 in edge_list:
                actual_result = "\n".join((actual_result, f"Remove an edge ({node_1} - {node_2})"))
                dynamic_graph.delete_edge(node_1, node_2)
                actual_result = "\n".join((actual_result, DynamicGraphTest.dynamic_graph_str(dynamic_graph)))

            # Isolated nodes
            actual_result = "\n".join((actual_result, "Isolated node (6)"))
            dynamic_graph.insert_node(6)
            dynamic_graph.insert_edge(5, 6)
            dynamic_graph.insert_edge(4, 6)
            dynamic_graph.insert_edge(2, 6)
            actual_result = "\n".join((actual_result, DynamicGraphTest.dynamic_graph_str(dynamic_graph)))

            dynamic_graph.delete_all_neighbours(6)
            actual_result = "\n".join((actual_result, DynamicGraphTest.dynamic_graph_str(dynamic_graph)))

            dynamic_graph.insert_edge(1, 6)
            actual_result = "\n".join((actual_result, DynamicGraphTest.dynamic_graph_str(dynamic_graph)))

            # Insert more edges at once
            edge_list = [(1, 2, 3), (1, 2, 2), (4, 5, 2), (4, 5, 1)]
            for node_1, node_2, number in edge_list:
                actual_result = "\n".join((actual_result, f"Add {number} edge(s) ({node_1} - {node_2})"))
                dynamic_graph.insert_edge(node_1, node_2, number_of_edges=number)
                actual_result = "\n".join((actual_result, DynamicGraphTest.dynamic_graph_str(dynamic_graph)))
        except (c_exception.CaraException, Exception) as err:
            actual_result = "\n".join((actual_result, str(err)))

        return actual_result
    # endregion
