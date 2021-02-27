# Import
from other.sorted_list import SortedList
from tests.test_abstract import TestAbstract
from formula.incidence_graph import IncidenceGraph

# Import exception
import exception.formula.incidence_graph_exception as ig_exception


class IncidenceGraphTest(TestAbstract):
    __FOLDER: str = "formula"
    __ORIGINAL_RESULT_FILE_NAME: str = "original_result_incidence_graph.txt"

    def __init__(self):
        super().__init__(IncidenceGraphTest.__FOLDER, IncidenceGraphTest.__ORIGINAL_RESULT_FILE_NAME, test_name="Incidence graph test")

    # region Static method
    @staticmethod
    def __incidence_graph_1() -> IncidenceGraph:
        """
        Create an incidence graph (incidence_graph_1)
        """

        incidence_graph = IncidenceGraph(3, 4)

        # clause 1
        incidence_graph.add_edge(-1, 0)
        incidence_graph.add_edge(-2, 0)

        # clause 2
        incidence_graph.add_edge(-1, 1)
        incidence_graph.add_edge(2, 1)

        # clause 3
        incidence_graph.add_edge(-2, 2)
        incidence_graph.add_edge(3, 2)

        # clause 4
        incidence_graph.add_edge(-3, 3)

        return incidence_graph
    # endregion

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        actual_result = "\n".join((actual_result, "Creating and connecting nodes", self.__test_1(), ""))    # Test 1
        actual_result = "\n".join((actual_result, "Modification", self.__test_2(), ""))                     # Test 2
        actual_result = "\n".join((actual_result, "Backups and components", self.__test_3()))               # Test 3

        return actual_result
    # endregion

    # region Private method
    def __incidence_graph_str(self, incidence_graph: IncidenceGraph) -> str:
        result = f"Is connected: {incidence_graph.is_connected()}, " \
                 f"number of components: {incidence_graph.number_of_components()}, " \
                 f"number of nodes: {incidence_graph.number_of_nodes()}, " \
                 f"number of variables: {incidence_graph.number_of_variables()}, " \
                 f"number of clauses: {incidence_graph.number_of_clauses()}"

        # Neighbours (variables)
        result = "\n".join((result, "Neighbours (variables)"))
        variable_set = incidence_graph.variable_set()
        for variable in variable_set:
            neighbour_sorted_list = SortedList(incidence_graph.variable_neighbour_set(variable))
            result = "\n".join((result, f"{variable}: {neighbour_sorted_list}"))

        # Neighbours (clauses)
        result = "\n".join((result, "Neighbours (clauses)"))
        clause_id_set = incidence_graph.clause_id_set()
        for clause_id in clause_id_set:
            neighbour_sorted_list = SortedList(incidence_graph.clause_id_neighbour_set(clause_id))
            result = "\n".join((result, f"{clause_id}: {neighbour_sorted_list}"))

        result = "\n".join((result, ""))
        return result

    def __test_1(self) -> str:
        """
        A test for creating and connecting nodes.
        Positive
        :return: the result of the test
        """

        result = ""

        try:
            incidence_graph = IncidenceGraphTest.__incidence_graph_1()
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))
        except ig_exception.IncidenceGraphException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_2(self) -> str:
        """
        A test for modification.
        Positive
        :return: the result of the test
        """

        result = ""

        try:
            incidence_graph = IncidenceGraphTest.__incidence_graph_1()
            result = "Before modification"
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

            # Add a variable
            result = "\n".join((result, "Add a variable (4)"))
            incidence_graph.add_variable(4)
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

            # Add a clause
            result = "\n".join((result, "Add a clause (4)"))
            incidence_graph.add_clause_id(4)
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

            # Add edges
            result = "\n".join((result, "Add an edge (|3| - 4)"))
            incidence_graph.add_edge(3, 4, create_node=True)
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

            result = "\n".join((result, "Add an edge (|-4| - 4)"))
            incidence_graph.add_edge(-4, 4, create_node=True)
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

            result = "\n".join((result, "Add an edge (5 - 4)"))
            incidence_graph.add_edge(5, 4, create_node=True)
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))
        except ig_exception.IncidenceGraphException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_3(self) -> str:
        """
        A test for backups and components.
        Positive
        :return: the result of the test
        """

        result = ""

        try:
            def connected_components_str(incidence_graph_func: IncidenceGraph) -> str:
                result_func = "Components"

                component_sorted_list = list(incidence_graph_func.create_incidence_graphs_for_components())
                component_sorted_list.sort(key=lambda ig: ig.number_of_nodes())
                for component in component_sorted_list:
                    result_func = "\n".join((result_func, self.__incidence_graph_str(component)))

                return result_func

            incidence_graph = IncidenceGraphTest.__incidence_graph_1()

            remove_literal_list_list = [[1, -3], [2]]
            for remove_literal_list in remove_literal_list_list:
                # Remove
                result = "\n".join((result, f"Remove literals ({remove_literal_list})"))
                for remove_literal in remove_literal_list:
                    result = "\n".join((result, f"Remove literal ({remove_literal})"))
                    incidence_graph.remove_literal(remove_literal)
                    result = "\n".join((result, self.__incidence_graph_str(incidence_graph), connected_components_str(incidence_graph)))

                # Restore
                restore_literal_list = remove_literal_list.copy()
                restore_literal_list.reverse()
                result = "\n".join((result, f"Restore literals ({restore_literal_list})"))
                for restore_literal in restore_literal_list:
                    result = "\n".join((result, f"Restore literal ({restore_literal})"))
                    incidence_graph.restore_backup_literal(restore_literal)
                    result = "\n".join((result, self.__incidence_graph_str(incidence_graph), connected_components_str(incidence_graph)))
        except ig_exception.IncidenceGraphException as err:
            result = "\n".join((result, str(err)))

        return result
    # endregion
