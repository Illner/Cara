# Import
import os
import subprocess
from pathlib import Path
from formula.cnf import Cnf
import other.environment as env
from typing import Set, Dict, List, Tuple

# Import exception
import exception.cara_exception as c_exception
import exception.formula.hypergraph_exception as h_exception

# Import enum
import formula.hypergraph_cache_enum as hc_enum
import formula.hypergraph_weight_type_enum as hw_enum
import formula.hypergraph_software_enum as hs_enum


class Hypergraph:
    """
    Hypergraph representation
    """

    """
    Private Cnf cnf
    Private float ub_factor
    Private int number_of_nodes                         # number of clauses
    Private int number_of_hyperedges                    # number of variables
    Private Set<int> variable_set
    Private HypergraphCacheEnum cache_enum
    Private HypergraphNodeWeightEnum node_weight_enum
    Private HypergraphHyperedgeWeightEnum hyperedge_weight_enum
    Private HypergraphSoftwareEnum software_enum
    
    Private Dict<int, int> node_weight_dictionary       # key: node = clause's id, value: the weight of the clause
    Private Dict<int, int> hyperedge_weight_dictionary  # key: edge = variable, value: the weight of the variable
    
    Private Dict<int, Set<int>> hypergraph_dictionary   # key: variable, value: a set of clauses where the variable appears
    """

    # Static variable - Path
    TEMP_FOLDER_PATH = os.path.join(os.getcwd(), "temp")
    INPUT_FILE_EXE_HMETIS_PATH = os.path.join(TEMP_FOLDER_PATH, "input_file_hypergraph.graph")
    OUTPUT_FILE_EXE_HMETIS_PATH = INPUT_FILE_EXE_HMETIS_PATH + ".part.2"
    WIN_PROGRAM_EXE_HMETIS_PATH = os.path.join(os.getcwd(), "external", "hypergraph_partitioning", "hMETIS", "win", "shmetis.exe")

    def __init__(self, cnf: Cnf, ub_factor: float = 0.10, cache_enum: hc_enum.HypergraphCacheEnum = hc_enum.HypergraphCacheEnum.NONE,
                 node_weight_enum: hw_enum.HypergraphNodeWeightEnum = hw_enum.HypergraphNodeWeightEnum.NONE,
                 hyperedge_weight_enum: hw_enum.HypergraphHyperedgeWeightEnum = hw_enum.HypergraphHyperedgeWeightEnum.NONE,
                 software_enum: hs_enum.HypergraphSoftwareEnum = hs_enum.HypergraphSoftwareEnum.HMETIS):
        self.__cnf: Cnf = cnf
        self.__cache_enum: hc_enum.HypergraphCacheEnum = cache_enum
        self.__node_weight_enum: hw_enum.HypergraphNodeWeightEnum = node_weight_enum
        self.__hyperedge_weight_enum: hw_enum.HypergraphHyperedgeWeightEnum = hyperedge_weight_enum
        self.__software_enum: hs_enum.HypergraphSoftwareEnum = software_enum
        self.__number_of_nodes: int = cnf.real_number_of_clauses
        self.__number_of_hyperedges: int = cnf.number_of_variables
        self.__variable_set: Set[int] = cnf._get_variable_set(copy=True)

        # UBfactor
        ub_factor = round(ub_factor, 2)
        if ub_factor < 0.01 or ub_factor > 0.49:
            raise h_exception.InvalidUBfactorException(ub_factor)
        self.__ub_factor: float = ub_factor

        self.__node_weight_dictionary: Dict[int, int] = dict()
        self.__hyperedge_weight_dictionary: Dict[int, int] = dict()
        self.__hypergraph_dictionary: Dict[int, Set[int]] = dict()

        self.__check_files_and_folders()
        self.__create_hypergraph()
        self.__set_static_weights()

    # region Private method
    def __create_hypergraph(self) -> None:
        """
        Initialize the hypergraph
        Variable: hypergraph_dictionary
        :return: None
        """

        for variable in self.__variable_set:
            clause_temp = set()

            # Positive literal
            clause_temp.update(self.__cnf._get_clause_set(variable))
            # Negative literal
            clause_temp.update(self.__cnf._get_clause_set(-variable))

            self.__hypergraph_dictionary[variable] = clause_temp

    def __set_static_weights(self) -> None:
        """
        Initialize the static weights.
        If the type of weights is not STATIC, nothing happens.
        Variable: node_weight_dictionary, hyperedge_weight_dictionary
        :return: None
        """

        # Node's weight
        if self.__node_weight_enum == hw_enum.HypergraphNodeWeightEnum.STATIC:
            for node in range(self.__number_of_nodes):
                self.__node_weight_dictionary[node] = node + 1     # TODO

        # Hyperedge's weight
        if self.__hyperedge_weight_enum == hw_enum.HypergraphHyperedgeWeightEnum.STATIC:
            for hyperedge in self.__variable_set:
                self.__hyperedge_weight_dictionary[hyperedge] = hyperedge   # TODO

    def __set_dynamic_weights(self, clause_id_set: Set[int], ignored_literal_set: Set[int]) -> None:
        """
        Initialize the dynamic weights based on the clause_id_set and ignored_literal_set.
        If the type of weights is not Dynamic, nothing happens.
        Variable: node_weight_dictionary, hyperedge_weight_dictionary
        :param clause_id_set: the subset of clauses
        :param ignored_literal_set: the ignored literals
        :return: None
        """

        # Node's weight
        if self.__node_weight_enum == hw_enum.HypergraphNodeWeightEnum.DYNAMIC:
            pass    # TODO

        # Hyperedge's weight
        if self.__hyperedge_weight_enum == hw_enum.HypergraphHyperedgeWeightEnum.DYNAMIC:
            pass    # TODO

    def __get_node_weight(self, node_id: int) -> int:
        """
        Return the weight of the node based on the node_weight_enum.
        If the node does not exist in the hypergraph, raise an exception (NodeDoesNotExistException).
        :param node_id: the node's ID
        :return: the weight of the node
        """

        # The node does not exist in the hypergraph
        if node_id < 0 or node_id >= self.__number_of_nodes:
            raise h_exception.NodeDoesNotExistException(node_id)

        # No weights
        if self.__node_weight_enum == hw_enum.HypergraphNodeWeightEnum.NONE:
            return 1

        # Static/Dynamic weights
        if (self.__node_weight_enum == hw_enum.HypergraphNodeWeightEnum.STATIC) or \
           (self.__node_weight_enum == hw_enum.HypergraphNodeWeightEnum.DYNAMIC):
            return self.__node_weight_dictionary[node_id]

        raise c_exception.FunctionNotImplementedException("get_node_weight", f"this type of weights ({self.__node_weight_enum.name}) is not implemented")

    def __get_hyperedge_weight(self, hyperedge_id: int) -> int:
        """
        Return the weight of the hyperedge based on the hyperedge_weight_enum.
        If the hyperedge does not exist in the hypergraph, raise an exception (HyperedgeDoesNotExistException).
        :param hyperedge_id: the hyperedge's ID
        :return: the weight of the hyperedge
        """

        # The hyperedge does not exist in the hypergraph
        if hyperedge_id not in self.__variable_set:
            raise h_exception.HyperedgeDoesNotExistException(hyperedge_id)

        # No weights
        if self.__hyperedge_weight_enum == hw_enum.HypergraphHyperedgeWeightEnum.NONE:
            return 1

        # Static/Dynamic weights
        if (self.__hyperedge_weight_enum == hw_enum.HypergraphHyperedgeWeightEnum.STATIC) or \
           (self.__hyperedge_weight_enum == hw_enum.HypergraphHyperedgeWeightEnum.DYNAMIC):
            return self.__hyperedge_weight_dictionary[hyperedge_id]

        raise c_exception.FunctionNotImplementedException("get_hyperedge_weight", f"this type of weights ({self.__hyperedge_weight_enum.name}) is not implemented")

    def __check_files_and_folders(self) -> None:
        """
        Check if all necessary files and folders exist.
        If some file is missing, raise an exception (FileIsMissingException).
        If the chosen software is not supported on the system, raise an exception (SoftwareIsNotSupportedOnSystemException).
        :return: None
        """

        # Windows
        if env.is_windows():
            # hMETIS
            if self.__software_enum == hs_enum.HypergraphSoftwareEnum.HMETIS:
                Path(Hypergraph.TEMP_FOLDER_PATH).mkdir(exist_ok=True)

                if not Path(Hypergraph.WIN_PROGRAM_EXE_HMETIS_PATH).exists():
                    raise h_exception.FileIsMissingException(Hypergraph.WIN_PROGRAM_EXE_HMETIS_PATH)
                return

            raise h_exception.SoftwareIsNotSupportedOnSystemException(self.__software_enum.name)

        # Linux
        elif env.is_linux():
            pass    # TODO

        # Mac
        elif env.is_mac():
            pass    # TODO

        # Undefined
        raise c_exception.FunctionNotImplementedException("check_files_and_folders", f"not implemented for this OS ({env.get_os().name})")

    def __generate_key_cache(self, clause_id_set: Set[int], ignored_literal_set: Set[int]) -> str:
        """
        Generate a key for caching
        """

        pass

    # region hMETIS
    def __create_hypergraph_hmetis_exe(self, clause_id_set: Set[int], ignored_literal_set: Set[int]) -> Tuple[str, Dict[int, int]]:
        """
        Create an input file with the hypergraph for hMETIS.exe.
        Hypergraph's nodes (clauses) are restricted to the clause_id_set and hyperedges (variables) are restricted to all
        variables except those in the ignored_literal_set.
        :param clause_id_set: the subset of clauses
        :param ignored_literal_set: the ignored literals
        :return: (file string, mapping from node_id (file) to clause_id (CNF))
        """

        clause_id_node_id_dictionary: Dict[int, int] = dict()   # Mapping clause_id -> node_id
        node_id_clause_id_dictionary: Dict[int, int] = dict()   # Mapping node_id -> clause_id

        number_of_nodes = 0
        number_of_hyperedges = 0
        string_hyperedge = "% Hyperedges"
        string_weight = "% Weights"
        variable_set = self.__variable_set.difference(ignored_literal_set)

        # Hyperedges
        for variable in variable_set:
            occurrence_list = (self.__hypergraph_dictionary[variable]).intersection(clause_id_set)
            # The variable is not in the hypergraph
            if not occurrence_list:
                continue

            number_of_hyperedges += 1
            line_temp = [self.__get_hyperedge_weight(variable)]
            for clause_id in occurrence_list:
                # Add to the mapping
                if clause_id not in clause_id_node_id_dictionary:
                    number_of_nodes += 1
                    clause_id_node_id_dictionary[clause_id] = number_of_nodes
                    node_id_clause_id_dictionary[number_of_nodes] = clause_id

                line_temp.append(clause_id_node_id_dictionary[clause_id])

            string_hyperedge = "\n".join((string_hyperedge, " ".join(map(str, line_temp))))

        # Weights
        for node_id in range(1, number_of_nodes + 1):
            string_weight = "\n".join((string_weight, str(self.__get_node_weight(node_id_clause_id_dictionary[node_id]))))

        string_result = "\n".join((f"{number_of_hyperedges} {number_of_nodes} 11",
                                   string_hyperedge,
                                   string_weight))

        return string_result, node_id_clause_id_dictionary

    def __get_cut_set_hmetis_exe(self, clause_id_set: Set[int], ignored_literal_set: Set[int]) -> Set[int]:
        """
        Compute a cut set using hMETIS.exe
        :param clause_id_set: the subset of clauses
        :param ignored_literal_set: the ignored literals
        :return: a cut set of the hypergraph
        """

        file_string, node_id_clause_id_dictionary = self.__create_hypergraph_hmetis_exe(clause_id_set, ignored_literal_set)

        # Delete temp files
        Path(Hypergraph.INPUT_FILE_EXE_HMETIS_PATH).unlink(missing_ok=True)
        Path(Hypergraph.OUTPUT_FILE_EXE_HMETIS_PATH).unlink(missing_ok=True)

        # Save the input file
        with open(Hypergraph.INPUT_FILE_EXE_HMETIS_PATH, "w", encoding="utf8") as input_file:
            input_file.write(file_string)

        devnull = open(os.devnull, 'w')
        subprocess.run([Hypergraph.WIN_PROGRAM_EXE_HMETIS_PATH, Hypergraph.INPUT_FILE_EXE_HMETIS_PATH, str(2), str(100 * self.__ub_factor)],
                       stdout=devnull, stderr=devnull)

        # The output file has not been generated => an error occurred
        if not Path(Hypergraph.OUTPUT_FILE_EXE_HMETIS_PATH).exists():
            raise h_exception.SomethingWrongException("the output file from hMETIS.exe has not been generated => an error occurred")

        # Get the cut set
        variable_partition_0_set = set()
        variable_partition_1_set = set()
        with open(Hypergraph.OUTPUT_FILE_EXE_HMETIS_PATH, "r", encoding="utf8") as output_file:
            for line_id, line in enumerate(output_file.readlines()):
                try:
                    partition_temp = int(line)
                except ValueError:
                    raise h_exception.SomethingWrongException(f"partition ({line}) in the output file from hMETIS.exe is not a number")

                if partition_temp != 0 and partition_temp != 1:
                    raise h_exception.SomethingWrongException(f"invalid partition ({partition_temp}) in the output file from hMETIS.exe")

                literal_set_temp = self.__cnf._get_clause(node_id_clause_id_dictionary[line_id + 1])
                variable_set_temp = map(lambda l: abs(l), literal_set_temp)

                if partition_temp == 0:
                    variable_partition_0_set.update(variable_set_temp)
                else:
                    variable_partition_1_set.update(variable_set_temp)

        cut_set = variable_partition_0_set.intersection(variable_partition_1_set)
        cut_set.difference_update(ignored_literal_set)

        # Delete temp files
        Path(Hypergraph.INPUT_FILE_EXE_HMETIS_PATH).unlink(missing_ok=True)
        Path(Hypergraph.OUTPUT_FILE_EXE_HMETIS_PATH).unlink(missing_ok=True)

        return cut_set
    # endregion
    # endregion

    # region Public method
    def get_cut_set(self, clause_id_set: Set[int], ignored_literal_list: List[int]) -> Set[int]:
        """
        Create a hypergraph, where nodes (clauses) are restricted to the clause_id_set and
        hyperedges (variables) are restricted to all variables except those in the ignored_literal_list.
        :param clause_id_set: the subset of clauses
        :param ignored_literal_list: the ignored literals (a partial assignment)
        :return: a cut set of the hypergraph
        """

        ignored_literal_set = set()
        for literal in ignored_literal_list:
            variable = abs(literal)
            if variable in self.__variable_set:
                ignored_literal_set.add(variable)
                ignored_literal_set.add(-variable)

        cut_set = set()
        self.__set_dynamic_weights(clause_id_set, ignored_literal_set)

        # TODO Cache

        # Windows -> hMETIS.exe
        if env.is_windows():
            cut_set = self.__get_cut_set_hmetis_exe(clause_id_set, ignored_literal_set)

        # TODO Cache

        return cut_set
    # endregion

    # region Magic method
    def __str__(self):
        string_temp = "".join(f"Number of nodes: {self.number_of_nodes}")
        string_temp = "\n".join((string_temp, f"Number of hyperedges: {self.number_of_hyperedges}"))

        return string_temp
    # endregion

    # region Property
    @property
    def number_of_nodes(self):
        return self.__number_of_nodes

    @property
    def number_of_hyperedges(self):
        return self.__number_of_hyperedges
    # endregion
