# Import
import os
from typing import List, Union
from other.sorted_list import SortedList
from tests.test_abstract import TestAbstract
from circuit.node.node_abstract import NodeAbstract
from circuit.node.leaf.constant_leaf import ConstantLeaf
from circuit.node.leaf.literal_leaf import LiteralLeaf
from circuit.node.leaf.leaf_abstract import LeafAbstract
from circuit.node.inner_node.and_inner_node import AndInnerNode
from circuit.node.inner_node.or_inner_node import OrInnerNode
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception


class NodeTest(TestAbstract):
    __FOLDER: str = os.path.join("circuit", "node")

    def __init__(self):
        super().__init__(NodeTest.__FOLDER, test_name="Node test")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        actual_result = "\n".join((actual_result, "Creating and connecting nodes", self.__test_1(), ""))            # Test 1
        actual_result = "\n".join((actual_result, "Modification", self.__test_2(), ""))                             # Test 2
        actual_result = "\n".join((actual_result, "Detecting a cycle", self.__test_3(), ""))                        # Test 3
        actual_result = "\n".join((actual_result, "Satisfiability", self.__test_4(), ""))                           # Test 4
        actual_result = "\n".join((actual_result, "Satisfiability (negative)", self.__test_5(), ""))                # Test 5
        actual_result = "\n".join((actual_result, "Model counting", self.__test_6(), ""))                           # Test 6
        actual_result = "\n".join((actual_result, "Model counting (negative)", self.__test_7(), ""))                # Test 7
        actual_result = "\n".join((actual_result, "Minimum default-cardinality", self.__test_8(), ""))              # Test 8
        actual_result = "\n".join((actual_result, "Minimum default-cardinality (negative)", self.__test_9(), ""))   # Test 9
        actual_result = "\n".join((actual_result, "Caches", self.__test_10(), ""))                                  # Test 10

        return actual_result
    # endregion

    # region Static method
    @staticmethod
    def __create_circuit_1() -> List[Union[NodeAbstract, LeafAbstract, InnerNodeAbstract]]:
        """
        Create a circuit (circuit_1)
        Decomposable
        Deterministic
        """

        n_0 = ConstantLeaf(True, 0)
        n_1 = LiteralLeaf(-3, 1)
        n_2 = AndInnerNode({n_0, n_1}, 2)
        n_3 = LiteralLeaf(1, 3)
        n_4 = ConstantLeaf(False, 4)
        n_5 = LiteralLeaf(2, 5)
        n_6 = OrInnerNode({n_2, n_1}, 6)
        n_7 = OrInnerNode({n_3, n_4, n_5}, 7)
        n_8 = AndInnerNode({n_6, n_7}, 8)

        return [n_0, n_1, n_2, n_3, n_4, n_5, n_6, n_7, n_8]

    @staticmethod
    def __create_circuit_2() -> List[Union[NodeAbstract, LeafAbstract, InnerNodeAbstract]]:
        """
        Create a circuit (circuit_2)
        Non-decomposable
        Deterministic
        """

        n_0 = LiteralLeaf(-3, 0)
        n_1 = LiteralLeaf(1, 1)
        n_2 = ConstantLeaf(False, 2)
        n_3 = LiteralLeaf(2, 3)
        n_4 = OrInnerNode({n_0, n_1}, 4)
        n_5 = OrInnerNode({n_1, n_2, n_3}, 5)
        n_6 = AndInnerNode({n_4, n_5}, 6)

        return [n_0, n_1, n_2, n_3, n_4, n_5, n_6]

    @staticmethod
    def __create_circuit_3() -> List[Union[NodeAbstract, LeafAbstract, InnerNodeAbstract]]:
        """
        Create a circuit (circuit_3)
        Decomposable
        Deterministic
        Smooth
        """

        n_0 = LiteralLeaf(-1, 0)
        n_1 = LiteralLeaf(2, 1)
        n_2 = LiteralLeaf(-2, 2)
        n_3 = LiteralLeaf(1, 3)
        n_4 = LiteralLeaf(3, 4)
        n_5 = LiteralLeaf(-4, 5)
        n_6 = LiteralLeaf(4, 6)
        n_7 = LiteralLeaf(-3, 7)

        n_8 = AndInnerNode({n_0, n_1}, 8)
        n_9 = AndInnerNode({n_0, n_2}, 9)
        n_10 = AndInnerNode({n_1, n_3}, 10)
        n_11 = AndInnerNode({n_2, n_3}, 11)
        n_12 = AndInnerNode({n_4, n_5}, 12)
        n_13 = AndInnerNode({n_4, n_6}, 13)
        n_14 = AndInnerNode({n_5, n_7}, 14)
        n_15 = AndInnerNode({n_6, n_7}, 15)

        n_16 = OrInnerNode({n_8, n_11}, 16, 1)
        n_17 = OrInnerNode({n_13, n_14}, 17, 4)
        n_18 = OrInnerNode({n_9, n_10}, 18, 2)
        n_19 = OrInnerNode({n_12, n_15}, 19, 3)

        n_20 = AndInnerNode({n_16, n_17}, 20)
        n_21 = AndInnerNode({n_18, n_19}, 21)

        n_22 = ConstantLeaf(False, 22)
        n_23 = ConstantLeaf(True, 23)

        n_24 = OrInnerNode({n_20, n_21}, 24)

        return [n_0, n_1, n_2, n_3, n_4, n_5, n_6, n_7, n_8, n_9, n_10, n_11, n_12, n_13, n_14, n_15, n_16,
                n_17, n_18, n_19, n_20, n_21, n_22, n_23, n_24]

    @staticmethod
    def __create_circuit_4() -> List[Union[NodeAbstract, LeafAbstract, InnerNodeAbstract]]:
        """
        Create a circuit (circuit_4)
        Decomposable
        Non-deterministic
        Non-smooth
        """

        n_0 = LiteralLeaf(-4, 0)
        n_1 = LiteralLeaf(1, 1)
        n_2 = LiteralLeaf(-5, 2)
        n_3 = LiteralLeaf(2, 3)
        n_4 = LiteralLeaf(3, 4)
        n_5 = LiteralLeaf(-6, 5)
        n_9 = LiteralLeaf(-1, 9)
        n_10 = LiteralLeaf(-2, 10)
        n_11 = LiteralLeaf(-3, 11)
        n_15 = LiteralLeaf(-7, 15)
        n_17 = LiteralLeaf(7, 17)

        n_6 = OrInnerNode({n_0, n_1}, 6)
        n_7 = OrInnerNode({n_2, n_3}, 7)
        n_8 = OrInnerNode({n_4, n_5}, 8)

        n_12 = AndInnerNode({n_9, n_0, n_7, n_8}, 12)
        n_13 = AndInnerNode({n_6, n_2, n_10, n_8}, 13)
        n_14 = AndInnerNode({n_6, n_7, n_5, n_11}, 14)

        n_16 = OrInnerNode({n_12, n_13, n_14}, 16)
        n_18 = AndInnerNode({n_15, n_16}, 18)

        n_19 = ConstantLeaf(False, 19)
        n_20 = ConstantLeaf(True, 20)

        n_21 = OrInnerNode({n_17, n_18}, 21, 7)

        return [n_0, n_1, n_2, n_3, n_4, n_5, n_6, n_7, n_8, n_9, n_10, n_11, n_12, n_13, n_14, n_15, n_16,
                n_17, n_18, n_19, n_20, n_21]

    @staticmethod
    def __create_circuit_5() -> List[Union[NodeAbstract, LeafAbstract, InnerNodeAbstract]]:
        """
        Create a circuit (circuit_5)
        Decomposable
        Non-deterministic
        Non-smooth
        """

        n_0 = LiteralLeaf(-1, 0)
        n_1 = LiteralLeaf(-3, 1)
        n_2 = LiteralLeaf(1, 2)
        n_3 = LiteralLeaf(3, 3)
        n_4 = LiteralLeaf(-4, 4)
        n_5 = LiteralLeaf(-5, 5)
        n_6 = LiteralLeaf(2, 6)
        n_7 = LiteralLeaf(-2, 7)

        n_8 = OrInnerNode({n_0, n_4}, 8)
        n_9 = OrInnerNode({n_1, n_5}, 9)
        n_10 = OrInnerNode({n_2, n_4}, 10)
        n_11 = OrInnerNode({n_3, n_5}, 11)

        n_12 = AndInnerNode({n_6, n_8, n_9}, 12)
        n_13 = AndInnerNode({n_7, n_10, n_11}, 13)

        n_14 = ConstantLeaf(False, 14)
        n_15 = ConstantLeaf(True, 15)

        n_16 = OrInnerNode({n_12, n_13}, 16, 1)

        return [n_0, n_1, n_2, n_3, n_4, n_5, n_6, n_7, n_8, n_9, n_10, n_11, n_12, n_13, n_14, n_15, n_16]
    # endregion

    # region Private method
    def __test_1(self) -> str:
        """
        A test for creating and connecting nodes.
        Positive
        :return: the result of the test
        """

        result = ""
        circuits = [NodeTest.__create_circuit_1, NodeTest.__create_circuit_2,
                    NodeTest.__create_circuit_3, NodeTest.__create_circuit_4, NodeTest.__create_circuit_5]

        for circuit in circuits:
            try:
                result = "\n".join((result, circuit.__name__))

                node_list = circuit()

                for node in node_list:
                    result = "\n".join((result, repr(node)))
            except c_exception.CircuitException as err:
                result = "\n".join((result, str(err)))

        return result

    def __test_2(self) -> str:
        """
        A test for modification (add_parent, remove_parent, add_child, remove_child).
        Positive
        :return: the result of the test
        """

        result = ""
        try:
            # Before modification
            node_list = NodeTest.__create_circuit_2()
            result = "Before modification"
            for node in node_list:
                result = "\n".join((result, repr(node)))

            # Remove a leaf
            result = "\n".join((result, "Remove a leaf"))
            node_list[4]._remove_child(node_list[1])
            node_list[1]._remove_parent(node_list[4])
            for node in node_list:
                result = "\n".join((result, repr(node)))

            # Add a circuit
            result = "\n".join((result, "Add a circuit"))
            node_list.append(LiteralLeaf(4, 7))
            node_list.append(ConstantLeaf(True, 8))
            node_list.append(AndInnerNode({node_list[7], node_list[8]}, 9))
            node_list[4]._add_child(node_list[9])
            node_list[9]._add_parent(node_list[4])
            for node in node_list:
                result = "\n".join((result, repr(node)))

            # Add a child
            result = "\n".join((result, "Add a child"))
            node_list[5]._add_child(node_list[7])
            node_list[7]._add_parent(node_list[5])
            for node in node_list:
                result = "\n".join((result, repr(node)))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_3(self) -> str:
        """
        A test for detecting a cycle.
        Negative
        :return: the result of the test
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_1()

            node_list[2]._add_child(node_list[8])
            node_list[8]._add_parent(node_list[2])
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_4(self) -> str:
        """
        A test for satisfiability.
        Positive
        :return: the result of the test
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_1()
            root = node_list[-1]

            for cache in range(2):
                for node in node_list:
                    result = "\n".join((result, f"Node: {node.id}, cache: {bool(cache)}, sat: {node.is_satisfiable(set(), set(), use_caches=bool(cache))}"))

                # Assumption
                assumption_list_temp = [{3}, {-3, -1}, {-1, -2}, {-3}]
                for assumption in assumption_list_temp:
                    result = "\n".join((result, f"Assumption: {SortedList(assumption)}, cache: {bool(cache)}, sat: {root.is_satisfiable(assumption, set(), use_caches=bool(cache))}"))

                # Exist quantification
                exist_quantification_list_temp = [{3}, {3, 1}, {1, 2}, {1, 2, 3}]
                for exist_quantification in exist_quantification_list_temp:
                    result = "\n".join((result, f"Exist quantification: {SortedList(exist_quantification)}, cache: {bool(cache)}, sat: {root.is_satisfiable(set(), exist_quantification, use_caches=bool(cache))}"))

                # Assumption and exist quantification
                list_temp = [({3}, {1, 2}), ({3}, {1}), ({-1}, {3})]
                for assumption, exist_quantification in list_temp:
                    result = "\n".join((result, f"Assumption: {SortedList(assumption)}, exist quantification: {SortedList(exist_quantification)}, cache: {bool(cache)}, sat: {root.is_satisfiable(assumption, exist_quantification, use_caches=bool(cache))}"))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_5(self) -> str:
        """
        A test for satisfiability.
        Negative
        :return: the result of the test
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_2()
            root = node_list[-1]
            root.is_satisfiable(set(), set())
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_6(self) -> str:
        """
        A test for model counting.
        Positive
        :return: the result of the test
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_3()
            root = node_list[-1]

            for cache in range(2):
                for node in node_list:
                    result = "\n".join((result, f"Node: {node.id}, cache: {bool(cache)}, count of models: {node.model_counting(set(), set(), use_caches=bool(cache))}"))

                # Assumption
                assumption_list_temp = [{-1}, {1}, {-1, -2}, {1, 2}]
                for assumption in assumption_list_temp:
                    result = "\n".join((result, f"Assumption: {SortedList(assumption)}, cache: {bool(cache)}, count of models: {root.model_counting(assumption, set(), use_caches=bool(cache))}"))

                # Exist quantification
                exist_quantification_list_temp = [{1}, {1, 2}, {1, 2, 3}]
                for exist_quantification in exist_quantification_list_temp:
                    result = "\n".join((result, f"Exist quantification: {SortedList(exist_quantification)}, cache: {bool(cache)}, count of models: {root.model_counting(set(), exist_quantification, use_caches=bool(cache))}"))

                # Assumption and exist quantification
                list_temp = [({-1}, {2, 3}), ({1}, {2, 3}), ({1, 2}, {3, 4})]
                for assumption, exist_quantification in list_temp:
                    result = "\n".join((result, f"Assumption: {SortedList(assumption)}, exist quantification: {SortedList(exist_quantification)}, cache: {bool(cache)}, count of models: {root.model_counting(assumption, exist_quantification, use_caches=bool(cache))}"))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_7(self) -> str:
        """
        A test for model counting.
        Negative
        :return: the result of the test
        """

        result = ""
        circuits = [NodeTest.__create_circuit_1, NodeTest.__create_circuit_2]

        for circuit in circuits:
            try:
                result = "\n".join((result, circuit.__name__))

                node_list = circuit()
                root = node_list[-1]
                root.model_counting(set(), set())
            except c_exception.CircuitException as err:
                result = "\n".join((result, str(err)))

        return result

    def __test_8(self) -> str:
        """
        A test for minimum default-cardinality.
        Positive
        :return: the result of the test
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_5()
            root = node_list[-1]
            variable_set = root._get_variable_in_circuit_set(True)

            for cache in range(2):
                for node in node_list:
                    result = "\n".join((result, f"Node: {node.id}, cache: {bool(cache)}, minimum cardinality: {node.minimum_default_cardinality(set(), variable_set, use_caches=bool(cache))}"))

                # Default
                default_list_temp = [{4}, {4, 5}]
                for default in default_list_temp:
                    result = "\n".join((result, f"Default: {SortedList(default)}, cache: {bool(cache)}, minimum cardinality: {root.minimum_default_cardinality(set(), default, use_caches=bool(cache))}"))

                # Observation and default
                list_temp = [({-1, 3}, {4, 5}), ({1, -3}, {4, 5}), ({1, 3}, {4, 5})]
                for observation, default in list_temp:
                    result = "\n".join((result, f"Observation: {SortedList(observation)}, default: {SortedList(default)}, cache: {bool(cache)}, minimum cardinality: {root.minimum_default_cardinality(observation, default, use_caches=bool(cache))}"))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_9(self) -> str:
        """
        A test for minimum default-cardinality.
        Negative
        :return: the result of the test
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_2()
            root = node_list[-1]
            root.minimum_default_cardinality(set(), set())
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    def __test_10(self) -> str:
        """
        A test for clearing caches.
        Positive
        :return: the result of the test
        """

        result = ""

        # is_satisfiable
        result = "\n".join((result, "is_satisfiable"))
        try:
            node_list = NodeTest.__create_circuit_1()
            root = node_list[-1]

            result = "\n".join((result, f"Sat: {root.is_satisfiable({-1}, set())}"))

            # Add a constant leaf (False)
            result = "\n".join((result, "Add a constant leaf (False)"))
            node_list.append(ConstantLeaf(False, 9))
            node_list[8]._add_child(node_list[9])
            node_list[9]._add_parent(node_list[8])
            result = "\n".join((result, f"Sat: {root.is_satisfiable({-1}, set())}"))

            # Remove a constant leaf (False)
            result = "\n".join((result, "Remove a constant leaf (False)"))
            node_list[8]._remove_child(node_list[9])
            node_list[9]._remove_parent(node_list[8])
            result = "\n".join((result, f"Sat: {root.is_satisfiable({-1}, set())}"))

            result = "\n".join((result, f"Sat: {root.is_satisfiable({-1, -2}, set())}"))

            # Add a literal leaf (-2)
            result = "\n".join((result, "Add a literal leaf (-2)"))
            node_list.append(LiteralLeaf(-2, 10))
            node_list[7]._add_child(node_list[10])
            node_list[10]._add_parent(node_list[7])
            result = "\n".join((result, f"Sat: {root.is_satisfiable({-1, -2}, set())}"))

            # Remove a literal leaf (-2)
            result = "\n".join((result, "Remove a literal leaf (-2)"))
            node_list[7]._remove_child(node_list[10])
            node_list[10]._remove_parent(node_list[7])
            result = "\n".join((result, f"Sat: {root.is_satisfiable({-1, -2}, set())}"))
            result = "\n".join((result, f"Sat: {root.is_satisfiable({-1}, set())}"))

            # Add a literal leaf (4)
            result = "\n".join((result, "Add a literal leaf (4)"))
            node_list.append(LiteralLeaf(4, 11))
            node_list[7]._add_child(node_list[11])
            node_list[11]._add_parent(node_list[7])
            result = "\n".join((result, f"Sat: {root.is_satisfiable({-1, -2}, set())}"))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        # minimum_default_cardinality
        result = "\n".join((result, "minimum_default_cardinality"))
        try:
            node_list = NodeTest.__create_circuit_5()
            root = node_list[-1]

            result = "\n".join((result, f"Minimum cardinality: {root.minimum_default_cardinality({-1, 3}, {4, 5})}"))

            # Add an edge (10 -> 0)
            result = "\n".join((result, "Add an edge (10 -> 0)"))
            node_list[10]._add_child(node_list[0])
            node_list[0]._add_parent(node_list[10])
            result = "\n".join((result, f"Minimum cardinality: {root.minimum_default_cardinality({-1, 3}, {4, 5})}"))

            # Remove an edge (10 -> 0)
            result = "\n".join((result, "Remove an edge (10 -> 0)"))
            node_list[10]._remove_child(node_list[0])
            node_list[0]._remove_parent(node_list[10])
            result = "\n".join((result, f"Minimum cardinality: {root.minimum_default_cardinality({-1, 3}, {4, 5})}"))

            result = "\n".join((result, f"Minimum cardinality: {root.minimum_default_cardinality({-1, 3}, {5, 6})}"))

            # Add a literal leaf (-6)
            result = "\n".join((result, "Add a literal leaf (-6)"))
            node_list.append(LiteralLeaf(-6, 17))
            node_list[13]._add_child(node_list[17])
            node_list[17]._add_parent(node_list[13])
            result = "\n".join((result, f"Minimum cardinality: {root.minimum_default_cardinality({-1, 3}, {5, 6})}"))

            # Remove a literal leaf (-6)
            result = "\n".join((result, "Remove a literal leaf (-6)"))
            node_list[13]._remove_child(node_list[17])
            node_list[17]._remove_parent(node_list[13])
            result = "\n".join((result, f"Minimum cardinality: {root.minimum_default_cardinality({-1, 3}, {5, 6})}"))
            result = "\n".join((result, f"Minimum cardinality: {root.minimum_default_cardinality({-1, 3}, {4, 5})}"))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result
    # endregion
