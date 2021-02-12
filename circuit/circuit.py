# Import
import warnings
from sortedcontainers import SortedDict
from other.sorted_list import SortedList
from typing import Set, Dict, List, Union
from circuit.node.node_abstract import NodeAbstract
from circuit.node.leaf.literal_leaf import LiteralLeaf
from circuit.node.leaf.constant_leaf import ConstantLeaf
from circuit.node.leaf.leaf_abstract import LeafAbstract
from circuit.node.inner_node.or_inner_node import OrInnerNode
from circuit.node.inner_node.and_inner_node import AndInnerNode
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract

# Import exception
import exception.circuit_exception as c_exception

# Import enum
import circuit.circuit_type_enum as ct_enum
import circuit.node.node_type_enum as nt_enum


class Circuit:
    """
    Circuit representation
    """

    """
    Private int id_counter
    Private str comments
    Private int size    # The number of edges in the circuit + the sizes of all leaves in the circuit
    Private CircuitTypeEnum circuit_type
    Private str circuit_name
    Private NodeAbstract root
    
    Private Dict<int, NodeAbstract> id_node_dictionary              # key: id, value: node

    Private Dict<int, NodeAbstract> literal_unique_node_cache       # key: literal, value: node
    Private List<NodeAbstract> constant_unique_node_cache           # [False: node, True: node]
    Private Dict<str, NodeAbstract> and_unique_node_cache           # key = {number >= 0}+
    Private Dict<str, NodeAbstract> or_unique_node_cache            # key = {number >= 0}+
    """

    def __init__(self, dimacs_nnf_file_path: str = None, circuit_name: str = "Circuit"):
        # region Initialization
        self.__id_counter: int = 0
        self.__comments: str = ""
        self.__size: Union[int, None] = None
        self.__circuit_name: str = circuit_name
        self.__circuit_type: Union[ct_enum.CircuitTypeEnum, None] = None
        self.__root: Union[NodeAbstract, None] = None

        self.__id_node_dictionary: Dict[int, NodeAbstract] = dict()

        self.__literal_unique_node_cache: Dict[int, NodeAbstract] = dict()
        self.__constant_unique_node_cache: List[Union[NodeAbstract, None]] = [None, None]
        self.__and_unique_node_cache: Dict[str, NodeAbstract] = dict()
        self.__or_unique_node_cache: Dict[str, NodeAbstract] = dict()
        # endregion

        # The file with the circuit was given
        if dimacs_nnf_file_path is not None:
            self.__create_nnf(dimacs_nnf_file_path)

    # region Private method
    def __create_nnf(self, dimacs_nnf_file_path: str) -> None:
        """
        Convert the circuit from the file into our structure
        :param dimacs_nnf_file_path: the file which is in the DIMACS NNF format
        """

        root_id = None

        with open(dimacs_nnf_file_path, "r") as file:
            v = None  # the number of nodes
            e = None  # the number of edges
            n = None  # the number of variables
            is_n_line_defined = False

            for line_id, line in enumerate(file.readlines()):
                line = line.strip()

                # The line is empty
                if not line:
                    continue

                # Comment line
                if line.startswith("c") or line.startswith("C"):
                    if not self.__comments:  # First comment
                        self.__comments = line[1:].strip()
                    else:
                        self.__comments = ", ".join((self.__comments, line[1:].strip()))
                    continue

                # End of file (optional)
                if line.startswith("%"):
                    break

                # N line
                if line.startswith("nnf"):
                    is_n_line_defined = True
                    line_array_temp = line.split()
                    # N line has an invalid format
                    if len(line_array_temp) != 4:  # nnf number_of_nodes number_of_edges number_of_variables
                        raise c_exception.InvalidDimacsNnfFormatException(
                            "nnf line has an invalid format - valid format is 'nnf number_of_nodes number_of_edges number_of_variables'")

                    # Parse the parameters
                    try:
                        v = int(line_array_temp[1])
                        e = int(line_array_temp[2])
                        n = int(line_array_temp[3])
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(
                            f"the number of nodes ({line_array_temp[1]}), the number of edges ({line_array_temp[2]}) or the number of variables ({line_array_temp[3]}) is not an integer")
                    continue

                # N line has not been mentioned
                if not is_n_line_defined:
                    raise c_exception.NLineIsNotMentionedException()

                # Node line
                # Constant leaf (TRUE)
                if line == "A 0" or line == "a 0":
                    root_id = self.create_constant_leaf(True, use_unique_node_cache=False)
                    continue

                # Constant leaf (FALSE)
                if line == "O 0 0" or line == "O 0" or line == "o 0 0" or line == "o 0":
                    root_id = self.create_constant_leaf(False, use_unique_node_cache=False)
                    continue

                # Literal leaf
                if line.startswith("L") or line.startswith("l"):
                    line_array_temp = line.split()
                    # Invalid line
                    if len(line_array_temp) != 2:
                        raise c_exception.InvalidDimacsNnfFormatException(
                            f"the literal leaf ({line}) defined on line {line_id + 1} has an invalid number of parameters")

                    # Parse the literal
                    try:
                        literal_temp = int(line_array_temp[1])
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(
                            f"the literal ({line_array_temp[1]}) mentioned on line {line_id + 1} in the leaf node is not an integer")

                    root_id = self.create_literal_leaf(literal_temp, use_unique_node_cache=False)
                    continue

                # AND node
                if line.startswith("A") or line.startswith("a"):
                    line_array_temp = line.split()
                    # Invalid line
                    if len(line_array_temp) < 3:
                        raise c_exception.InvalidDimacsNnfFormatException(
                            f"the AND node ({line}) defined on line {line_id + 1} has an invalid number of parameters")

                    # Parse the IDs
                    child_id_set_temp = set()
                    try:
                        c_temp = int(line_array_temp[1])
                        if c_temp < 0:
                            raise c_exception.InvalidDimacsNnfFormatException(
                                f"the c value ({c_temp}) mentioned on line {line_id + 1} in the AND node is negative")

                        for i in range(2, len(line_array_temp)):
                            id_temp = int(line_array_temp[i])

                            # Check if the node with the id has been already declared
                            node_child_temp = self.get_node(id_temp)
                            if node_child_temp is None:
                                raise c_exception.InvalidDimacsNnfFormatException(
                                    f"the node (child) with the id ({id_temp}) mentioned on line {line_id + 1} in the AND node has not been seen yet")

                            child_id_set_temp.add(id_temp)

                        # The c value and the number of children don't correspond
                        if len(child_id_set_temp) != c_temp:
                            raise c_exception.InvalidDimacsNnfFormatException(
                                f"the c value ({c_temp}) and the number of children ({len(child_id_set_temp)}) mentioned on line {line_id + 1} in the AND node don't correspond")
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(
                            f"the c value or some id of a node ({line}) mentioned on line {line_id + 1} in the AND node is not an integer")

                    root_id = self.create_and_node(child_id_set_temp, use_unique_node_cache=False)
                    continue

                # OR node
                if line.startswith("O") or line.startswith("o"):
                    line_array_temp = line.split()
                    # Invalid line
                    if len(line_array_temp) < 4:
                        raise c_exception.InvalidDimacsNnfFormatException(
                            f"the OR node ({line}) defined on line {line_id + 1} has an invalid number of parameters")

                    # Parse the IDs
                    child_id_set_temp = set()
                    try:
                        j_temp = int(line_array_temp[1])
                        if (j_temp <= 0) or (j_temp > n):
                            raise c_exception.InvalidDimacsNnfFormatException(
                                f"the j value ({j_temp}) mentioned on line {line_id + 1} in the OR node is not a valid number")

                        c_temp = int(line_array_temp[2])
                        if c_temp < 0:
                            raise c_exception.InvalidDimacsNnfFormatException(
                                f"the c value ({c_temp}) mentioned on line {line_id + 1} in the OR node is negative")

                        j_temp = None if j_temp == 0 else j_temp

                        for i in range(3, len(line_array_temp)):
                            id_temp = int(line_array_temp[i])

                            # Check if the node with the id has been already declared
                            node_child_temp = self.get_node(id_temp)
                            if node_child_temp is None:
                                raise c_exception.InvalidDimacsNnfFormatException(
                                    f"the node (child) with the id ({id_temp}) mentioned on line {line_id + 1} in the OR node has not been seen yet")

                            child_id_set_temp.add(id_temp)

                        # The c value and the number of children don't correspond
                        if len(child_id_set_temp) != c_temp:
                            raise c_exception.InvalidDimacsNnfFormatException(
                                f"the c value ({c_temp}) and the number of children ({len(child_id_set_temp)}) mentioned on line {line_id + 1} in the OR node don't correspond")
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(
                            f"the c value, j value or some id of a node ({line}) mentioned on line {line_id + 1} in the OR node is not an integer")

                    root_id = self.create_or_node(child_id_set_temp, j_temp, use_unique_node_cache=False)
                    continue

                raise c_exception.InvalidDimacsNnfFormatException(f"the line ({line_id + 1}) starts with an invalid char ({line})")

        # The file does not contain any node
        if not len(self.__id_node_dictionary):
            raise c_exception.InvalidDimacsNnfFormatException("file does not contain any node")

        if root_id is None:
            raise c_exception.SomethingWrongException("root was not set")

        self.set_root(root_id)

        # Check v, e, n
        if v != self.number_of_nodes:
            warnings.warn(f"The number of nodes in the circuit ({self.number_of_nodes}) differs from the v value ({v})!")
            # raise c_exception.SomethingWrongException(f"the number of nodes in the circuit ({self.number_of_nodes}) differs from the v value ({v})")
        if e != self.size:
            warnings.warn(f"The number of edges in the circuit ({self.size}) differs from the e value ({e})!")
            # raise c_exception.SomethingWrongException(f"the number of edges in the circuit ({self.size}) differs from the e value ({e})")
        if n != self.number_of_variables:
            warnings.warn(f"The number of variables in the circuit ({self.number_of_variables}) differs from the n value ({n})!")
            # raise c_exception.SomethingWrongException(f"the number of variables in the circuit ({self.number_of_variables}) differs from the n value ({n})")

    def __get_new_id(self) -> int:
        """
        Return a new ID. The ID counter will be incremented.
        :return: a new ID
        """

        id_temp = self.__id_counter
        self.__id_counter += 1

        return id_temp

    def __add_new_node(self, node: NodeAbstract) -> None:
        """
        Add the node to the circuit.
        If some node already exists in the circuit with the same ID, raise an exception (NodeWithSameIDAlreadyExistsInCircuitException).
        :param node: the node
        """

        id_temp = node.id

        # There is already some node with the same ID
        if self.node_exist(node):
            raise c_exception.NodeWithSameIDAlreadyExistsInCircuitException(str(node))

        self.__id_node_dictionary[id_temp] = node

    def __smooth_create_and_node(self, id_node: int, variable_set: Set[int]) -> NodeAbstract:
        """
        This function is used for smoothing.
        id_node --> AND (id_node, (v_1 OR -v_1), (v_2 OR -v_2), ...)
        If the node's ID does not exist in the circuit, raise an exception (NodeWithIDDoesNotExistInCircuitException).
        :param id_node: the node's ID
        :param variable_set: the set of variables
        :return: the new AND node
        """

        node = self.get_node(id_node)

        # The node does not exist in the circuit
        if node is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(id_node))

        child_id_set = {id_node}
        for variable in variable_set:
            v_id = self.create_literal_leaf(variable)
            non_v_id = self.create_literal_leaf(-variable)

            or_node_id = self.create_or_node({v_id, non_v_id}, variable)
            child_id_set.add(or_node_id)

        and_node_id = self.create_and_node(child_id_set)
        return self.get_node(and_node_id)

    def __topological_ordering_recursion(self, node_id: int, topological_ordering_list: List[int]) -> List[int]:
        node = self.get_node(node_id)

        # The node does not exist in the circuit
        if node is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(node_id))

        # Base case - the node is a leaf
        if isinstance(node, LeafAbstract):
            if node_id not in topological_ordering_list:
                topological_ordering_list.append(node_id)

            return topological_ordering_list

        # Recursion - the node is an inner node
        child_id_list = node.get_child_id_list()
        child_id_list.sort()
        for child_id in child_id_list:
            # The child has been already explored
            if child_id in topological_ordering_list:
                continue

            self.__topological_ordering_recursion(child_id, topological_ordering_list)

        topological_ordering_list.append(node_id)
        return topological_ordering_list

    def __compute_size_of_circuit(self) -> None:
        """
        Compute the size of the circuit
        """

        # Root of the circuit is not set
        if self.__root is None:
            self.__size = None
            return

        self.__size = 0
        node_set = self.__root._get_node_in_circuit_set()

        for node in node_set:
            self.__size += node.node_size()

    def __add_edge(self, from_node: NodeAbstract, to_node: NodeAbstract, call_update: bool = True) -> None:
        """
        Add an oriented edge (from_node -> to_node) in the circuit.
        :param call_update: True for calling the update function after this modification.
        If the parameter is set to False, then the circuit may be inconsistent after this modification.
        """

        to_node._add_parent(from_node)
        from_node._add_child(to_node, call_update)

    def __remove_edge(self, from_node: NodeAbstract, to_node: NodeAbstract, call_update: bool = True) -> None:
        """
        Remove an oriented edge (from_node -> to_node) in the circuit.
        :param call_update: True for calling the update function after this modification.
        If the parameter is set to False, then the circuit may be inconsistent after this modification.
        """

        to_node._remove_parent(from_node)
        from_node._remove_child(to_node, call_update)

    def __generate_key_cache(self, child_id_set: Set[int]) -> str:
        """
        Generate a key for caching based on the children set.
        Cache: and_unique_node_cache, or_unique_node_cache
        :param child_id_set: the set of child's id
        :return: the generated key based on the child_id_set
        """

        child_id_sorted_list = SortedList(child_id_set)
        return child_id_sorted_list.str_delimiter("-")
    # endregion

    # region Static method
    @staticmethod
    def __check_assumption_set_and_exist_quantification_set(assumption_set: Set[int],
                                                            exist_quantification_set: Set[int],
                                                            assumption_and_exist_set: bool = True,
                                                            error: bool = True) -> bool:
        """
        Check if the assumption set and existential quantification set are valid.
        The assumption set and existential quantification set must be disjoint (with respect to variables).
        No complementary literals can appear in the assumption set.
        If the sets are not valid, raise an exception (AssumptionSetAndExistentialQuantificationSetAreNotDisjointException,
        AssumptionSetContainsComplementLiteralsException, SetContainsLiteralsButOnlyVariablesAreAllowedException)
        if the error is set to True, otherwise False is returned.
        Can be used for a default set and an observation set as well.
        :param assumption_set: the assumption set / observation set
        :param exist_quantification_set: the existential quantification set / default set
        :param assumption_and_exist_set: True for an assumption and existential quantification set. False for an observation
        and default set.
        :param error: the error
        :return: if the error is set to False, True is returned if the sets are valid, otherwise False is returned
        """

        # Check if the sets are disjoint
        intersection_set_temp = set()
        for variable in exist_quantification_set:
            if (variable in assumption_set) or (-variable in assumption_set):
                intersection_set_temp.add(variable)

        if intersection_set_temp:
            if error:
                raise c_exception.AssumptionSetAndExistentialQuantificationSetAreNotDisjointException(intersection_set_temp, assumption_and_exist_set)
            else:
                return False

        # Check if the existential quantification set contains only variables
        for var in exist_quantification_set:
            if var <= 0:
                set_name_temp = "existential quantification set" if assumption_and_exist_set else "default set"
                raise c_exception.SetContainsLiteralsButOnlyVariablesAreAllowedException(set_name_temp, exist_quantification_set)

        # Check complementary literals in the assumption set
        complementary_literals_set_temp = set()
        for lit in assumption_set:
            if -lit in assumption_set:
                complementary_literals_set_temp.add(lit)

        if complementary_literals_set_temp:
            if error:
                raise c_exception.AssumptionSetContainsComplementLiteralsException(complementary_literals_set_temp, assumption_and_exist_set)
            else:
                return False

        return True
    # endregion

    # region Public method
    def node_exist(self, node: NodeAbstract) -> bool:
        """
        Check if the node's id exists in the circuit.
        :param node: the node
        :return: Return True if the node's id exists in the circuit. Otherwise False is returned.
        """

        return self.id_exist(node.id)

    def id_exist(self, id: int) -> bool:
        """
        Check if a node with the id exists in the circuit.
        :param id: the id
        :return: Return True if a node with the id exists in the circuit. Otherwise False is returned.
        """

        return id in self.__id_node_dictionary

    def get_node(self, id: int) -> Union[NodeAbstract, None]:
        """
        Return the node with the id. If the node does not exist in the circuit None is returned.
        :param id: the id
        :return: the node with the id
        """

        # The id does not exist
        if not self.id_exist(id):
            return None

        return self.__id_node_dictionary[id]

    def create_constant_leaf(self, constant: bool, use_unique_node_cache: bool = True) -> int:
        """
        Create a new constant leaf in the circuit.
        If the node already exists in the circuit, then new node will not be created, and the existed node will be used instead.
        :param constant: the value of the constant leaf
        :param use_unique_node_cache: True if unique node caching can be used, otherwise False
        :return: the node's id
        """

        # The node already exists in the circuit
        if use_unique_node_cache and (self.__constant_unique_node_cache[int(constant)] is not None):
            return self.__constant_unique_node_cache[int(constant)].id

        node = ConstantLeaf(constant, self.__get_new_id())
        self.__add_new_node(node)
        self.__constant_unique_node_cache[int(constant)] = node

        return node.id

    def create_literal_leaf(self, literal: int, use_unique_node_cache: bool = True) -> int:
        """
        Create a new literal leaf in the circuit.
        If the node already exists in the circuit, then new node will not be created, and the existed node will be used instead.
        :param literal: the value of the literal leaf
        :param use_unique_node_cache: True if unique node caching can be used, otherwise False
        :return: the node's id
        """

        # The node already exists in the circuit
        if use_unique_node_cache and (literal in self.__literal_unique_node_cache):
            return self.__literal_unique_node_cache[literal].id

        node = LiteralLeaf(literal, self.__get_new_id())
        self.__add_new_node(node)
        self.__literal_unique_node_cache[literal] = node

        return node.id

    def create_and_node(self, child_id_set: Set[int], use_unique_node_cache: bool = True) -> int:
        """
        Create a new AND node in the circuit.
        If some child's id does not exist in the circuit, raise an exception (NodeWithIDDoesNotExistInCircuitException).
        :param child_id_set: the set of child's id
        :param use_unique_node_cache: True if unique node caching can be used, otherwise False
        :return: the node's id
        """

        # No child was given -> constant leaf (TRUE)
        if not len(child_id_set):
            return self.create_constant_leaf(True)

        # Check if the node already exists in the cache
        key_cache = self.__generate_key_cache(child_id_set)
        if use_unique_node_cache and (key_cache in self.__and_unique_node_cache):
            return self.__and_unique_node_cache[key_cache].id

        child_node_set = set()
        for child_id in child_id_set:
            child_temp = self.get_node(child_id)

            # The child's id does not exist in the circuit
            if child_temp is None:
                raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(child_id), "trying to create an AND node with a nonexisting child")

            child_node_set.add(child_temp)

        node = AndInnerNode(child_node_set, self.__get_new_id())
        self.__add_new_node(node)

        # Cache
        self.__and_unique_node_cache[key_cache] = node

        return node.id

    def create_or_node(self, child_id_set: Set[int], decision_variable: Union[int, None] = None, use_unique_node_cache: bool = True) -> int:
        """
        Create a new OR node in the circuit.
        If some child's id does not exist in the circuit, raise an exception (NodeWithIDDoesNotExistInCircuitException).
        :param child_id_set: the set of child's id
        :param decision_variable: The decision variable. If the decision variable does not exist, None is expected.
        :param use_unique_node_cache: True if unique node caching can be used, otherwise False
        :return: the node's id
        """

        # No child was given -> constant leaf (FALSE)
        if not len(child_id_set):
            return self.create_constant_leaf(False)

        # Check if the node already exists in the cache
        key_cache = self.__generate_key_cache(child_id_set)
        if use_unique_node_cache and (key_cache in self.__or_unique_node_cache):
            return self.__or_unique_node_cache[key_cache].id

        child_node_set = set()
        for child_id in child_id_set:
            child_temp = self.get_node(child_id)

            # The child's id does not exist in the circuit
            if child_temp is None:
                raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(child_id), "trying to create an OR node with a nonexisting child")

            child_node_set.add(child_temp)

        node = OrInnerNode(child_node_set, self.__get_new_id(), decision_variable=decision_variable)
        self.__add_new_node(node)

        # Cache
        self.__or_unique_node_cache[key_cache] = node

        return node.id

    def create_decision_node(self, variable: int, true_node_id: int, false_node_id: int) -> int:
        """
        Create a new decision node in the circuit.
        (true_node_id AND variable) OR (false_node_id AND -variable)
        If true_node_id or false_node_id does not exist in the circuit, raise an exception (NodeWithIDDoesNotExistInCircuitException).
        :param variable: the decision variable
        :param true_node_id: the id of a node which appears with the variable in the AND node (true_node_id AND variable)
        :param false_node_id: the id of a node which appears with the negative variable in the AND node (false_node_id AND -variable)
        :return: the node's id
        """

        # One of the nodes does not exist in the circuit
        true_node_temp = self.get_node(true_node_id)
        false_node_temp = self.get_node(false_node_id)
        if true_node_temp is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(true_node_id), message_extension="decision node (true_node)")
        if false_node_temp is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(false_node_id), message_extension="decision node (false_node)")

        true_literal_leaf_id = self.create_literal_leaf(variable)
        false_literal_leaf_id = self.create_literal_leaf(-variable)

        true_and_node_id = self.create_and_node({true_node_id, true_literal_leaf_id})
        false_and_node_id = self.create_and_node({false_node_id, false_literal_leaf_id})
        or_node_id = self.create_or_node({true_and_node_id, false_and_node_id}, variable)

        return or_node_id

    def is_circuit_connected(self) -> bool:
        """
        Check if the circuit is connected.
        If the root of the circuit is not set, raise an exception (RootOfCircuitIsNotSetUpException).
        :return: True if the circuit is connected, otherwise False is returned
        """

        # Root of the circuit is not set
        if self.__root is None:
            raise c_exception.RootOfCircuitIsNotSetException()

        if self.real_number_of_nodes == self.number_of_nodes:
            return True

        return False

    def clear_comments(self) -> None:
        """
        Clear the comments of the circuit
        """

        self.set_comments("")

    def set_comments(self, new_comment: str) -> None:
        """
        Set the comments of the circuit
        :param new_comment: the new comment
        """

        self.__comments = new_comment

    def set_root(self, node_id: int) -> None:
        """
        Set the root of the circuit.
        If the node's ID does not exist in the circuit, raise an exception (NodeWithIDDoesNotExistInCircuitException).
        :param node_id: the node's ID
        """

        root_temp = self.get_node(node_id)

        # The node's id does not exist in the circuit
        if root_temp is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(node_id))

        self.__root = root_temp

        # Recheck the type of the circuit
        self.check_circuit_type()
        # Recompute the size of the circuit
        self.__compute_size_of_circuit()

    def check_circuit_type(self) -> None:
        """
        Check the circuit type.
        If the root of the circuit is not set, None is set.
        """

        # Root of the circuit is not set
        if self.__root is None:
            self.__circuit_type = None
            return

        # The circuit is only a list
        if isinstance(self.__root, LeafAbstract):
            self.__circuit_type = ct_enum.CircuitTypeEnum.SD_BDMC
            return

        # The root of the circuit is an inner node
        decomposable_temp = self.__root.decomposable_in_circuit
        deterministic_temp = self.__root.deterministic_in_circuit
        smoothness_temp = self.__root.smoothness_in_circuit

        if smoothness_temp:
            if decomposable_temp and deterministic_temp:
                self.__circuit_type = ct_enum.CircuitTypeEnum.SD_BDMC
            elif decomposable_temp and (not deterministic_temp):
                self.__circuit_type = ct_enum.CircuitTypeEnum.S_BDMC
            else:
                self.__circuit_type = ct_enum.CircuitTypeEnum.S_NNF
        else:
            if decomposable_temp and deterministic_temp:
                self.__circuit_type = ct_enum.CircuitTypeEnum.D_BDMC
            elif decomposable_temp and (not deterministic_temp):
                self.__circuit_type = ct_enum.CircuitTypeEnum.BDMC
            else:
                self.__circuit_type = ct_enum.CircuitTypeEnum.NNF

    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int],
                       use_caches: bool = True) -> bool:
        """
        Check if the circuit is satisfiable with the assumption set and existential quantification set
        If the assumption set and existential quantification set are not disjoint, raise an exception (AssumptionSetAndExistentialQuantificationSetAreNotDisjointException).
        If the root of the circuit is not set, raise an exception (RootOfCircuitIsNotSetUpException).
        If the existential quantification set contains a literal instead of variables, raise an exception
        (SetContainsLiteralsButOnlyVariablesAreAllowedException).
        Requirement: decomposability
        :param assumption_set: the assumption set
        :param exist_quantification_set: the existential quantification set
        :param use_caches: True if satisfiability can use the caches
        :return: True if the circuit is satisfiable with the assumption set and existential quantification set, otherwise False is returned
        """

        # Root of the circuit is not set
        if self.__root is None:
            raise c_exception.RootOfCircuitIsNotSetException()

        self.__check_assumption_set_and_exist_quantification_set(assumption_set, exist_quantification_set)

        return self.__root.is_satisfiable(assumption_set, exist_quantification_set, use_caches)

    def clause_entailment(self, clause: Set[int], exist_quantification_set: Set[int], use_caches: bool = True) -> bool:
        """
        Clause entailment
        Check if the clause is implied by the circuit
        Requirement: decomposability
        :param clause: the clause
        :param exist_quantification_set: the existential quantification set
        :param use_caches: True if clause entailment can use the caches
        :return:
        """

        assumption_set = set()
        for lit in clause:
            assumption_set.add(-lit)

        return not self.is_satisfiable(assumption_set, exist_quantification_set, use_caches)

    def model_counting(self, assumption_set: Set[int], exist_quantification_set: Set[int],
                       use_caches: bool = True) -> int:
        """
        Count the number of models with the assumption set and existential quantification set
        If the assumption set or existential quantification set is not valid, raise an exception
        (AssumptionSetAndExistentialQuantificationSetAreNotDisjointException, AssumptionSetContainsComplementLiteralsException).
        If the root of the circuit is not set, raise an exception (RootOfCircuitIsNotSetUpException).
        If the existential quantification set contains a literal instead of variables, raise an exception
        (SetContainsLiteralsButOnlyVariablesAreAllowedException).
        Requirement: decomposability, determinism, smooth
        :param assumption_set: the assumption set
        :param exist_quantification_set: the existential quantification set
        :param use_caches: True if model counting can use the caches
        :return: The number of models
        """

        # Root of the circuit is not set
        if self.__root is None:
            raise c_exception.RootOfCircuitIsNotSetException()

        self.__check_assumption_set_and_exist_quantification_set(assumption_set, exist_quantification_set)

        self.smooth()
        return self.__root.model_counting(assumption_set, exist_quantification_set, use_caches)

    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int],
                                    use_caches: bool = True) -> float:
        """
        Compute minimum default-cardinality of the circuit.
        If the root of the circuit is not set, raise an exception (RootOfCircuitIsNotSetUpException).
        Return infinity in case the circuit is unsatisfiable.
        If the observation set or default set is not valid, raise an exception
        (AssumptionSetAndExistentialQuantificationSetAreNotDisjointException, AssumptionSetContainsComplementLiteralsException).
        An empty default set corresponds to all variables except ones that appear in the observation set.
        Requirement: decomposability
        :param observation_set: the set of literals representing observations
        :param default_set: the set of variables representing defaults (we assume that all of these defaults are true)
        :param use_caches: True if minimum default-cardinality can use the caches
        :return: minimum default-cardinality
        """

        # Root of the circuit is not set
        if self.__root is None:
            raise c_exception.RootOfCircuitIsNotSetException()

        # The default set is empty
        if not default_set:
            default_set = set()
            variable_set_temp = self.__root._get_variable_in_circuit_set()
            for variable in variable_set_temp:
                if (variable not in observation_set) and (-variable not in observation_set):
                    default_set.add(variable)

        self.__check_assumption_set_and_exist_quantification_set(observation_set, default_set, False)

        return self.__root.minimum_default_cardinality(observation_set, default_set, use_caches)

    def smooth(self) -> None:
        """
        Smooth the circuit
        """

        # Root of the circuit is not set or the root is a leaf
        if (self.__root is None) or (isinstance(self.__root, LeafAbstract)):
            return

        # The circuit is already smooth
        if self.__root.smoothness_in_circuit:
            return

        node_in_circuit_set = self.__root._get_node_in_circuit_set()
        for node in node_in_circuit_set:
            # The node is not an inner node
            if not isinstance(node, OrInnerNode):
                continue

            # The node is smooth
            if node.smoothness:
                continue

            union_variable_set = node._get_variable_in_circuit_set()
            child_set = node._get_child_set(True)
            for child in child_set:
                difference_set = union_variable_set.difference(child._get_variable_in_circuit_set())

                # The difference set is not empty
                if difference_set:
                    and_node = self.__smooth_create_and_node(child.id, difference_set)

                    self.__remove_edge(node, child, False)
                    self.__add_edge(node, and_node, False)

        # Update properties for all inner nodes in the circuit
        leaf_set = set()
        inner_node_set = set()

        inner_node_set_temp = set()
        for id in self.__id_node_dictionary:
            node_temp = self.get_node(id)
            if isinstance(node_temp, LeafAbstract):
                leaf_set.add(node_temp)
                inner_node_set_temp.update(node_temp._get_parent_set())

        visited_inner_node_set = leaf_set

        # Get only those inner nodes whose children are only leaves
        for inner_node in inner_node_set_temp:
            child_set = inner_node._get_child_set()

            if len(child_set.intersection(leaf_set)) == len(child_set):
                inner_node_set.add(inner_node)

        while inner_node_set:
            inner_node_set_temp = set()

            for inner_node in inner_node_set:
                inner_node._update(False)
                visited_inner_node_set.add(inner_node)

                # Add parents whose all children are visited nodes
                parent_set = inner_node._get_parent_set()
                for parent in parent_set:
                    child_set = parent._get_child_set()
                    if len(child_set.intersection(visited_inner_node_set)) == len(child_set):
                        inner_node_set_temp.add(parent)

            inner_node_set = inner_node_set_temp

        # Recheck the type of the circuit
        self.check_circuit_type()
        # Recompute the size of the circuit
        self.__compute_size_of_circuit()

    def topological_ordering(self) -> List[int]:
        """
        Return a topological ordering of the circuit.
        If the root of the circuit is not set, raise an exception (RootOfCircuitIsNotSetUpException).
        :return: a list (of identifiers) which corresponds to a topological ordering
        """

        # Root of the circuit is not set
        if self.__root is None:
            raise c_exception.RootOfCircuitIsNotSetException()

        return self.__topological_ordering_recursion(self.__root.id, [])

    def is_decomposable(self) -> Union[bool, None]:
        """
        Is the circuit decomposable?
        If the root of the circuit is not set, None is returned.
        :return: true if the circuit is decomposable, otherwise False is returned
        """

        # Root of the circuit is not set
        if self.__root is None:
            return None

        # Root of the circuit is a leaf
        if isinstance(self.__root, LeafAbstract):
            return True

        return self.__root.decomposable_in_circuit

    def is_deterministic(self) -> Union[bool, None]:
        """
        Is the circuit deterministic?
        If the root of the circuit is not set, None is returned.
        :return: true if the circuit is deterministic, otherwise False is returned
        """

        # Root of the circuit is not set
        if self.__root is None:
            return None

        # Root of the circuit is a leaf
        if isinstance(self.__root, LeafAbstract):
            return True

        return self.__root.deterministic_in_circuit

    def is_smooth(self) -> Union[bool, None]:
        """
        Is the circuit smooth?
        If the root of the circuit is not set, None is returned.
        :return: true if the circuit is smooth, otherwise False is returned
        """

        # Root of the circuit is not set
        if self.__root is None:
            return None

        # Root of the circuit is a leaf
        if isinstance(self.__root, LeafAbstract):
            return True

        return self.__root.smoothness_in_circuit

    def add_edge(self, from_id_node: int, to_id_node: int) -> None:
        """
        Add an oriented edge (from_id_node -> to_id_node) in the circuit.
        If the oriented edge already exists in the circuit, nothing happens.
        If the from_id_node is not an inner node, raise an exception (SomethingWrongException).
        If one of the nodes does not exist in the circuit, raise an exception (NodeWithIDDoesNotExistInCircuitException).
        If a cycle is detected, raise an exception (CycleWasDetectedException).
        :param from_id_node: new to_id_node's parent
        :param to_id_node: new from_id_node's child
        """

        # One of the nodes does not exist in the circuit
        from_node = self.get_node(from_id_node)
        to_node = self.get_node(to_id_node)
        if from_node is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(from_id_node), message_extension="add_edge (from_id_node)")
        if to_node is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(to_id_node), message_extension="add_edge (to_id_node)")

        # from_node is not an inner node
        if not isinstance(from_node, InnerNodeAbstract):
            raise c_exception.SomethingWrongException(f"trying to add an edge from the node ({from_id_node}) which is not an inner node")

        # The edge already exists
        if to_id_node in from_node.get_child_id_list():
            return

        self.__add_edge(from_node, to_node)

        # Recheck the type of the circuit
        self.check_circuit_type()
        # Recompute the size of the circuit
        self.__compute_size_of_circuit()
    # endregion

    # region Magic method
    def __str__(self):
        try:
            topological_ordering = self.topological_ordering()
            id_to_dictionary = dict()
            for to, id in enumerate(topological_ordering):
                id_to_dictionary[id] = to

            # Comment line
            string = "\n".join((f"C Name: {self.circuit_name}",
                                f"C Type: {str(self.circuit_type.name)}",
                                f"C Decomposability: {self.is_decomposable()}",
                                f"C Determinism: {self.is_deterministic()}",
                                f"C Smoothness: {self.is_smooth()}"))

            if isinstance(self.__root, InnerNodeAbstract):
                for nt in nt_enum.NodeTypeEnum:
                    string = "\n".join((string,
                                        f"C {nt.name}: {self.__root.get_number_of_occurrences_node_type_in_circuit_counter_dict(nt)}"))

            comments_temp = self.comments.replace("\n", ", ")
            string = "\n".join((string,
                                "C",
                                f"C {comments_temp}"))

            # N line
            string = "\n".join((string, f"nnf {str(self.real_number_of_nodes)} {str(self.size)} {str(self.number_of_variables)}"))

            # Node line
            for node_id in topological_ordering:
                node = self.get_node(node_id)

                # Constant leaf
                if isinstance(node, ConstantLeaf):
                    # True
                    if node.constant:
                        string = "\n".join((string, "A 0"))
                    # False
                    else:
                        string = "\n".join((string, "O 0 0"))

                    continue

                # Literal leaf
                if isinstance(node, LiteralLeaf):
                    string = "\n".join((string, f"L {node.literal}"))
                    continue

                # AND node
                if isinstance(node, AndInnerNode):
                    child_id_list = node.get_child_id_list()
                    child_to_list = []

                    for child_id in child_id_list:
                        child_to_list.append(id_to_dictionary[child_id])

                    child_to_list.sort()

                    string_temp = " ".join(map(str, child_to_list))
                    string = "\n".join((string, f"A {len(child_to_list)} {string_temp}"))
                    continue

                # OR node
                if isinstance(node, OrInnerNode):
                    child_id_list = node.get_child_id_list()
                    child_to_list = []

                    for child_id in child_id_list:
                        child_to_list.append(id_to_dictionary[child_id])

                    child_to_list.sort()

                    j = 0 if node.decision_variable is None else node.decision_variable

                    string_temp = " ".join(map(str, child_to_list))
                    string = "\n".join((string, f"O {j} {len(child_to_list)} {string_temp}"))
                    continue

                raise c_exception.SomethingWrongException(
                    f"this type of node ({type(node)}) is not implemented in ToString (circuit)")

            return string
        except c_exception.RootOfCircuitIsNotSetException:
            warnings.warn("ToString (circuit) returned an empty string because the root of the circuit is not set!")
            return ""

    def __repr__(self):
        comments_temp = self.comments.replace("\n", ", ")
        string_temp = " ".join((f"Name: {self.circuit_name}",
                                f"Number of nodes: {str(self.number_of_nodes)}",
                                f"Comments: {comments_temp}"))

        if self.__root is not None:
            string_temp = " ".join((string_temp,
                                    f"Root: {self.root_id}",
                                    f"Number of variables: {str(self.number_of_variables)}",
                                    f"Real number of nodes: {str(self.real_number_of_nodes)}",
                                    f"Size: {str(self.size)}",
                                    f"Connected: {str(self.is_circuit_connected())}"))

        # The nodes in the circuit
        id_node_sorted_dictionary_temp = SortedDict(self.__id_node_dictionary)
        for key in iter(id_node_sorted_dictionary_temp):
            string_temp = "\n".join((string_temp, repr(self.__id_node_dictionary[key])))

        return string_temp
    # endregion

    # region Property
    @property
    def circuit_name(self):
        return self.__circuit_name

    @property
    def number_of_nodes(self):
        return len(self.__id_node_dictionary)

    @property
    def real_number_of_nodes(self):
        if self.__root is None:
            return 0

        return self.__root.number_of_nodes

    @property
    def number_of_variables(self):
        if self.__root is None:
            return 0

        return self.__root.number_of_variables

    @property
    def size(self):
        return self.__size

    @property
    def comments(self):
        return self.__comments

    @property
    def circuit_type(self):
        return self.__circuit_type

    @property
    def root_id(self):
        if self.__root is None:
            return None

        return self.__root.id
    # endregion
