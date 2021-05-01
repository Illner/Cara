# Import
import os
from other.sorted_list import SortedList
from tests.test_abstract import TestAbstract
from formula.incidence_graph import IncidenceGraph

# Import exception
import exception.cara_exception as c_exception

# Import enum
import formula.enum.eliminating_redundant_clauses_enum as erc_enum


class IncidenceGraphTest(TestAbstract):
    __DIRECTORY: str = os.path.join("formula", "incidence_graph")

    def __init__(self):
        super().__init__(IncidenceGraphTest.__DIRECTORY, test_name="Incidence graph test")

    # region Static method
    @staticmethod
    def __incidence_graph_1() -> IncidenceGraph:
        """
        Create an incidence graph (incidence_graph_1)
        """

        incidence_graph = IncidenceGraph()

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

    @staticmethod
    def __incidence_graph_2() -> IncidenceGraph:
        """
        Create an incidence graph (incidence_graph_2)
        """

        incidence_graph = IncidenceGraph()

        # clause 1
        incidence_graph.add_edge(1, 0)
        incidence_graph.add_edge(4, 0)

        # clause 2
        incidence_graph.add_edge(1, 1)
        incidence_graph.add_edge(2, 1)
        incidence_graph.add_edge(3, 1)

        # clause 3
        incidence_graph.add_edge(1, 2)
        incidence_graph.add_edge(2, 2)
        incidence_graph.add_edge(3, 2)
        incidence_graph.add_edge(4, 2)
        incidence_graph.add_edge(-5, 2)

        # clause 4
        incidence_graph.add_edge(-3, 3)

        # clause 5
        incidence_graph.add_edge(-3, 4)
        incidence_graph.add_edge(5, 4)

        # clause 6
        incidence_graph.add_edge(3, 5)
        incidence_graph.add_edge(5, 5)

        return incidence_graph

    @staticmethod
    def __incidence_graph_str(incidence_graph: IncidenceGraph) -> str:
        result = f"Is connected: {incidence_graph.is_connected()}, " \
                 f"number of components: {incidence_graph.number_of_components()}, " \
                 f"number of nodes: {incidence_graph.number_of_nodes()}, " \
                 f"number of variables: {incidence_graph.number_of_variables()}, " \
                 f"number of clauses: {incidence_graph.number_of_clauses()}"

        # Neighbours (variables)
        result = "\n".join((result, "Neighbours (variables)"))
        for variable in sorted(incidence_graph.variable_set(copy=False)):
            neighbour_sorted_list = SortedList(incidence_graph.variable_neighbour_set(variable))
            number_of_neighbours = incidence_graph.number_of_neighbours_variable(variable)
            result = "\n".join((result, f"{variable} ({number_of_neighbours}): {neighbour_sorted_list}"))

        # Neighbours (clauses)
        result = "\n".join((result, "Neighbours (clauses)"))
        for clause_id in sorted(incidence_graph.clause_id_set(copy=False)):
            neighbour_sorted_list = SortedList(incidence_graph.clause_id_neighbour_set(clause_id))
            number_of_neighbours = incidence_graph.number_of_neighbours_clause_id(clause_id)
            result = "\n".join((result, f"{clause_id} ({number_of_neighbours}): {neighbour_sorted_list}"))

        result = "\n".join((result, ""))
        return result
    # endregion

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""
        test_list = [("Creating and connecting nodes", self.__test_1),
                     ("Modification", self.__test_2),
                     ("Components and backups - assignment", self.__test_3),
                     ("Backups - variable simplification", self.__test_4),
                     ("Backups - subsumption", self.__test_5)]

        for test_name, test in test_list:
            try:
                actual_result = "\n".join((actual_result, test_name, test(), ""))
            except Exception as err:
                actual_result = "\n".join((actual_result, test_name, str(err), ""))

        return actual_result
    # endregion

    # region Private method
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
        except c_exception.CaraException as err:
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
            incidence_graph.add_edge(3, 4)
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

            result = "\n".join((result, "Add an edge (|-4| - 4)"))
            incidence_graph.add_edge(-4, 4)
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

            result = "\n".join((result, "Add an edge (5 - 4)"))
            incidence_graph.add_edge(5, 4)
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))
        except c_exception.CaraException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_3(self) -> str:
        """
        A test for components and backups - assignment.
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

            remove_literal_list_list = [[1, -3], [2], [-1, 3]]
            for remove_literal_list in remove_literal_list_list:
                # Remove
                result = "\n".join((result, f"Remove literals ({remove_literal_list})"))
                for remove_literal in remove_literal_list:
                    result = "\n".join((result, f"Remove literal ({remove_literal})"))
                    incidence_graph.remove_literal(remove_literal, erc_enum.EliminatingRedundantClausesEnum.NONE)
                    result = "\n".join((result, self.__incidence_graph_str(incidence_graph), connected_components_str(incidence_graph)))

                # Restore
                restore_literal_list = remove_literal_list.copy()
                restore_literal_list.reverse()
                result = "\n".join((result, f"Restore literals ({restore_literal_list})"))
                for restore_literal in restore_literal_list:
                    result = "\n".join((result, f"Restore literal ({restore_literal})"))
                    incidence_graph.restore_backup_literal(restore_literal)
                    result = "\n".join((result, self.__incidence_graph_str(incidence_graph), connected_components_str(incidence_graph)))
        except c_exception.CaraException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_4(self) -> str:
        """
        A test for backups - variable simplification.
        Positive
        :return: the result of the test
        """

        result = ""

        try:
            incidence_graph = IncidenceGraphTest.__incidence_graph_1()

            variable_simplification_dictionary_list = [{1: {3}}, {1: {2}}, {2: {1}}, {2: {3}}, {3: {1, 2}}]

            for variable_simplification_dictionary in variable_simplification_dictionary_list:
                result = "\n".join((result, f"Variable simplification: ({variable_simplification_dictionary})"))
                incidence_graph.merge_variable_simplification(variable_simplification_dictionary)
                result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

                result = "\n".join((result, "Restore:"))
                incidence_graph.restore_backup_variable_simplification()
                result = "\n".join((result, self.__incidence_graph_str(incidence_graph), ""))
        except c_exception.CaraException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_5(self) -> str:
        """
        A test for backups - subsumption.
        Positive
        :return: the result of the test
        """

        result = ""

        try:
            incidence_graph = IncidenceGraphTest.__incidence_graph_2()
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

            subsumed_clause_set = {0, 1, 3}
            result = "\n".join((result, f"Subsumption: ({SortedList(subsumed_clause_set).str_delimiter(', ')})"))
            incidence_graph.remove_subsumed_clause_variable_set(subsumed_clause_set)
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))

            result = "\n".join((result, "Restore:"))
            incidence_graph.restore_backup_subsumption_variable()
            result = "\n".join((result, self.__incidence_graph_str(incidence_graph)))
        except c_exception.CaraException as err:
            result = "\n".join((result, str(err)))

        return result
    # endregion
