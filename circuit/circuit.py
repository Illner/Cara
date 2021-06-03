# Import
import warnings
from io import StringIO
from formula.cnf import Cnf
from sortedcontainers import SortedDict
from other.sorted_list import SortedList
from typing import Set, Dict, List, Union

from formula.pysat_2_cnf import PySat2Cnf
from formula.pysat_horn_cnf import PySatHornCnf

from circuit.node.node_abstract import NodeAbstract
from circuit.node.leaf.two_cnf_leaf import TwoCnfLeaf
from circuit.node.leaf.literal_leaf import LiteralLeaf
from circuit.node.leaf.constant_leaf import ConstantLeaf
from circuit.node.leaf.leaf_abstract import LeafAbstract
from circuit.node.inner_node.or_inner_node import OrInnerNode
from circuit.node.inner_node.and_inner_node import AndInnerNode
from circuit.node.inner_node.mapping_inner_node import MappingInnerNode
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract
from circuit.node.leaf.renamable_horn_cnf_leaf import RenamableHornCnfLeaf

# Import exception
import exception.formula.formula_exception as f_exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.circuit_type_enum as ct_enum
import circuit.node.node_type_enum as nt_enum


class Circuit:
    """
    Circuit representation
    """

    """
    Private int size                                                        # the number of edges in the circuit + the sizes of all leaves in the circuit
    Private str comments
    Private int id_counter
    Private str circuit_name
    Private NodeAbstract root
    Private CircuitTypeEnum circuit_type
    
    Private Dict<int, NodeAbstract> id_node_dictionary                      # key: an identifier, value: a node
    Private Dict<NodeTypeEnum, int> node_type_in_circuit_counter_dictionary

    Private Dict<int, int> literal_unique_node_cache                        # key: a literal, value: an identifier of the node
    Private List<int> constant_unique_node_cache                            # [an identifier of the FALSE leaf, an identifier of the TRUE leaf]
    Private Dict<str, int> and_unique_node_cache                            # key: hash, value: an identifier of the node
    Private Dict<str, int> or_unique_node_cache                             # key: hash, value: an identifier of the node
    """

    def __init__(self, dimacs_nnf_file_path: Union[str, None] = None, circuit_name: str = "Circuit"):
        self.__comments: str = ""
        self.__id_counter: int = 0
        self.__size: Union[int, None] = None
        self.__circuit_name: str = circuit_name
        self.__root: Union[NodeAbstract, None] = None
        self.__circuit_type: Union[ct_enum.CircuitTypeEnum, None] = None

        self.__id_node_dictionary: Dict[int, NodeAbstract] = dict()

        self.__node_type_in_circuit_counter_dictionary: Dict[nt_enum.NodeTypeEnum, int] = dict()
        for node_type in nt_enum.NodeTypeEnum:
            self.__node_type_in_circuit_counter_dictionary[node_type] = 0

        self.__literal_unique_node_cache: Dict[int, int] = dict()
        self.__constant_unique_node_cache: List[Union[int, None]] = [None, None]
        self.__and_unique_node_cache: Dict[str, int] = dict()
        self.__or_unique_node_cache: Dict[str, int] = dict()

        # A file with the circuit was given
        if dimacs_nnf_file_path is not None:
            self.__create_nnf(dimacs_nnf_file_path)

    # region Private method
    def __create_nnf(self, dimacs_nnf_file_path: str) -> None:
        """
        Convert the circuit in the file into our structure
        :param dimacs_nnf_file_path: a file that is in the DIMACS NNF format
        :return: None
        :raises InvalidDimacsNnfFormatException, NLineIsNotMentionedException: if the DIMACS NNF format in the file is invalid
        """

        root_id = None

        with open(dimacs_nnf_file_path, "r", encoding="utf-8") as file:
            line_id = 0

            v = None  # the number of nodes
            e = None  # the number of edges
            n = None  # the number of variables
            is_n_line_defined = False

            while True:
                line = file.readline()
                line_id += 1

                # End of the file
                if not line:
                    break

                line = line.strip()

                # The line is empty
                if not line:
                    continue

                # Comment line
                if line.startswith("C") or line.startswith("c"):
                    if not self.__comments:     # First comment
                        self.__comments = line[1:].strip()
                    else:
                        self.__comments = "\n".join((self.__comments, line[1:].strip()))
                    continue

                # End of the file (optional)
                if line.startswith("%"):
                    break

                # N line
                if line.startswith("NNF") or line.startswith("nnf"):
                    is_n_line_defined = True
                    line_array_temp = line.split()

                    # N line has an invalid format
                    if len(line_array_temp) != 4:  # nnf number_of_nodes number_of_edges number_of_variables
                        raise c_exception.InvalidDimacsNnfFormatException("nnf line has an invalid format - the valid format is 'nnf number_of_nodes number_of_edges number_of_variables'")

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
                if (line == "A 0") or (line == "a 0"):
                    root_id = self.create_constant_leaf(constant=True,
                                                        use_unique_node_cache=False)
                    continue

                # Constant leaf (FALSE)
                if (line == "O 0 0") or (line == "O 0") or (line == "o 0 0") or (line == "o 0"):
                    root_id = self.create_constant_leaf(constant=False,
                                                        use_unique_node_cache=False)
                    continue

                # Literal leaf
                if line.startswith("L") or line.startswith("l"):
                    line_array_temp = line.split()

                    # Invalid line
                    if len(line_array_temp) != 2:   # L number
                        raise c_exception.InvalidDimacsNnfFormatException(f"the literal leaf ({line}) defined at line {line_id} has an invalid number of parameters")

                    # Parse the literal
                    try:
                        literal_temp = int(line_array_temp[1])
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the literal ({line_array_temp[1]}) mentioned at line {line_id} in the leaf node is not an integer")

                    root_id = self.create_literal_leaf(literal=literal_temp,
                                                       use_unique_node_cache=False)
                    continue

                # AND node
                if line.startswith("A") or line.startswith("a"):
                    line_array_temp = line.split()

                    # Invalid line
                    if len(line_array_temp) < 3:    # A number_of_children ...
                        raise c_exception.InvalidDimacsNnfFormatException(f"the AND node ({line}) defined at line {line_id} has an invalid number of parameters")

                    # Parse the IDs
                    child_id_set_temp = set()
                    try:
                        c_temp = int(line_array_temp[1])
                        if c_temp < 0:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the c value ({c_temp}) mentioned at line {line_id} in the AND node is negative")

                        for i in range(2, len(line_array_temp)):
                            id_temp = int(line_array_temp[i])

                            # Check if the node with the id has been already declared
                            if not self.node_id_exist(id_temp):
                                raise c_exception.InvalidDimacsNnfFormatException(f"the node (child) with the id ({id_temp}) mentioned at line {line_id} in the AND node has not been seen yet")

                            child_id_set_temp.add(id_temp)

                        # The c value and the number of children don't correspond
                        if len(child_id_set_temp) != c_temp:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the c value ({c_temp}) and the number of children ({len(child_id_set_temp)}) mentioned at line {line_id} in the AND node don't correspond")
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the c value or some id of a node ({line}) mentioned at line {line_id} in the AND node is not an integer")

                    root_id = self.create_and_node(child_id_set=child_id_set_temp,
                                                   use_unique_node_cache=False)
                    continue

                # OR node
                if line.startswith("O") or line.startswith("o"):
                    line_array_temp = line.split()

                    # Invalid line
                    if len(line_array_temp) < 4:    # O decision_variable number_of_children ...
                        raise c_exception.InvalidDimacsNnfFormatException(f"the OR node ({line}) defined at line {line_id} has an invalid number of parameters")

                    # Parse the IDs
                    child_id_set_temp = set()
                    try:
                        j_temp = int(line_array_temp[1])
                        if (j_temp < 0) or (j_temp > n):
                            raise c_exception.InvalidDimacsNnfFormatException(f"the j value ({j_temp}) mentioned at line {line_id} in the OR node is not a valid variable")

                        c_temp = int(line_array_temp[2])
                        if c_temp < 0:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the c value ({c_temp}) mentioned at line {line_id} in the OR node is negative")

                        j_temp = None if j_temp == 0 else j_temp

                        for i in range(3, len(line_array_temp)):
                            id_temp = int(line_array_temp[i])

                            # Check if the node with the id has been already declared
                            if not self.node_id_exist(id_temp):
                                raise c_exception.InvalidDimacsNnfFormatException(f"the node (child) with the id ({id_temp}) mentioned at line {line_id} in the OR node has not been seen yet")

                            child_id_set_temp.add(id_temp)

                        # The c value and the number of children don't correspond
                        if len(child_id_set_temp) != c_temp:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the c value ({c_temp}) and the number of children ({len(child_id_set_temp)}) mentioned at line {line_id} in the OR node don't correspond")
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the c value, j value or some id of a node ({line}) mentioned at line {line_id} in the OR node is not an integer")

                    root_id = self.create_or_node(child_id_set=child_id_set_temp,
                                                  decision_variable=j_temp,
                                                  use_unique_node_cache=False)
                    continue

                # Mapping node
                if line.startswith("M") or line.startswith("m"):
                    line_array_temp = line.split()

                    # Invalid line
                    if len(line_array_temp) < 5:    # M child_id number_of_variables ...
                        raise c_exception.InvalidDimacsNnfFormatException(f"the mapping node ({line}) defined at line {line_id} has an invalid number of parameters")

                    # Parse the child and the number of variables
                    try:
                        child_id_temp = int(line_array_temp[1])
                        number_of_variables_temp = int(line_array_temp[2])

                        # Check if the child has been already declared
                        if not self.node_id_exist(child_id_temp):
                            raise c_exception.InvalidDimacsNnfFormatException(f"the node (child) with the id ({child_id_temp}) mentioned at line {line_id} in the mapping node has not been seen yet")
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the child's id or the number of variables in the mapping ({line}) mentioned at line {line_id} in the mapping node is not an integer")

                    # The mapping does not contain all variables
                    if len(line_array_temp) != (2 * number_of_variables_temp + 3):
                        raise c_exception.InvalidDimacsNnfFormatException(f"the number of variables ({number_of_variables_temp}) and the number of variables in the mapping ({(len(line_array_temp) - 3) // 2}) are different at line {line_id} in the mapping node")

                    # Parse the mapping
                    variable_id_mapping_id_dictionary_temp: Dict[int, int] = dict()
                    mapping_id_variable_id_dictionary_temp: Dict[int, int] = dict()
                    try:
                        for i in range(0, 2 * number_of_variables_temp, 2):
                            var_temp = int(line_array_temp[3 + i])
                            var_map_temp = int(line_array_temp[3 + i + 1])

                            # The (mapping) variable is negative
                            if var_temp < 0:
                                raise c_exception.InvalidDimacsNnfFormatException(f"the variable ({var_temp}) in the mapping mentioned at line {line_id} in the mapping node is negative")
                            if var_map_temp < 0:
                                raise c_exception.InvalidDimacsNnfFormatException(f"the mapped variable ({var_map_temp}) in the mapping mentioned at line {line_id} in the mapping node is negative")

                            variable_id_mapping_id_dictionary_temp[var_temp] = var_map_temp
                            mapping_id_variable_id_dictionary_temp[var_map_temp] = var_temp
                    except ValueError:
                        raise c_exception.InvalidDimacsNnfFormatException(f"some variable in the mapping ({line}) mentioned at line {line_id} in the mapping node is not an integer")

                    root_id = self.create_mapping_node(child_id=child_id_temp,
                                                       variable_id_mapping_id_dictionary_cache=variable_id_mapping_id_dictionary_temp,
                                                       mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary_temp,
                                                       composition_needed=False)
                    continue

                # 2-CNF or renamable Horn CNF leaf
                if line.startswith("T") or line.startswith("t") or \
                   line.startswith("R") or line.startswith("r"):

                    # 2-CNF leaf
                    if line.startswith("T") or line.startswith("t"):
                        node_type_temp = nt_enum.NodeTypeEnum.TWO_CNF
                    # Renamable Horn CNF leaf
                    else:
                        node_type_temp = nt_enum.NodeTypeEnum.RENAMABLE_HORN_CNF

                    line_array_temp = line.split()

                    # Invalid line
                    if len(line_array_temp) < 2:    # T/R dimacs_size
                        raise c_exception.InvalidDimacsNnfFormatException(f"the {node_type_temp.name} leaf ({line}) defined at line {line_id} has an invalid number of parameters")

                    # Version without mapping
                    if len(line_array_temp) == 2:
                        use_mapping_temp = False
                    # Version with mapping
                    else:
                        use_mapping_temp = True

                    # Parse the size of DIMACS CNF and the number of variables
                    try:
                        size_of_dimacs_cnf_temp = int(line_array_temp[1])

                        if use_mapping_temp:
                            number_of_variables_temp = int(line_array_temp[2])
                    except ValueError:
                        if use_mapping_temp:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the size of DIMACS CNF ({line_array_temp[1]}) or the number of variables ({line_array_temp[2]}) mentioned at line {line_id} in the {node_type_temp.name} leaf is not an integer")
                        else:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the size of DIMACS CNF ({line_array_temp[1]}) mentioned at line {line_id} in the {node_type_temp.name} leaf is not an integer")

                    # The mapping does not contain all variables
                    if use_mapping_temp and (len(line_array_temp) != (3 + number_of_variables_temp)):
                        raise c_exception.InvalidDimacsNnfFormatException(f"the number of variables ({number_of_variables_temp}) and the number of variables in the mapping ({len(line_array_temp) - 3}) are different at line {line_id} in the {node_type_temp.name} leaf")

                    # Parse the mapping
                    variable_mapping_temp: Dict[int, int] = dict()
                    if use_mapping_temp:
                        try:
                            for i in range(number_of_variables_temp):
                                var_temp = int(line_array_temp[3 + i])

                                # The variable is negative
                                if var_temp < 0:
                                    raise c_exception.InvalidDimacsNnfFormatException(f"the variable ({var_temp}) in the mapping mentioned at line {line_id} in the {node_type_temp.name} leaf is negative")

                                variable_mapping_temp[i + 1] = var_temp
                        except ValueError:
                            raise c_exception.InvalidDimacsNnfFormatException(f"some variable in the mapping ({line}) mentioned at line {line_id} in the {node_type_temp.name} leaf is not an integer")

                    dimacs_cnf_temp = ""
                    for _ in range(size_of_dimacs_cnf_temp):
                        dimacs_cnf_temp = "".join((dimacs_cnf_temp, file.readline()))

                    io_temp = StringIO(initial_value=dimacs_cnf_temp)
                    try:
                        cnf_temp = Cnf(dimacs_cnf_source=io_temp,
                                       starting_line_id=line_id,
                                       variable_mapping=variable_mapping_temp)
                    except f_exception.FormulaException as err:
                        raise c_exception.InvalidDimacsNnfFormatException(f"the formula mentioned at line {line_id} has an invalid DIMACS format ({err})")

                    # 2-CNF leaf
                    if node_type_temp == nt_enum.NodeTypeEnum.TWO_CNF:
                        try:
                            two_cnf_temp = cnf_temp.get_incidence_graph().convert_to_2_cnf()

                            root_id = self.create_2_cnf_leaf(two_cnf=two_cnf_temp)
                        except f_exception.FormulaIsNot2CnfException:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the formula mentioned at line {line_id} in the {node_type_temp.name} leaf is not 2-CNF")

                    # Renamable Horn CNF leaf
                    else:
                        try:
                            cnf_temp.get_incidence_graph().initialize_renamable_horn_formula_recognition()
                            renaming_function_temp = cnf_temp.get_incidence_graph().is_renamable_horn_formula()
                            horn_cnf_temp = cnf_temp.get_incidence_graph().convert_to_horn_cnf(renaming_function_temp)

                            root_id = self.create_renamable_horn_cnf_leaf(renamable_horn_cnf=horn_cnf_temp,
                                                                          renaming_function=renaming_function_temp)
                        except f_exception.FormulaIsNotHornException:
                            raise c_exception.InvalidDimacsNnfFormatException(f"the formula mentioned at line {line_id} in the {node_type_temp.name} leaf is not a renamable Horn formula")

                    line_id += size_of_dimacs_cnf_temp
                    continue

                raise c_exception.InvalidDimacsNnfFormatException(f"the line ({line_id}) starts with an invalid char ({line})")

        # The file does not contain any node
        if not len(self.__id_node_dictionary):
            raise c_exception.InvalidDimacsNnfFormatException("the file does not contain any node")

        if root_id is None:
            raise c_exception.SomethingWrongException("the root has not been set")

        self.set_root(root_id)

        # Check v, e, n
        if v != self.number_of_nodes:
            warning_temp = f"The number of nodes in the circuit ({self.number_of_nodes}) differs from the v value ({v})!"
            warnings.warn(warning_temp)
        if e != self.size:
            warning_temp = f"The number of edges in the circuit ({self.size}) differs from the e value ({e})!"
            warnings.warn(warning_temp)
        if n != self.number_of_variables:
            warning_temp = f"The number of variables in the circuit ({self.number_of_variables}) differs from the n value ({n})!"
            warnings.warn(warning_temp)

    def __get_new_id(self) -> int:
        """
        Return a new ID.
        The ID counter will be incremented.
        :return: a new ID
        """

        id_temp = self.__id_counter
        self.__id_counter += 1

        return id_temp

    def __add_new_node(self, node: NodeAbstract) -> None:
        """
        Add the node to the circuit
        :param node: a node
        :return: None
        :raises NodeWithSameIDAlreadyExistsInCircuitException: if some node with the same ID already exists in the circuit
        """

        # There already exists some node with the same ID
        if self.node_exist(node):
            raise c_exception.NodeWithSameIDAlreadyExistsInCircuitException(str(node))

        self.__id_node_dictionary[node.id] = node
        self.__node_type_in_circuit_counter_dictionary[node.node_type] += 1

    def __smooth_create_and_node(self, node_id: int, variable_set: Set[int], use_unique_node_cache: bool = True) -> NodeAbstract:
        """
        This function is used by smoothing.
        node_id --> AND (node_id, (v_1 OR -v_1), (v_2 OR -v_2), ...)
        :param node_id: an identifier of the node
        :param variable_set: a set of variables
        :param use_unique_node_cache: True if unique node caching can be used
        :return: the new AND node
        :raises NodeWithIDDoesNotExistInCircuitException: if the identifier of the node does not exist in the circuit
        """

        # The node does not exist in the circuit
        if not self.node_id_exist(node_id):
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(node_id))

        child_id_set = {node_id}
        for variable in variable_set:
            v_id = self.create_literal_leaf(literal=variable,
                                            use_unique_node_cache=use_unique_node_cache)
            non_v_id = self.create_literal_leaf(literal=(-variable),
                                                use_unique_node_cache=use_unique_node_cache)

            or_node_id = self.create_or_node(child_id_set={v_id, non_v_id},
                                             decision_variable=variable,
                                             use_unique_node_cache=use_unique_node_cache)
            child_id_set.add(or_node_id)

        and_node_id = self.create_and_node(child_id_set=child_id_set,
                                           use_unique_node_cache=use_unique_node_cache)
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
        for child_id in sorted(child_id_list):
            # The child has been already explored
            if child_id in topological_ordering_list:
                continue

            self.__topological_ordering_recursion(child_id, topological_ordering_list)

        topological_ordering_list.append(node_id)
        return topological_ordering_list

    def __compute_size_of_circuit(self) -> None:
        """
        Compute the size of the circuit
        :return: None
        """

        # The root of the circuit is not set
        if not self.is_root_set():
            self.__size = None
            return

        self.__size = 0
        for node_id in self.__id_node_dictionary:
            node = self.__id_node_dictionary[node_id]
            self.__size += node.get_node_size()

    def __check_circuit_type(self) -> None:
        """
        Check the type of the circuit.
        If the root of the circuit is not set, None is set.
        :return: None
        """

        # The root of the circuit is not set
        if not self.is_root_set():
            self.__circuit_type = None
            return

        # The root of the circuit is a leaf
        if isinstance(self.__root, LeafAbstract):
            # 2-CNF or renamable Horn CNF leaf
            if isinstance(self.__root, TwoCnfLeaf) or isinstance(self.__root, RenamableHornCnfLeaf):
                self.__circuit_type = ct_enum.CircuitTypeEnum.SD_BDMC
            # Literal or constant leaf
            else:
                self.__circuit_type = ct_enum.CircuitTypeEnum.SD_DNNF

            return

        # The root of the circuit is an inner node
        is_decomposable_temp = self.__root.decomposable_in_circuit
        is_deterministic_temp = self.__root.deterministic_in_circuit
        is_smoothness_temp = self.__root.smoothness_in_circuit

        # BDMC
        bdmc = False
        if (self.__node_type_in_circuit_counter_dictionary[nt_enum.NodeTypeEnum.TWO_CNF] > 0) or \
           (self.__node_type_in_circuit_counter_dictionary[nt_enum.NodeTypeEnum.RENAMABLE_HORN_CNF] > 0):
            bdmc = True

        # CARA
        cara = False
        if self.__node_type_in_circuit_counter_dictionary[nt_enum.NodeTypeEnum.MAPPING_NODE] > 0:
            cara = True

        if is_smoothness_temp:
            if is_decomposable_temp and is_deterministic_temp:
                if bdmc:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.SD_BDMC
                elif cara:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.SD_CARA
                else:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.SD_DNNF

            elif is_decomposable_temp and (not is_deterministic_temp):
                if bdmc:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.S_BDMC
                elif cara:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.S_CARA
                else:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.S_DNNF

            else:
                if bdmc or cara:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.UNDEFINED
                else:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.NNF
        else:
            if is_decomposable_temp and is_deterministic_temp:
                if bdmc:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.D_BDMC
                elif cara:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.D_CARA
                else:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.D_DNNF

            elif is_decomposable_temp and (not is_deterministic_temp):
                if bdmc:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.BDMC
                elif cara:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.CARA
                else:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.DNNF

            else:
                if bdmc or cara:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.UNDEFINED
                else:
                    self.__circuit_type = ct_enum.CircuitTypeEnum.NNF
    # endregion

    # region Static method
    @staticmethod
    def __check_assumption_set_and_exist_quantification_set(assumption_set: Set[int],
                                                            exist_quantification_set: Set[int],
                                                            assumption_and_exist_set: bool = True) -> None:
        """
        Check if the assumption set and existential quantification set are valid.
        The assumption set and existential quantification set must be disjoint (with respect to the variables).
        No complementary literals can appear in the assumption set.
        It can be used for a default set and observation set as well.
        :param assumption_set: an assumption set / observation set
        :param exist_quantification_set: an existential quantification set / default set
        :param assumption_and_exist_set: True for an assumption and existential quantification set. False for an observation
        and default set.
        :return: None
        :raises AssumptionSetAndExistentialQuantificationSetAreNotDisjointException: if the assumption set and existential quantification set are not disjoint
        :raises AssumptionSetContainsComplementLiteralsException: if the sets are not valid
        :raises SetContainsLiteralsButOnlyVariablesAreAllowedException: if the existential quantification set contains a literal instead of variables
        """

        # Check if the sets are disjoint
        intersection_set_temp = set()
        for variable in exist_quantification_set:
            if (variable in assumption_set) or (-variable in assumption_set):
                intersection_set_temp.add(variable)

        if intersection_set_temp:
            raise c_exception.AssumptionSetAndExistentialQuantificationSetAreNotDisjointException(intersection_set_temp, assumption_and_exist_set)

        # Check if the existential quantification set contains only variables
        for variable in exist_quantification_set:
            if variable <= 0:
                set_name_temp = "existential quantification set" if assumption_and_exist_set else "default set"
                raise c_exception.SetContainsLiteralsButOnlyVariablesAreAllowedException(set_name_temp, exist_quantification_set)

        # Check complementary literals in the assumption set
        complementary_literals_set_temp = set()
        for literal in assumption_set:
            if -literal in assumption_set:
                complementary_literals_set_temp.add(literal)

        if complementary_literals_set_temp:
            raise c_exception.AssumptionSetContainsComplementLiteralsException(complementary_literals_set_temp, assumption_and_exist_set)

    @staticmethod
    def __add_edge(from_node: InnerNodeAbstract, to_node: NodeAbstract, smooth: bool = False, call_update: bool = True) -> None:
        """
        Add an oriented edge (from_node -> to_node) in the circuit
        :param smooth: True if the function is called because of smoothness
        :param call_update: True for calling the update function after this modification.
        If the parameter is set to False, then the circuit may be inconsistent after this modification.
        :return: None
        """

        to_node._add_parent(new_parent=from_node)
        from_node._add_child(new_child=to_node,
                             smooth=smooth,
                             call_update=call_update)

    @staticmethod
    def __remove_edge(from_node: InnerNodeAbstract, to_node: NodeAbstract, smooth: bool = False, call_update: bool = True) -> None:
        """
        Remove an oriented edge (from_node -> to_node) in the circuit
        :param smooth: True if the function is called because of smoothness
        :param call_update: True for calling the update function after this modification.
        If the parameter is set to False, then the circuit may be inconsistent after this modification.
        :return: None
        """

        to_node._remove_parent(parent_to_delete=from_node)
        from_node._remove_child(child_to_delete=to_node,
                                smooth=smooth,
                                call_update=call_update)

    @staticmethod
    def __generate_key_cache(child_id_set: Set[int]) -> str:
        """
        Generate a key for caching based on the children set.
        Cache: and_unique_node_cache, or_unique_node_cache
        :param child_id_set: a set of children's id
        :return: the generated key based on the child_id_set
        """

        child_id_sorted_list = SortedList(child_id_set)
        key_string = child_id_sorted_list.str_delimiter("-")

        return key_string
    # endregion

    # region Public method
    def node_exist(self, node: NodeAbstract) -> bool:
        """
        Check if the node exists in the circuit
        :param node: a node
        :return: True if the node exists in the circuit. Otherwise, False is returned.
        """

        return node.id in self.__id_node_dictionary

    def node_id_exist(self, node_id: int) -> bool:
        """
        Check if a node with the identifier exists in the circuit
        :param node_id: an identifier of the node
        :return: True if a node with the identifier exists in the circuit. Otherwise, False is returned.
        """

        return node_id in self.__id_node_dictionary

    def get_node(self, node_id: int) -> Union[NodeAbstract, None]:
        """
        Return a node with the identifier.
        If the node does not exist in the circuit, None is returned.
        :param node_id: an identifier of the node
        :return: the node with the identifier
        """

        # The identifier does not exist in the circuit
        if node_id not in self.__id_node_dictionary:
            return None

        return self.__id_node_dictionary[node_id]

    def create_constant_leaf(self, constant: bool, use_unique_node_cache: bool = True) -> int:
        """
        Create a new constant leaf in the circuit
        :param constant: the value of the constant leaf
        :param use_unique_node_cache: True if unique node caching can be used
        :return: the identifier of the node
        """

        # The node already exists in the circuit
        if use_unique_node_cache and (self.__constant_unique_node_cache[int(constant)] is not None):
            return self.__constant_unique_node_cache[int(constant)]

        node = ConstantLeaf(constant=constant,
                            id=self.__get_new_id())
        self.__add_new_node(node)
        node_id = node.id

        # Cache
        self.__constant_unique_node_cache[int(constant)] = node_id

        return node_id

    def create_literal_leaf(self, literal: int, use_unique_node_cache: bool = True) -> int:
        """
        Create a new literal leaf in the circuit
        :param literal: the value of the literal leaf
        :param use_unique_node_cache: True if unique node caching can be used
        :return: the identifier of the node
        """

        # The node already exists in the circuit
        if use_unique_node_cache and (literal in self.__literal_unique_node_cache):
            return self.__literal_unique_node_cache[literal]

        node = LiteralLeaf(literal=literal,
                           id=self.__get_new_id())
        self.__add_new_node(node)
        node_id = node.id

        # Cache
        self.__literal_unique_node_cache[literal] = node_id

        return node_id

    def create_literal_leaf_set(self, literal_set: Set[int], use_unique_node_cache: bool = True) -> Set[int]:
        node_id_set = set()

        for literal in literal_set:
            node_id = self.create_literal_leaf(literal, use_unique_node_cache)
            node_id_set.add(node_id)

        return node_id_set

    def create_2_cnf_leaf(self, two_cnf: PySat2Cnf) -> int:
        """
        Create a new 2-CNF leaf in the circuit
        :param two_cnf: 2-CNF
        :return: the identifier of the node
        """

        node = TwoCnfLeaf(cnf=two_cnf,
                          id=self.__get_new_id())
        self.__add_new_node(node)

        return node.id

    def create_renamable_horn_cnf_leaf(self, renamable_horn_cnf: PySatHornCnf, renaming_function: Set[int]) -> int:
        """
        Create a new renamable Horn CNF leaf in the circuit
        :param renamable_horn_cnf: renamable Horn CNF
        :param renaming_function: a set of variables that were renamed
        :return: the identifier of the node
        """

        node = RenamableHornCnfLeaf(cnf=renamable_horn_cnf,
                                    renaming_function=renaming_function,
                                    id=self.__get_new_id())
        self.__add_new_node(node)

        return node.id

    def create_and_node(self, child_id_set: Set[int], use_unique_node_cache: bool = True) -> int:
        """
        Create a new AND node in the circuit
        :param child_id_set: a set of children's id
        :param use_unique_node_cache: True if unique node caching can be used
        :return: the identifier of the node
        :raises NodeWithIDDoesNotExistInCircuitException: if some child's id does not exist in the circuit
        """

        # No child was given -> constant leaf (TRUE)
        if not len(child_id_set):
            return self.create_constant_leaf(constant=True,
                                             use_unique_node_cache=use_unique_node_cache)

        # Only one child was given -> AND node is not needed
        if len(child_id_set) == 1:
            return list(child_id_set)[0]

        # Cache
        key_cache = Circuit.__generate_key_cache(child_id_set)
        if use_unique_node_cache and (key_cache in self.__and_unique_node_cache):
            return self.__and_unique_node_cache[key_cache]

        child_node_set = set()
        for child_id in child_id_set:
            child_temp = self.get_node(child_id)

            # The child's id does not exist in the circuit
            if child_temp is None:
                raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(child_id), "trying to create an AND node with a nonexisting child")

            child_node_set.add(child_temp)

        node = AndInnerNode(child_set=child_node_set,
                            id=self.__get_new_id())
        self.__add_new_node(node)
        node_id = node.id

        # Cache
        self.__and_unique_node_cache[key_cache] = node_id

        return node_id

    def create_or_node(self, child_id_set: Set[int], decision_variable: Union[int, None] = None, use_unique_node_cache: bool = True) -> int:
        """
        Create a new OR node in the circuit
        :param child_id_set: a set of children's id
        :param decision_variable: The decision variable. If the decision variable does not exist, None is expected.
        :param use_unique_node_cache: True if unique node caching can be used
        :return: the identifier of the node
        :raises NodeWithIDDoesNotExistInCircuitException: if some child's id does not exist in the circuit
        """

        # No child was given -> constant leaf (FALSE)
        if not len(child_id_set):
            return self.create_constant_leaf(constant=False,
                                             use_unique_node_cache=use_unique_node_cache)

        # Only one child was given -> OR node is not needed
        if len(child_id_set) == 1:
            return list(child_id_set)[0]

        # Cache
        key_cache = Circuit.__generate_key_cache(child_id_set)
        if use_unique_node_cache and (key_cache in self.__or_unique_node_cache):
            return self.__or_unique_node_cache[key_cache]

        child_node_set = set()
        for child_id in child_id_set:
            child_temp = self.get_node(child_id)

            # The child's id does not exist in the circuit
            if child_temp is None:
                raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(child_id), "trying to create an OR node with a nonexisting child")

            child_node_set.add(child_temp)

        node = OrInnerNode(child_set=child_node_set,
                           id=self.__get_new_id(),
                           decision_variable=decision_variable)
        self.__add_new_node(node)
        node_id = node.id

        # Cache
        self.__or_unique_node_cache[key_cache] = node_id

        return node_id

    def create_decision_node(self, variable: int, true_node_id: int, false_node_id: int, use_unique_node_cache: bool = True) -> int:
        """
        Create a new decision node in the circuit
        (true_node_id AND variable) OR (false_node_id AND -variable)
        :param variable: a decision variable
        :param true_node_id: an identifier of the node that occurs with the variable in the AND node (true_node_id AND variable)
        :param false_node_id: an identifier of the node that occurs with the negative variable in the AND node (false_node_id AND -variable)
        :param use_unique_node_cache: True if unique node caching can be used
        :return: the identifier of the node
        :raises NodeWithIDDoesNotExistInCircuitException: if true_node_id or false_node_id does not exist in the circuit
        """

        # One of the nodes does not exist in the circuit
        if not self.node_id_exist(true_node_id):
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(true_node_id), message_extension="decision node (true_node)")

        if not self.node_id_exist(false_node_id):
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(false_node_id), message_extension="decision node (false_node)")

        true_literal_leaf_id = self.create_literal_leaf(literal=variable,
                                                        use_unique_node_cache=use_unique_node_cache)
        false_literal_leaf_id = self.create_literal_leaf(literal=(-variable),
                                                         use_unique_node_cache=use_unique_node_cache)

        true_and_node_id = self.create_and_node(child_id_set={true_node_id, true_literal_leaf_id},
                                                use_unique_node_cache=use_unique_node_cache)
        false_and_node_id = self.create_and_node(child_id_set={false_node_id, false_literal_leaf_id},
                                                 use_unique_node_cache=use_unique_node_cache)
        or_node_id = self.create_or_node(child_id_set={true_and_node_id, false_and_node_id},
                                         decision_variable=variable,
                                         use_unique_node_cache=use_unique_node_cache)

        return or_node_id

    def create_mapping_node(self, child_id: int, variable_id_mapping_id_dictionary_cache: Dict[int, int],
                            mapping_id_variable_id_dictionary: Dict[int, int], composition_needed: bool = True) -> int:
        """
        Create a new mapping node in the circuit
        :param child_id: an identifier of the child
        :param variable_id_mapping_id_dictionary_cache: variable_id -> mapping_id (mapping from the node in the cache)
        :param mapping_id_variable_id_dictionary: mapping_id -> variable_id (mapping from the generated key)
        :param composition_needed: True if the composition is needed to be done (mainly for caching) (variable_id_mapping_id_dictionary_cache o mapping_id_variable_id_dictionary)
        :return: the identifier of the node
        :raises MappingIsIncompleteException: if one of the mappings is invalid
        :raises NodeWithIDDoesNotExistInCircuitException: if the child's id does not exist in the circuit
        """

        composed_mapping_variable_cache_variable_id_dictionary: Dict[int, int] = dict()
        composed_mapping_variable_id_variable_cache_dictionary: Dict[int, int] = dict()

        # The composition is needed
        if composition_needed:
            for variable_cache in variable_id_mapping_id_dictionary_cache:
                mapping_id = variable_id_mapping_id_dictionary_cache[variable_cache]

                if mapping_id not in mapping_id_variable_id_dictionary:
                    raise c_exception.MappingIsIncompleteException(mapping_dictionary=mapping_id_variable_id_dictionary,
                                                                   variable_or_literal_in_circuit=set(variable_id_mapping_id_dictionary_cache.values()))

                variable_id = mapping_id_variable_id_dictionary[mapping_id]

                composed_mapping_variable_cache_variable_id_dictionary[variable_cache] = variable_id
                composed_mapping_variable_id_variable_cache_dictionary[variable_id] = variable_cache

            mapping_is_needed = False
            for variable_cache in composed_mapping_variable_cache_variable_id_dictionary:
                variable_id = composed_mapping_variable_cache_variable_id_dictionary[variable_cache]

                if variable_cache != variable_id:
                    mapping_is_needed = True
                    break

            # Mapping is not needed
            if not mapping_is_needed:
                return child_id
        else:
            composed_mapping_variable_id_variable_cache_dictionary = variable_id_mapping_id_dictionary_cache
            composed_mapping_variable_cache_variable_id_dictionary = mapping_id_variable_id_dictionary

        child_temp = self.get_node(child_id)

        # The child's id does not exist in the circuit
        if child_temp is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(child_id), "trying to create a mapping node with a nonexisting child")

        node = MappingInnerNode(child=child_temp,
                                variable_id_mapping_id_dictionary=composed_mapping_variable_id_variable_cache_dictionary,
                                mapping_id_variable_id_dictionary=composed_mapping_variable_cache_variable_id_dictionary,
                                id=self.__get_new_id())
        self.__add_new_node(node)

        return node.id

    def clear_comments(self) -> None:
        """
        Clear the comments of the circuit
        :return: None
        """

        self.set_comments("")

    def set_comments(self, new_comment: str) -> None:
        """
        Set the comments of the circuit
        :param new_comment: a new comment
        :return: None
        """

        self.__comments = new_comment

    def set_root(self, node_id: int) -> None:
        """
        Set the root of the circuit
        :param node_id: an identifier of the node
        :return: None
        :raises NodeWithIDDoesNotExistInCircuitException: if the identifier of the node does not exist in the circuit
        """

        root_temp = self.get_node(node_id)

        # The node does not exist in the circuit
        if root_temp is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(node_id))

        self.__root = root_temp

        # Recheck the type of the circuit
        self.__check_circuit_type()

        # Recompute the size of the circuit
        self.__compute_size_of_circuit()

    def is_root_set(self) -> bool:
        """
        :return: True if the root of the circuit is set. Otherwise, False is returned.
        """

        if self.__root is None:
            return False

        return True

    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True) -> bool:
        """
        Check if the circuit is satisfiable with the assumption set and existential quantification set
        Requirement: decomposability
        :param assumption_set: an assumption set
        :param exist_quantification_set: an existential quantification set
        :param use_cache: True if the cache can be used
        :return: True if the circuit is satisfiable with the assumption set and existential quantification set. Otherwise, False is returned.
        :raises AssumptionSetAndExistentialQuantificationSetAreNotDisjointException: if the assumption set and existential quantification set are not disjoint
        :raises SetContainsLiteralsButOnlyVariablesAreAllowedException: if the existential quantification set contains a literal instead of variables
        :raises RootOfCircuitIsNotSetUpException: if the root of the circuit is not set
        """

        # The root of the circuit is not set
        if not self.is_root_set():
            raise c_exception.RootOfCircuitIsNotSetException()

        Circuit.__check_assumption_set_and_exist_quantification_set(assumption_set, exist_quantification_set)

        return self.__root.is_satisfiable(assumption_set=assumption_set,
                                          exist_quantification_set=exist_quantification_set,
                                          use_cache=use_cache)

    def clause_entailment(self, clause: Set[int], exist_quantification_set: Set[int], use_cache: bool = True) -> bool:
        """
        Check if the circuit implies the clause
        Requirement: decomposability
        :param clause: a clause
        :param exist_quantification_set: an existential quantification set
        :param use_cache: True if the cache can be used
        :return: True if the circuit implies the clause. Otherwise, False is returned.
        """

        assumption_set = set()
        for lit in clause:
            assumption_set.add(-lit)

        return not self.is_satisfiable(assumption_set=assumption_set,
                                       exist_quantification_set=exist_quantification_set,
                                       use_cache=use_cache)

    def model_counting(self, assumption_set: Set[int], use_cache: bool = True) -> int:
        """
        Count the number of models with the assumption set
        Requirement: decomposability, determinism, smoothness
        :param assumption_set: an assumption set
        :param use_cache: True if the cache can be used
        :return: the number of models
        :raises AssumptionSetContainsComplementLiteralsException: if the assumption set is not valid
        :raises RootOfCircuitIsNotSetUpException: if the root of the circuit is not set
        """

        # The root of the circuit is not set
        if not self.is_root_set():
            raise c_exception.RootOfCircuitIsNotSetException()

        # BDMC
        if (self.__node_type_in_circuit_counter_dictionary[nt_enum.NodeTypeEnum.TWO_CNF] > 0) or \
           (self.__node_type_in_circuit_counter_dictionary[nt_enum.NodeTypeEnum.RENAMABLE_HORN_CNF] > 0):
            warnings.warn("The circuit contains 2-CNF or renamable Horn formulae -> time complexity can be exponential!")

        Circuit.__check_assumption_set_and_exist_quantification_set(assumption_set, set())

        self.smooth()
        return self.__root.model_counting(assumption_set=assumption_set,
                                          use_cache=use_cache)

    def is_valid(self, assumption_set: Set[int], use_cache: bool = True) -> bool:
        """
        Check if the formula is valid with the assumption set
        Requirement: decomposability, determinism, smoothness
        :param assumption_set: an assumption set
        :param use_cache: True if the cache can be used
        :return: True if the formula is valid. Otherwise, False is returned.
        :raises AssumptionSetContainsComplementLiteralsException: if the assumption set is not valid
        :raises RootOfCircuitIsNotSetUpException: if the root of the circuit is not set
        """

        number_of_models = self.model_counting(assumption_set=assumption_set,
                                               use_cache=use_cache)

        restricted_assumption_set_temp = self.__root._create_restricted_assumption_set(assumption_set=assumption_set,
                                                                                       variable_id_mapping_id_dictionary=None)

        return number_of_models == 2**(self.number_of_variables - len(restricted_assumption_set_temp))

    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_cache: bool = True) -> float:
        """
        Compute the minimum default-cardinality of the circuit.
        Return infinity in case the circuit is unsatisfiable.
        An empty default set corresponds to all variables except ones that appear in the observation set.
        Requirement: decomposability
        :param observation_set: a set of literals representing observations
        :param default_set: a set of variables representing defaults (we assume that all of these defaults are true)
        :param use_cache: True if the cache can be used
        :return: the minimum default-cardinality
        :raises AssumptionSetAndExistentialQuantificationSetAreNotDisjointException: if the observation set and default set are not disjoint
        :raises AssumptionSetContainsComplementLiteralsException: if the observation set is not valid
        :raises RootOfCircuitIsNotSetUpException: if the root of the circuit is not set
        """

        # The root of the circuit is not set
        if not self.is_root_set():
            raise c_exception.RootOfCircuitIsNotSetException()

        # The default set is empty
        if not default_set:
            default_set = set()
            variable_set_temp = self.__root._get_variable_in_circuit_set(copy=False)
            for variable in variable_set_temp:
                if (variable not in observation_set) and (-variable not in observation_set):
                    default_set.add(variable)

        Circuit.__check_assumption_set_and_exist_quantification_set(observation_set, default_set)

        return self.__root.minimum_default_cardinality(observation_set=observation_set,
                                                       default_set=default_set,
                                                       use_cache=use_cache)

    def smooth(self) -> None:
        """
        Smooth the circuit
        :return: None
        """

        # The root of the circuit is not set, or the root is a leaf
        if not self.is_root_set() or isinstance(self.__root, LeafAbstract):
            return

        # The circuit is already smooth
        if self.__root.smoothness_in_circuit:
            return

        node_id_list = list(self.__id_node_dictionary.keys())
        for node_id in node_id_list:
            node = self.__id_node_dictionary[node_id]

            # The node is not an inner node
            if not isinstance(node, OrInnerNode):
                continue

            # The node is smooth
            if node.smoothness:
                continue

            union_variable_set = node._get_variable_in_circuit_set(copy=False)
            child_set = node._get_child_set(copy=True)
            for child in child_set:
                difference_set = union_variable_set.difference(child._get_variable_in_circuit_set(copy=False))

                # The difference set is not empty
                if difference_set:
                    and_node = self.__smooth_create_and_node(child.id, difference_set)

                    Circuit.__remove_edge(from_node=node,
                                          to_node=child,
                                          smooth=True,
                                          call_update=False)
                    Circuit.__add_edge(from_node=node,
                                       to_node=and_node,
                                       smooth=True,
                                       call_update=False)

        # Update properties for all inner nodes in the circuit
        leaf_set = set()
        inner_node_set = set()

        inner_node_set_temp = set()
        for node_id in self.__id_node_dictionary:
            node = self.__id_node_dictionary[node_id]

            if isinstance(node, LeafAbstract):
                leaf_set.add(node)
                inner_node_set_temp.update(node._get_parent_set(copy=False))

        visited_inner_node_set = leaf_set

        # Get only those inner nodes whose children are only leaves
        for inner_node in inner_node_set_temp:
            child_set = inner_node._get_child_set(copy=False)

            if len(child_set.intersection(leaf_set)) == len(child_set):
                inner_node_set.add(inner_node)

        while inner_node_set:
            inner_node_set_temp = set()

            for inner_node in inner_node_set:
                inner_node._update(call_parent_update=False,
                                   smooth=True)
                visited_inner_node_set.add(inner_node)

                # Add parents whose all children are visited nodes
                parent_set = inner_node._get_parent_set(copy=False)
                for parent in parent_set:
                    child_set = parent._get_child_set(copy=False)
                    if len(child_set.intersection(visited_inner_node_set)) == len(child_set):
                        inner_node_set_temp.add(parent)

            inner_node_set = inner_node_set_temp

        # Recheck the type of the circuit
        self.__check_circuit_type()

        # Recompute the size of the circuit
        self.__compute_size_of_circuit()

    def topological_ordering(self) -> List[int]:
        """
        Return a topological ordering of the circuit
        :return: a list (of identifiers) that corresponds to a topological ordering
        :raises RootOfCircuitIsNotSetUpException: if the root of the circuit is not set
        """

        # The root of the circuit is not set
        if not self.is_root_set():
            raise c_exception.RootOfCircuitIsNotSetException()

        return self.__topological_ordering_recursion(self.__root.id, [])

    def is_decomposable(self) -> Union[bool, None]:
        """
        Is the circuit decomposable?
        If the root of the circuit is not set, None is returned.
        :return: True if the circuit is decomposable. Otherwise, False is returned.
        """

        # The root of the circuit is not set
        if not self.is_root_set():
            return None

        # The root of the circuit is a leaf
        if isinstance(self.__root, LeafAbstract):
            return True

        return self.__root.decomposable_in_circuit

    def is_deterministic(self) -> Union[bool, None]:
        """
        Is the circuit deterministic?
        If the root of the circuit is not set, None is returned.
        :return: True if the circuit is deterministic. Otherwise, False is returned.
        """

        # The root of the circuit is not set
        if not self.is_root_set():
            return None

        # The root of the circuit is a leaf
        if isinstance(self.__root, LeafAbstract):
            return True

        return self.__root.deterministic_in_circuit

    def is_smooth(self) -> Union[bool, None]:
        """
        Is the circuit smooth?
        If the root of the circuit is not set, None is returned.
        :return: True if the circuit is smooth. Otherwise, False is returned.
        """

        # The root of the circuit is not set
        if not self.is_root_set():
            return None

        # The root of the circuit is a leaf
        if isinstance(self.__root, LeafAbstract):
            return True

        return self.__root.smoothness_in_circuit

    def add_edge(self, from_id_node: int, to_id_node: int) -> None:
        """
        Add an oriented edge (from_id_node -> to_id_node) in the circuit.
        If the oriented edge already exists in the circuit, nothing happens.
        :param from_id_node: a new to_id_node's parent
        :param to_id_node: a new from_id_node's child
        :return: None
        :raises SomethingWrongException: if the from_id_node is not an inner node
        :raises NodeWithIDDoesNotExistInCircuitException: if one of the nodes does not exist in the circuit
        """

        # One of the nodes does not exist in the circuit
        from_node = self.get_node(from_id_node)
        if from_node is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(from_id_node), message_extension="add_edge (from_id_node)")

        to_node = self.get_node(to_id_node)
        if to_node is None:
            raise c_exception.NodeWithIDDoesNotExistInCircuitException(str(to_id_node), message_extension="add_edge (to_id_node)")

        # from_node is not an inner node
        if not isinstance(from_node, InnerNodeAbstract):
            raise c_exception.SomethingWrongException(f"trying to add an edge from the node ({from_id_node}) that is not an inner node")

        # The edge already exists
        if to_id_node in from_node.get_child_id_list():
            return

        Circuit.__add_edge(from_node=from_node,
                           to_node=to_node,
                           smooth=False,
                           call_update=True)

        # Recheck the type of the circuit
        self.__check_circuit_type()

        # Recompute the size of the circuit
        self.__compute_size_of_circuit()

    def str_node_type_dictionary(self, prefix: str = "") -> str:
        """
        :param prefix: a string that appears before every line (mainly for comments)
        :return: a string representation of the node type dictionary
        """

        result = ""

        for node_type in self.__node_type_in_circuit_counter_dictionary:
            value = self.__node_type_in_circuit_counter_dictionary[node_type]

            if not result:
                result = f"{prefix}{node_type.name}: {str(value)}"
            else:
                result = "\n".join((result, f"{prefix}{node_type.name}: {str(value)}"))

        return result

    def get_node_type_dictionary(self) -> Dict[nt_enum.NodeTypeEnum, int]:
        """
        :return: a copy of node type dictionary
        """

        return self.__node_type_in_circuit_counter_dictionary.copy()

    def get_header_str(self) -> str:
        string = "\n".join((f"C CaraCompiler",
                            f"C Name: {self.circuit_name}",
                            f"C Type: {str(self.circuit_type.name)}",
                            f"C Decomposability: {self.is_decomposable()}",
                            f"C Determinism: {self.is_deterministic()}",
                            f"C Smoothness: {self.is_smooth()}",
                            self.str_node_type_dictionary(prefix="C ")))

        if self.comments and not self.comments.startswith("CaraCompiler"):
            comments_list_temp = self.comments.split("\n")
            comments_temp = "\n".join(map(lambda comment: f"C {comment}", comments_list_temp))
            string = "\n".join((string, "C", comments_temp))

        return string

    def save_to_file(self, file_path: str) -> None:
        """
        Save the circuit to the file.
        No topological ordering is used!
        :return: None
        """

        with open(file_path, "w", encoding="utf-8") as file:
            # Header
            file.write(f"{self.get_header_str()}\n")

            # N line
            file.write(f"nnf {str(self.number_of_nodes)} {str(self.size)} {str(self.number_of_variables)}\n")

            # Node lines
            for node_id in self.__id_node_dictionary:
                node = self.__id_node_dictionary[node_id]

                # Constant leaf
                if isinstance(node, ConstantLeaf):
                    # True
                    if node.constant:
                        file.write("A 0\n")
                    # False
                    else:
                        file.write("O 0 0\n")

                    continue

                # Literal leaf
                if isinstance(node, LiteralLeaf):
                    file.write(f"L {node.literal}\n")
                    continue

                # AND node
                if isinstance(node, AndInnerNode):
                    child_id_list = node.get_child_id_list()
                    child_id_sorted_list = SortedList(child_id_list)

                    file.write(f"A {len(child_id_list)} {str(child_id_sorted_list)}\n")
                    continue

                # OR node
                if isinstance(node, OrInnerNode):
                    child_id_list = node.get_child_id_list()
                    child_id_sorted_list = SortedList(child_id_list)
                    j = 0 if node.decision_variable is None else node.decision_variable

                    file.write(f"O {j} {len(child_id_list)} {str(child_id_sorted_list)}\n")
                    continue

                # 2-CNF or renamable Horn CNF leaf
                if isinstance(node, TwoCnfLeaf) or isinstance(node, RenamableHornCnfLeaf):
                    char_temp = "T" if isinstance(node, TwoCnfLeaf) else "R"

                    string_temp, mapping_temp = node.str_with_mapping()
                    mapping_temp = sorted(mapping_temp, key=mapping_temp.get, reverse=False)

                    file.write(f"{char_temp} {node.number_of_clauses + 1} {node.number_of_variables} {' '.join(map(str, mapping_temp))}\n")
                    file.write(f"{string_temp}\n")
                    continue

                # Mapping node
                if isinstance(node, MappingInnerNode):
                    child_id = node.get_child_id_list()[0]

                    file.write(f"M {child_id} {node.number_of_variables} {node.str_mapping()}\n")
                    continue

                raise c_exception.SomethingWrongException(f"this type of node ({type(node)}) is not implemented in save_to_file")
    # endregion

    # region Magic method
    def __str__(self):
        try:
            topological_ordering = self.topological_ordering()
            id_to_dictionary = dict()
            for to, id in enumerate(topological_ordering):
                id_to_dictionary[id] = to

            # Header
            string = self.get_header_str()

            # N line
            string = "\n".join((string, f"nnf {str(self.number_of_nodes)} {str(self.size)} {str(self.number_of_variables)}"))

            # Node lines
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

                    child_to_sorted_list = SortedList(child_to_list)

                    string = "\n".join((string, f"A {len(child_to_list)} {str(child_to_sorted_list)}"))
                    continue

                # OR node
                if isinstance(node, OrInnerNode):
                    child_id_list = node.get_child_id_list()
                    child_to_list = []

                    for child_id in child_id_list:
                        child_to_list.append(id_to_dictionary[child_id])

                    child_to_sorted_list = SortedList(child_to_list)
                    j = 0 if node.decision_variable is None else node.decision_variable

                    string = "\n".join((string, f"O {j} {len(child_to_list)} {str(child_to_sorted_list)}"))
                    continue

                # 2-CNF or renamable Horn CNF leaf
                if isinstance(node, TwoCnfLeaf) or isinstance(node, RenamableHornCnfLeaf):
                    char_temp = "T" if isinstance(node, TwoCnfLeaf) else "R"

                    string_temp, mapping_temp = node.str_with_mapping()
                    mapping_temp = sorted(mapping_temp, key=mapping_temp.get, reverse=False)

                    string = "\n".join((string, f"{char_temp} {node.number_of_clauses + 1} {node.number_of_variables} {' '.join(map(str, mapping_temp))}", string_temp))
                    continue

                # Mapping node
                if isinstance(node, MappingInnerNode):
                    child_id = node.get_child_id_list()[0]
                    child_id = id_to_dictionary[child_id]

                    string = "\n".join((string, f"M {child_id} {node.number_of_variables} {node.str_mapping()}"))
                    continue

                raise c_exception.SomethingWrongException(f"this type of node ({type(node)}) is not implemented in __str__ (circuit)")

            return string
        except c_exception.RootOfCircuitIsNotSetException:
            warnings.warn("__str__ (circuit) returned an empty string because the root of the circuit is not set!")
            return ""

    def __repr__(self):
        comments_temp = self.comments.replace("\n", ", ")
        string_temp = " ".join((f"Name: {self.circuit_name}",
                                f"Number of nodes: {str(self.number_of_nodes)}",
                                f"Comments: {comments_temp}"))

        if self.is_root_set():
            string_temp = " ".join((string_temp,
                                    f"Root: {self.root_id}",
                                    f"Number of variables: {str(self.number_of_variables)}",
                                    f"Size: {str(self.size)}"))

        # The nodes in the circuit
        id_node_sorted_dictionary_temp = SortedDict(self.__id_node_dictionary)
        for key in iter(id_node_sorted_dictionary_temp):
            string_temp = "\n".join((string_temp, repr(self.__id_node_dictionary[key])))

        return string_temp
    # endregion

    # region Property
    @property
    def circuit_name(self) -> str:
        return self.__circuit_name

    @property
    def number_of_nodes(self) -> int:
        return len(self.__id_node_dictionary)

    @property
    def number_of_variables(self) -> int:
        if not self.is_root_set():
            return 0

        return self.__root.number_of_variables

    @property
    def size(self) -> Union[int, None]:
        return self.__size

    @property
    def comments(self) -> str:
        return self.__comments

    @property
    def circuit_type(self) -> Union[ct_enum.CircuitTypeEnum, None]:
        return self.__circuit_type

    @property
    def root_id(self) -> Union[int, None]:
        if not self.is_root_set():
            return None

        return self.__root.id
    # endregion
