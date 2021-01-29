# Import
from typing import Union
from sortedcontainers import SortedDict
from circuit.node.node_abstract import NodeAbstract
from circuit.node.leaf.literal_leaf import LiteralLeaf
from circuit.node.leaf.constant_leaf import ConstantLeaf
from circuit.node.inner_node.or_inner_node import OrInnerNode
from circuit.node.inner_node.and_inner_node import AndInnerNode

# Import exception
import exception.circuit_exception as c_exception

# Import enum
import circuit.circuit_type_enum as ct_enum

# TODO NNF parser (save / load)
# TODO circuit test - files (read, circuit)
# TODO is_satisfiable
# TODO root
# TODO set comments
# TODO connectivity


class Circuit:
    """
    Circuit representation
    """

    """
    private int id_counter
    private str comments
    private Dict<int, NodeAbstract> id_node_dictionary      # key: id, value: node
    private Dict<int, NodeAbstract> literal_node_dictionary # key: literal, value: node
    private List<NodeAbstract> constant_node_list           # [False: node, True: node]
    
    private NodeAbstract root
    """

    def __init__(self, dimacs_nnf_file_path: str = None):
        # region Initialization
        self.__id_counter: int = 0
        self.__comments: str = ""

        self.__id_node_dictionary: dict[int, NodeAbstract] = dict()                 # initialization
        self.__literal_node_dictionary: dict[int, NodeAbstract] = dict()            # initialization
        self.__constant_node_list: list[Union[NodeAbstract, None]] = [None, None]   # initialization

        self.__root: Union[NodeAbstract, None] = None
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
            v = None    # the number of nodes
            e = None    # the number of edges
            n = None    # the number of variables
            is_n_line_defined = False

            for line_id, line in enumerate(file.readlines()):
                # The line is empty
                if not line.strip():
                    continue

                # Comment line
                if line.startswith("c") or line.startswith("C"):
                    if not self.__comments:  # First comment
                        self.__comments = line[1:].strip()
                    else:
                        self.__comments = "\n".join((self.__comments, line[1:].strip()))
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
                        raise c_exception.InvalidDimacsNnfFormatException("nnf line has an invalid format. Valid format is 'nnf number_of_nodes number_of_edges number_of_variables'")

                    # Parse the parameters
                    try:
                        v = int(line_array_temp[1])
                        e = int(line_array_temp[2])
                        n = int(line_array_temp[3])
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the number of nodes ({line_array_temp[1]}), the number of edges ({line_array_temp[2]}) or the number of variables ({line_array_temp[3]}) is not an integer")
                    continue

                # N line has not been mentioned
                if not is_n_line_defined:
                    raise c_exception.NLineIsNotMentionedException()

                # Node line
                # Constant leaf (TRUE)
                if line.strip() == "A 0":
                    root_id = self.create_constant_leaf(True)
                    continue

                # Constant leaf (FALSE)
                if line.strip() == "O 0 0" or line.strip() == "O 0":
                    root_id = self.create_constant_leaf(False)
                    continue

                # Literal leaf
                if line.startswith("L"):
                    line_array_temp = line.split()
                    # Invalid line
                    if len(line_array_temp) != 2:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the literal leaf ({line}) defined on line {line_id + 1} has an invalid number of parameters")

                    # Parse the literal
                    try:
                        literal_temp = int(line_array_temp[1])
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the literal ({line_array_temp[1]}) mentioned on line {line_id + 1} in the leaf node is not an integer")

                    root_id = self.create_literal_leaf(literal_temp)
                    continue

                # AND node
                if line.startswith("A"):
                    line_array_temp = line.split()
                    # Invalid line
                    if len(line_array_temp) < 3:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the AND node ({line}) defined on line {line_id + 1} has an invalid number of parameters")

                    # Parse the IDs
                    child_id_set_temp = set()
                    try:
                        c_temp = int(line_array_temp[1])

                        for i in range(2, len(line_array_temp)):
                            id_temp = int(line_array_temp[i])

                            # Check if the node with the id has been already declared
                            node_child_temp = self.get_node(id_temp)
                            if node_child_temp is None:
                                raise c_exception.InvalidDimacsNnfFormatException(f"the node (child) with the id ({id_temp}) mentioned on line {line_id + 1} in the AND node has not been seen yet")

                            child_id_set_temp.add(id_temp)

                        # The c value and the number of children don't correspond
                        if len(child_id_set_temp) != c_temp:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the c value ({c_temp}) and the number of children ({len(child_id_set_temp)}) mentioned on line {line_id + 1} in the AND node don't correspond")
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(f"some id ({line}) mentioned on line {line_id + 1} in the AND node is not an integer")

                    root_id = self.create_and_node(child_id_set_temp)
                    continue

                # OR node
                if line.startswith("O"):
                    line_array_temp = line.split()
                    # Invalid line
                    if len(line_array_temp) < 4:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the OR node ({line}) defined on line {line_id + 1} has an invalid number of parameters")

                    # Parse the IDs
                    child_id_set_temp = set()
                    try:
                        j_temp = int(line_array_temp[1])
                        c_temp = int(line_array_temp[2])

                        for i in range(3, len(line_array_temp)):
                            id_temp = int(line_array_temp[i])

                            # Check if the node with the id has been already declared
                            node_child_temp = self.get_node(id_temp)
                            if node_child_temp is None:
                                raise c_exception.InvalidDimacsNnfFormatException(f"the node (child) with the id ({id_temp}) mentioned on line {line_id + 1} in the OR node has not been seen yet")

                            child_id_set_temp.add(id_temp)

                        # The c value and the number of children don't correspond
                        if len(child_id_set_temp) != c_temp:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the c value ({c_temp}) and the number of children ({len(child_id_set_temp)}) mentioned on line {line_id + 1} in the OR node don't correspond")
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(f"some id ({line}) mentioned on line {line_id + 1} in the OR node is not an integer")

                    root_id = self.create_or_node(child_id_set_temp, j_temp)
                    continue

        # The file does not contain any node
        if not len(self.__id_node_dictionary):
            raise c_exception.InvalidDimacsNnfFormatException("file does not contain any node")

        if root_id is None:
            raise c_exception.SomethingWrongException("root was not set")

        self.__root = self.get_node(root_id)

        # Check v, e, n
        if v != self.number_of_nodes:
            raise c_exception.SomethingWrongException(f"the number of nodes in the circuit ({self.number_of_nodes}) differs from the v value ({v})")
        if e != self.size:
            raise c_exception.SomethingWrongException(f"the number of edges in the circuit ({self.size}) differs from the e value ({e})")
        if n != self.number_of_variables:
            raise c_exception.SomethingWrongException(f"the number of variables in the circuit ({self.number_of_variables}) differs from the n value ({n})")

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
        Add the node to the circuit. If some node already exists in the circuit with the same ID, raise an exception (NodeWithSameIDAlreadyExistsInCircuitException).
        :param node: the node
        """

        id_temp = node.id

        # There is already some node with the same ID
        if self.node_exist(node):
            c_exception.NodeWithSameIDAlreadyExistsInCircuitException(str(node))

        self.__id_node_dictionary[id_temp] = node
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

    def create_constant_leaf(self, constant: bool) -> int:
        """
        Create a new constant leaf in the circuit.
        If the node already exists in the circuit, then new node will not be created, and the existed node will be used instead.
        :param constant: the value of the constant leaf
        :return: the node's id
        """

        # The node already exists in the circuit
        if self.__constant_node_list[int(constant)] is not None:
            return self.__constant_node_list[int(constant)].id

        node = ConstantLeaf(constant, self.__get_new_id())
        self.__add_new_node(node)
        self.__constant_node_list[int(constant)] = node

        return node.id

    def create_literal_leaf(self, literal: int) -> int:
        """
        Create a new literal leaf in the circuit.
        If the node already exists in the circuit, then new node will not be created, and the existed node will be used instead.
        :param literal: the value of the literal leaf
        :return: the node's id
        """

        # The node already exists in the circuit
        if literal in self.__literal_node_dictionary:
            return self.__literal_node_dictionary[literal].id

        node = LiteralLeaf(literal, self.__get_new_id())
        self.__add_new_node(node)
        self.__literal_node_dictionary[literal] = node

        return node.id

    def create_and_node(self, child_id_set: set[int]) -> int:
        """
        Create a new AND node in the circuit.
        If some child's id does not exist in the circuit, raise an exception (NodeWithIDDoesNotExistInCircuitException).
        :param child_id_set: the set of child's id
        :return: the node's id
        """

        # No child was given -> constant leaf (TRUE)
        if not len(child_id_set):
            return self.create_constant_leaf(True)

        child_node_set = set()
        for child_id in child_id_set:
            child_temp = self.get_node(child_id)

            # The child's id does not exist in the circuit
            if child_temp is None:
                raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(child_id), "trying to create an AND node with a nonexisting child")

            child_node_set.add(child_temp)

        node = AndInnerNode(child_node_set, self.__get_new_id())
        self.__add_new_node(node)

        return node.id

    def create_or_node(self, child_id_set: set[int], decision_variable: Union[int, None] = None) -> int:
        """
        Create a new OR node in the circuit.
        If some child's id does not exist in the circuit, raise an exception (NodeWithIDDoesNotExistInCircuitException).
        :param child_id_set: the set of child's id
        :param decision_variable: The decision variable. If the decision variable does not exist, None is expected.
        :return: the node's id
        """

        # No child was given -> constant leaf (FALSE)
        if not len(child_id_set):
            return self.create_constant_leaf(False)

        child_node_set = set()
        for child_id in child_id_set:
            child_temp = self.get_node(child_id)

            # The child's id does not exist in the circuit
            if child_temp is None:
                raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(child_id), "trying to create an OR node with a nonexisting child")

            child_node_set.add(child_temp)

        node = OrInnerNode(child_node_set, self.__get_new_id(), decision_variable=decision_variable)
        self.__add_new_node(node)

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
    # endregion

    # region Magic method
    def __repr__(self):
        string_temp = " ".join((f"Number of nodes: {str(self.number_of_nodes)}",
                                f"Comments: {self.__comments}"))

        if self.__root is not None:
            string_temp = " ".join((string_temp,
                                    f"Root: {self.__root}",
                                    f"Number of variables: {str(self.number_of_variables)}",
                                    f"Real number of nodes: {str(self.real_number_of_nodes)}",
                                    f"Size: {str(self.size)}"))

        # The nodes in the circuit
        id_node_sorted_dictionary_temp = SortedDict(self.__id_node_dictionary)
        for key in iter(id_node_sorted_dictionary_temp):
            string_temp = "\n".join((string_temp, repr(self.__id_node_dictionary[key])))

        return string_temp
    # endregion

    # region Property
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
        if self.__root is None:
            return 0

        return self.__root.size
    # endregion
