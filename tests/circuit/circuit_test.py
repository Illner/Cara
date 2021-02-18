# Import
from circuit.circuit import Circuit
from other.sorted_list import SortedList
from tests.test_abstract import TestAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception


class CircuitTest(TestAbstract):
    __FOLDER: str = "circuit"
    __ORIGINAL_RESULT_FILE_NAME: str = "original_result_circuit.txt"

    def __init__(self):
        super().__init__(CircuitTest.__FOLDER, CircuitTest.__ORIGINAL_RESULT_FILE_NAME, test_name="Circuit test")
        self._set_files(CircuitTest.__FOLDER, "NNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        actual_result = "\n".join((actual_result, "Parsing", self.__test_1(), ""))              # Test 1
        actual_result = "\n".join((actual_result, "Creating circuits", self.__test_2(), ""))    # Test 2
        actual_result = "\n".join((actual_result, "Modification", self.__test_3(), ""))         # Test 3
        actual_result = "\n".join((actual_result, "Operations", self.__test_4(), ""))           # Test 4
        actual_result = "\n".join((actual_result, "Properties", self.__test_5(), ""))           # Test 5
        actual_result = "\n".join((actual_result, "Checking an assumption set and exist quantification set", self.__test_6(), ""))  # Test 6
        actual_result = "\n".join((actual_result, "Smoothness", self.__test_7(), ""))           # Test 7
        actual_result = "\n".join((actual_result, "Leaf as root", self.__test_8(), ""))         # Test 8

        return actual_result
    # endregion

    # region Static method
    @staticmethod
    def __create_circuit_2(set_root: bool = True) -> (Circuit, int):
        """
        Create a circuit (circuit_2)
        Non-decomposable
        Deterministic
        """

        circuit = Circuit(circuit_name="circuit_2")

        circuit.create_literal_leaf(-3)                 # 0
        circuit.create_literal_leaf(1)                  # 1
        circuit.create_constant_leaf(False)             # 2
        circuit.create_literal_leaf(2)                  # 3

        circuit.create_or_node({0, 1})                  # 4
        circuit.create_or_node({1, 2, 3})               # 5

        max_id = circuit.create_and_node({4, 5})        # 6

        if set_root:
            circuit.set_root(max_id)

        return circuit, max_id

    @staticmethod
    def __create_circuit_3(set_root: bool = True) -> (Circuit, int):
        """
        Create a circuit (circuit_3)
        Decomposable
        Deterministic
        Smooth
        """

        circuit = Circuit(circuit_name="circuit_3")

        circuit.create_literal_leaf(-1)                 # 0
        circuit.create_literal_leaf(2)                  # 1
        circuit.create_literal_leaf(-2)                 # 2
        circuit.create_literal_leaf(1)                  # 3
        circuit.create_literal_leaf(3)                  # 4
        circuit.create_literal_leaf(-4)                 # 5
        circuit.create_literal_leaf(4)                  # 6
        circuit.create_literal_leaf(-3)                 # 7

        circuit.create_and_node({0, 1})                 # 8
        circuit.create_and_node({0, 2})                 # 9
        circuit.create_and_node({1, 3})                 # 10
        circuit.create_and_node({2, 3})                 # 11
        circuit.create_and_node({4, 5})                 # 12
        circuit.create_and_node({4, 6})                 # 13
        circuit.create_and_node({5, 7})                 # 14
        circuit.create_and_node({6, 7})                 # 15

        circuit.create_or_node({8, 11}, 1)              # 16
        circuit.create_or_node({13, 14}, 4)             # 17
        circuit.create_or_node({9, 10}, 2)              # 18
        circuit.create_or_node({12, 15}, 3)             # 19

        circuit.create_and_node({16, 17})               # 20
        circuit.create_and_node({18, 19})               # 21

        max_id = circuit.create_or_node({20, 21})       # 22

        if set_root:
            circuit.set_root(max_id)

        return circuit, max_id

    @staticmethod
    def __create_circuit_4(set_root: bool = True) -> (Circuit, int):
        """
        Create a circuit (circuit_4)
        Decomposable
        Non-deterministic
        Non-smooth
        """

        circuit = Circuit(circuit_name="circuit_4")

        circuit.create_literal_leaf(-4)                 # 0
        circuit.create_literal_leaf(1)                  # 1
        circuit.create_literal_leaf(-5)                 # 2
        circuit.create_literal_leaf(2)                  # 3
        circuit.create_literal_leaf(3)                  # 4
        circuit.create_literal_leaf(-6)                 # 5

        circuit.create_or_node({0, 1})                  # 6
        circuit.create_or_node({2, 3})                  # 7
        circuit.create_or_node({4, 5})                  # 8

        circuit.create_literal_leaf(-1)                 # 9
        circuit.create_literal_leaf(-2)                 # 10
        circuit.create_literal_leaf(-3)                 # 11

        circuit.create_and_node({0, 7, 8, 9})           # 12
        circuit.create_and_node({2, 6, 8, 10})          # 13
        circuit.create_and_node({5, 6, 7, 11})          # 14

        circuit.create_literal_leaf(-7)                 # 15
        circuit.create_or_node({12, 13, 14})            # 16
        circuit.create_literal_leaf(7)                  # 17
        circuit.create_and_node({15, 16})               # 18
        max_id = circuit.create_or_node({17, 18}, 7)    # 19

        if set_root:
            circuit.set_root(max_id)

        return circuit, max_id

    @staticmethod
    def __create_circuit_5(set_root: bool = True) -> (Circuit, int):
        """
        Create a circuit (circuit_5)
        Decomposable
        Non-deterministic
        Non-smooth
        """

        circuit = Circuit(circuit_name="circuit_5")

        circuit.create_literal_leaf(-1)                 # 0
        circuit.create_literal_leaf(-3)                 # 1
        circuit.create_literal_leaf(1)                  # 2
        circuit.create_literal_leaf(3)                  # 3
        circuit.create_literal_leaf(-4)                 # 4
        circuit.create_literal_leaf(-5)                 # 5
        circuit.create_literal_leaf(2)                  # 6
        circuit.create_literal_leaf(-2)                 # 7

        circuit.create_or_node({0, 4})                  # 8
        circuit.create_or_node({1, 5})                  # 9
        circuit.create_or_node({2, 4})                  # 10
        circuit.create_or_node({3, 5})                  # 11

        circuit.create_and_node({6, 8, 9})              # 12
        circuit.create_and_node({7, 10, 11})            # 13

        max_id = circuit.create_or_node({12, 13}, 1)    # 14

        if set_root:
            circuit.set_root(max_id)

        return circuit, max_id
    # endregion

    # region Private method
    def __test_1(self) -> str:
        """
        A test for parsing.
        Positive / negative
        :return: the result of the test
        """

        result = ""

        for (file_name, file_path) in self._files:
            try:
                c = Circuit(file_path)
                result = "\n".join((result, file_name, str(c), ""))
            except c_exception.CircuitException as err:
                result = "\n".join((result, file_name, str(err), ""))

        return result

    def __test_2(self) -> str:
        """
        A test for creating circuits.
        Positive
        :return: the result of the test
        """

        result = ""
        circuit_list = [CircuitTest.__create_circuit_2, CircuitTest.__create_circuit_3,
                        CircuitTest.__create_circuit_4, CircuitTest.__create_circuit_5]

        for circuit in circuit_list:
            result = "\n".join((result, circuit.__name__))

            try:
                c, _ = circuit()
                result = "\n".join((result, str(c), ""))
            except c_exception.CircuitException as err:
                result = "\n".join((result, str(err), ""))

        return result

    def __test_3(self) -> str:
        """
        A test for modification and getters.
        Positive / negative
        :return: the result of the test
        """

        result = ""

        try:
            circuit, max_id = CircuitTest.__create_circuit_4(set_root=False)

            # Root
            result = "\n".join((result, "Root", "Root is not set", str(circuit.root_id)))
            root_id_list = [3, 7, 13, 20, 19]
            for root_id in root_id_list:
                try:
                    circuit.set_root(root_id)
                    result = "\n".join((result, f"Root is set ({root_id})", str(circuit.root_id)))
                except c_exception.CircuitException as err:
                    result = "\n".join((result, f"Root is set ({root_id})", str(err)))

            # id_exist, node_exist, get_node
            result = "\n".join((result, "id_exist, node_exist, get_node"))
            node_id_list = [5, 6, 12, 19, 25, -1]
            for node_id in node_id_list:
                node_id_exist_temp = circuit.id_exist(node_id)
                node_temp = circuit.get_node(node_id)
                node_exist_temp = None if node_temp is None else circuit.node_exist(node_temp)

                result = "\n".join((result, f"{str(node_id)}",
                                    f"id_exist: {node_id_exist_temp}",
                                    f"node_exist: {node_exist_temp}",
                                    f"get_node: {repr(node_temp)}"))

            # Comment
            result = "\n".join((result, "Comment"))
            # New comment
            circuit.set_comments("New comment 1\nNew comment 2")
            result = "\n".join((result, "New comments", str(circuit), ""))
            # Clear comment
            circuit.clear_comments()
            result = "\n".join((result, "Clear comments", str(circuit), ""))

            # Modification
            result = "\n".join((result, "Modification"))
            # Add a leaf
            literal_list = [1, -1, -5, 5, 5]
            for literal in literal_list:
                node_id_temp = circuit.create_literal_leaf(literal)
                result = "\n".join((result, f"Add a leaf ({literal})", f"Node id: {node_id_temp}"))

            # Add an OR node (l v -l)
            literal_list = [1, 6, 8]
            for literal in literal_list:
                for _ in range(2):
                    literal_node_id_1_temp = circuit.create_literal_leaf(literal)
                    literal_node_id_2_temp = circuit.create_literal_leaf(-literal)
                    or_node_id_temp = circuit.create_or_node({literal_node_id_1_temp, literal_node_id_2_temp}, literal)
                    or_node_temp = circuit.get_node(or_node_id_temp)

                    result = "\n".join((result, f"Literal: {literal}", f"{repr(or_node_temp)}"))

            # Decision node
            node_id = circuit.create_decision_node(1, max_id, 26)
            circuit.set_root(node_id)
            result = "\n".join((result, f"Add a decision node", f"{repr(circuit)}"))

            # Add a constant leaf
            constant_list = [True, False, True, False]
            for constant in constant_list:
                node_id_temp = circuit.create_constant_leaf(constant)
                result = "\n".join((result, f"Add a constant leaf ({constant})", f"Node id: {node_id_temp}"))

            or_node_id_temp = circuit.create_or_node({circuit.create_constant_leaf(True), circuit.create_constant_leaf(False)})
            circuit.add_edge(29, or_node_id_temp)

            # Add an edge / is connected
            result = "\n".join((result, "Add an edge / is connected", f"is connected: {circuit.is_circuit_connected()}"))
            edge_list = [(18, 20), (16, 23), (7, 18), (1, 35), (40, 45), (25, 21), (26, 21)]
            for (edge_from, edge_to) in edge_list:
                try:
                    result = "\n".join((result, f"Add edge ({edge_from} -> {edge_to})"))
                    circuit.add_edge(edge_from, edge_to)
                    result = "\n".join((result, f"is connected: {circuit.is_circuit_connected()}", f"{repr(circuit)}", ""))
                except c_exception.CircuitException as err:
                    result = "\n".join((result, str(err), ""))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_4(self) -> str:
        """
        A test for operations.
        Positive / negative
        :return: the result of the test
        """

        result = ""
        circuits_and_sets = [(CircuitTest.__create_circuit_2, [(set(), set())]),
                             (CircuitTest.__create_circuit_3, [(set(), set()), ({-1}, set()), ({-1}, {2}), ({-1, -2, -3, -4}, set()), ({-3}, {1, 2, 4})]),
                             (CircuitTest.__create_circuit_5, [(set(), set()), ({-1}, set()), (set(), {4, 5}), ({-1, 3}, {4, 5}), ({-1, 3, 4, 5}, set()), ({1, -3}, {4, 5})])]

        try:
            for circuit, sets in circuits_and_sets:
                result = "\n".join((result, circuit.__name__))

                c, _ = circuit()
                operation_set = [c.is_satisfiable, c.clause_entailment, c.model_counting, c.minimum_default_cardinality]

                for operation in operation_set:
                    result = "\n".join((result, operation.__name__))

                    for assumption_set, exist_quantification_set in sets:
                        try:
                            result = "\n".join((result, f"assumption set: {SortedList(assumption_set)}, exist quantification set: {SortedList(exist_quantification_set)}"))

                            temp = operation(assumption_set, exist_quantification_set)

                            result = "\n".join((result, str(temp)))
                        except c_exception.CircuitException as err:
                            result = "\n".join((result, str(err)))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_5(self) -> str:
        """
        A test for properties.
        Positive
        :return: the result of the test
        """

        result = ""

        try:
            circuit, root_id = CircuitTest.__create_circuit_3()
            result = "\n".join((result, f"Decomposability: {circuit.is_decomposable()}, determinism: {circuit.is_deterministic()}, smoothness: {circuit.is_smooth()}, circuit type: {circuit.circuit_type.name}"))

            # Add a leaf
            leaf_id = circuit.create_literal_leaf(5)
            result = "\n".join((result, f"Decomposability: {circuit.is_decomposable()}, determinism: {circuit.is_deterministic()}, smoothness: {circuit.is_smooth()}, circuit type: {circuit.circuit_type.name}"))

            # Add an edge (root -> new_leaf)
            circuit.add_edge(root_id, leaf_id)
            result = "\n".join((result, f"Decomposability: {circuit.is_decomposable()}, determinism: {circuit.is_deterministic()}, smoothness: {circuit.is_smooth()}, circuit type: {circuit.circuit_type.name}"))

            # Add an edge (12 -> 2)
            circuit.add_edge(12, 2)
            result = "\n".join((result, f"Decomposability: {circuit.is_decomposable()}, determinism: {circuit.is_deterministic()}, smoothness: {circuit.is_smooth()}, circuit type: {circuit.circuit_type.name}"))

            # Change the root
            circuit.set_root(20)
            result = "\n".join((result, f"Decomposability: {circuit.is_decomposable()}, determinism: {circuit.is_deterministic()}, smoothness: {circuit.is_smooth()}, circuit type: {circuit.circuit_type.name}"))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_6(self) -> str:
        """
        A test for checking an assumption set and exist quantification set.
        Negative
        :return: the result of the test
        """

        result = ""
        set_list = [({2}, {-1}), ({1}, {1}), ({-1}, {1}), ({1, -1}, set())]

        try:
            circuit, _ = CircuitTest.__create_circuit_3()

            for assumption_set, exist_quantification_set in set_list:
                try:
                    result = "\n".join((result, f"Assumption set: {SortedList(assumption_set)}, exist quantification set: {SortedList(exist_quantification_set)}"))
                    circuit.is_satisfiable(assumption_set, exist_quantification_set)
                except c_exception.CircuitException as err:
                    result = "\n".join((result, str(err)))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_7(self) -> str:
        """
        A test for smoothness.
        Positive
        :return: the result of the test
        """

        result = ""
        circuit_list = [CircuitTest.__create_circuit_2, CircuitTest.__create_circuit_3,
                        CircuitTest.__create_circuit_4, CircuitTest.__create_circuit_5]

        for circuit in circuit_list:
            result = "\n".join((result, circuit.__name__))

            try:
                c, _ = circuit()
                result = "\n".join((result, f"Smooth: {c.is_smooth()}", ""))
                c.smooth()
                result = "\n".join((result, f"Smooth: {c.is_smooth()}", ""))
            except c_exception.CircuitException as err:
                result = "\n".join((result, str(err), ""))

        return result

    def __test_8(self) -> str:
        """
        A leaf as the root of the circuit.
        :return: the result of the test
        """

        result = ""

        try:
            circuit = Circuit()
            id = circuit.create_literal_leaf(1)
            circuit.set_root(id)

            result = "\n".join((result, str(circuit), ""))

            # Operations
            result = "\n".join((result, f"Satisfiable: {circuit.is_satisfiable(set(), set())}"))
            result = "\n".join((result, f"Clause entailment: {circuit.clause_entailment(set(), set())}"))
            result = "\n".join((result, f"Model counting: {circuit.model_counting(set(), set())}"))
            result = "\n".join((result, f"Minimum default-cardinality: {circuit.minimum_default_cardinality({1}, set())}", ""))

            # Smooth
            result = "\n".join((result, "Smooth", ""))
            circuit.smooth()

            # Properties
            result = "\n".join((result, f"Decomposability: {circuit.is_decomposable()}, determinism: {circuit.is_deterministic()}, smoothness: {circuit.is_smooth()}, circuit type: {circuit.circuit_type.name}"))
            result = "\n".join((result, f"is connected: {circuit.is_circuit_connected()}"))

        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result
    # endregion
