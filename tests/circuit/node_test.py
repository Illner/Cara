# Import
import warnings
from typing import Union
from tests.test_abstract import TestAbstract
from circuit.node.node_abstract import NodeAbstract
from circuit.node.leaf.constant_leaf import ConstantLeaf
from circuit.node.leaf.literal_leaf import LiteralLeaf
from circuit.node.leaf.leaf_abstract import LeafAbstract
from circuit.node.inner_node.and_inner_node import AndInnerNode
from circuit.node.inner_node.or_inner_node import OrInnerNode
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract

# Import exception
import exception.circuit_exception as c_exception

# Warning
warnings.simplefilter('ignore')


class NodeTest(TestAbstract):
    __FOLDER: str = "circuit"
    __ORIGINAL_RESULT_FILE_NAME: str = "original_result_node.txt"

    def __init__(self):
        super().__init__(NodeTest.__FOLDER, NodeTest.__ORIGINAL_RESULT_FILE_NAME, test_name="Node test")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        actual_result = "\n".join((actual_result, "Test 1", self.__test_1(), ""))   # Test 1
        actual_result = "\n".join((actual_result, "Test 2", self.__test_2(), ""))   # Test 2
        actual_result = "\n".join((actual_result, "Test 3", self.__test_3(), ""))   # Test 3
        actual_result = "\n".join((actual_result, "Test 4", self.__test_4(), ""))   # Test 4
        actual_result = "\n".join((actual_result, "Test 5", self.__test_5(), ""))   # Test 5
        actual_result = "\n".join((actual_result, "Test 6", self.__test_6(), ""))   # Test 6

        return actual_result
    # endregion

    # region Static method
    @staticmethod
    def __create_circuit_1() -> list[Union[NodeAbstract, LeafAbstract, InnerNodeAbstract]]:
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
    def __create_circuit_2() -> list[Union[NodeAbstract, LeafAbstract, InnerNodeAbstract]]:
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
    def __test_1() -> str:
        """
        A standard test for creating and connecting nodes.
        Positive
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_1()

            for node in node_list:
                result = "\n".join((result, repr(node)))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    @staticmethod
    def __test_2() -> str:
        """
        A test for satisfiability.
        Positive
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_1()

            for cache in range(2):
                for node in node_list:
                    result = "\n".join((result, f"Node: {node.id}, cache: {bool(cache)}, sat: {node.is_satisfiable(set(), set(), use_caches=bool(cache))}"))

                root = node_list[-1]

                # Assumption
                assumption_list_temp = [{3}, {-3, -1}, {-1, -2}, {-3}]
                for assumption in assumption_list_temp:
                    result = "\n".join((result, f"Assumption: {assumption}, cache: {bool(cache)}, sat: {root.is_satisfiable(assumption, set(), use_caches=bool(cache))}"))

                # Exist quantification
                exist_quantification_list_temp = [{3}, {3, 1}, {1, 2}]
                for exist_quantification in exist_quantification_list_temp:
                    result = "\n".join((result, f"Exist quantification: {exist_quantification}, cache: {bool(cache)}, sat: {root.is_satisfiable(set(), exist_quantification, use_caches=bool(cache))}"))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    @staticmethod
    def __test_3() -> str:
        """
        A test for satisfiability.
        Negative
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_2()
            root = node_list[-1]
            root.is_satisfiable(set(), set())
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    @staticmethod
    def __test_4() -> str:
        """
        A test for modification (add_parent, remove_parent, add_child, remove_child).
        Positive
        """

        result = ""
        try:
            # Before modification
            node_list = NodeTest.__create_circuit_2()
            result = "Before modification"
            for node in node_list:
                result = "\n".join((result, repr(node)))

            # Remove a leaf
            node_list[4]._remove_child(node_list[1])
            node_list[1]._remove_parent(node_list[4])
            result = "\n".join((result, "Remove a leaf"))
            for node in node_list:
                result = "\n".join((result, repr(node)))

            # Add a circuit
            node_list.append(LiteralLeaf(4, 7))
            node_list.append(ConstantLeaf(True, 8))
            node_list.append(AndInnerNode({node_list[7], node_list[8]}, 9))
            node_list[4]._add_child(node_list[9])
            node_list[9]._add_parent(node_list[4])
            result = "\n".join((result, "Add a circuit"))
            for node in node_list:
                result = "\n".join((result, repr(node)))

            # Add a child
            node_list[5]._add_child(node_list[7])
            node_list[7]._add_parent(node_list[5])
            result = "\n".join((result, "Add a child"))
            for node in node_list:
                result = "\n".join((result, repr(node)))
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    @staticmethod
    def __test_5() -> str:
        """
        A test for detecting a cycle.
        Negative
        """

        result = ""
        try:
            node_list = NodeTest.__create_circuit_1()

            node_list[2]._add_child(node_list[8])
            node_list[8]._add_parent(node_list[2])
        except c_exception.CircuitException as err:
            result = "\n".join((result, str(err)))

        return result

    @staticmethod
    def __test_6() -> str:
        """
        A test for clearing caches.
        Positive
        """

        result = ""
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

        return result
    # endregion
