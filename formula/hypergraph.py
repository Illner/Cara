# Import
import os
import subprocess
from pathlib import Path
from formula.cnf import Cnf
import other.environment as env
from typing import Set, Dict, List, Tuple, Union

# Import exception
import exception.cara_exception as c_exception
import exception.formula.hypergraph_exception as h_exception

# Import enum
import formula.enum.hypergraph_cache_enum as hc_enum
import formula.enum.hypergraph_software_enum as hs_enum
import formula.enum.hypergraph_weight_type_enum as hw_enum

# TODO use incidence graph


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
    
    Private Dict<str, Set<int>> cut_set_cache           # key = {number}+
    
    Private Tuple<int, int> limit_number_of_clauses_cache    # (lower_bound, upper_bound) - None = no limit
    Private Tuple<int, int> limit_number_of_variables_cache  # (lower_bound, upper_bound) - None = no limit
    
    Private Dict<int, int> node_weight_dictionary       # key: node = clause's id, value: the weight of the clause
    Private Dict<int, int> hyperedge_weight_dictionary  # key: edge = variable, value: the weight of the variable
    
    Private Dict<int, Set<int>> hypergraph_dictionary   # key: variable, value: a set of clauses where the variable appears
    """

    # Static variable - Path
    TEMP_FOLDER_PATH = os.path.join(os.getcwd(), "temp")
    INPUT_FILE_EXE_HMETIS_PATH = os.path.join(TEMP_FOLDER_PATH, "input_file_hypergraph.graph")
    OUTPUT_FILE_EXE_HMETIS_PATH = INPUT_FILE_EXE_HMETIS_PATH + ".part.2"
    WIN_PROGRAM_EXE_HMETIS_PATH = os.path.join(os.getcwd(), "external", "hypergraph_partitioning", "hMETIS", "win", "shmetis.exe")

    def __init__(self, cnf: Cnf, ub_factor: float = 0.10,
                 limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                 limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                 cache_enum: hc_enum.HypergraphCacheEnum = hc_enum.HypergraphCacheEnum.NONE,
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

        self.__cut_set_cache: Dict[str, Set[int]] = dict()

        # limit_number_of_clauses_cache
        lnocc_l_temp = limit_number_of_clauses_cache[0]
        lnocc_u_temp = limit_number_of_clauses_cache[1]
        if (lnocc_l_temp is not None) and (lnocc_u_temp is not None) and (lnocc_l_temp > lnocc_u_temp):
            raise h_exception.InvalidLimitCacheException(lnocc_l_temp, lnocc_u_temp, "limit_number_of_clauses_cache")
        self.__limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]] = limit_number_of_clauses_cache

        # limit_number_of_variables_cache
        lnovc_l_temp = limit_number_of_variables_cache[0]
        lnovc_u_temp = limit_number_of_variables_cache[1]
        if (lnovc_l_temp is not None) and (lnovc_u_temp is not None) and (lnovc_l_temp > lnovc_u_temp):
            raise h_exception.InvalidLimitCacheException(lnovc_l_temp, lnovc_u_temp, "limit_number_of_variables_cache")
        self.__limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]] = limit_number_of_variables_cache

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
            clause_temp.update(self.__cnf._get_clause_set_literal(variable))
            # Negative literal
            clause_temp.update(self.__cnf._get_clause_set_literal(-variable))

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

    def __generate_key_cache(self, clause_id_set: Set[int], variable_clause_id_dictionary: Dict[int, Set[int]],
                             use_variance: bool = True) -> Union[Tuple[str, Tuple[Dict[int, int], Dict[int, int]]], None]:
        """
        Generate a key for caching
        Variable property: occurrence, mean, variance (optional)
        :param clause_id_set: the subset of clauses
        :param variable_clause_id_dictionary: the hypergraph structure
        :param use_variance: True if variances can be used for generating the key
        :return: The generated key based on the variable_clause_id_dictionary and both mappings between variables
        (variable_id -> order_id, order_id -> variable_id).
        In case some limit (number of clauses/variables) is not satisfied, return None.
        """

        # Check limits - number of clauses
        number_of_clauses = len(clause_id_set)
        if ((self.__limit_number_of_clauses_cache[0] is not None) and (number_of_clauses < self.__limit_number_of_clauses_cache[0])) or \
           ((self.__limit_number_of_clauses_cache[1] is not None) and (number_of_clauses > self.__limit_number_of_clauses_cache[1])):
            return None

        # Check limits - number of variables
        number_of_variables = len(variable_clause_id_dictionary)
        if ((self.__limit_number_of_variables_cache[0] is not None) and (number_of_variables < self.__limit_number_of_variables_cache[0])) or \
           ((self.__limit_number_of_variables_cache[1] is not None) and (number_of_variables > self.__limit_number_of_variables_cache[1])):
            return None

        # Initialize
        occurrence_dictionary: Dict[int, int] = dict()
        mean_dictionary: Dict[int, float] = dict()
        variance_dictionary: Dict[int, float] = dict()

        # Compute occurrences and means
        for variable in variable_clause_id_dictionary:
            occurrence_list_temp = variable_clause_id_dictionary[variable]

            # Occurrence
            occurrence_dictionary[variable] = len(occurrence_list_temp)

            # Mean
            mean_temp = 0
            for clause_id in occurrence_list_temp:
                mean_temp += len(self.__cnf.get_clause(clause_id))
            # mean_temp = mean_temp / len(occurrence_list_temp)
            mean_dictionary[variable] = mean_temp

        # Compute variances
        if use_variance:
            for variable in variable_clause_id_dictionary:
                occurrence_list_temp = variable_clause_id_dictionary[variable]
                mean_temp = mean_dictionary[variable]

                variance_temp = 0
                for clause_id in occurrence_list_temp:
                    variance_temp += (len(self.__cnf.get_clause(clause_id)) - mean_temp)**2
                # variance_temp = variance_temp / (len(occurrence_list_temp) - 1)
                variance_dictionary[variable] = variance_temp

        def variable_order(ordering: List[List[int]], mapping_dictionary: Dict[int, float]) -> List[List[int]]:
            result_ordering = []

            for group in ordering:
                last_value = None
                new_group = []

                for var in sorted(group, key=lambda v: mapping_dictionary[v]):
                    value = mapping_dictionary[var]

                    if (last_value is None) or (value == last_value):
                        new_group.append(var)
                    else:
                        result_ordering.append(new_group)
                        new_group = [var]

                    last_value = value

                result_ordering.append(new_group)

            return result_ordering

        variable_ordering = [[v for v in variable_clause_id_dictionary]]
        variable_ordering = variable_order(variable_ordering, occurrence_dictionary)
        variable_ordering = variable_order(variable_ordering, mean_dictionary)
        if use_variance:
            variable_ordering = variable_order(variable_ordering, variance_dictionary)

        variable_id_order_id_dictionary: Dict[int, int] = dict()    # Mapping variable_id -> order_id
        order_id_variable_id_dictionary: Dict[int, int] = dict()    # Mapping order_id -> variable_id
        counter_temp = 0

        # Create an ordering
        for group in variable_ordering:
            for var in sorted(group):
                variable_id_order_id_dictionary[var] = counter_temp
                order_id_variable_id_dictionary[counter_temp] = var
                counter_temp += 1

        key_list = []
        for clause_id in clause_id_set:
            variable_set_temp = self.__cnf._get_variable_in_clause(clause_id)
            key_clause = 0
            for v in variable_set_temp:
                if v in variable_clause_id_dictionary:
                    key_clause += 2**(variable_id_order_id_dictionary[v])

            key_list.append(key_clause)

        key_string = ""
        for key in sorted(key_list):
            key_string = "-".join((key_string, str(key)))

        return key_string, (variable_id_order_id_dictionary, order_id_variable_id_dictionary)

    def __add_cut_set_cache(self, key: str, cut_set: Set[int]) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        :param key: the key
        :param cut_set: the value
        :return: None
        """

        self.__cut_set_cache[key] = cut_set

    def __get_cut_set_cache(self, key: str) -> Union[Set[int], None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        :param key: the key
        :return: The record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if key not in self.__cut_set_cache:
            return None

        return self.__cut_set_cache[key]

    def _clear_cut_set_cache(self) -> None:
        """
        Clear the cache
        :return: None
        """

        self.__cut_set_cache = dict()

    # region hMETIS
    def __create_hypergraph_hmetis_exe(self, variable_clause_id_dictionary: Dict[int, Set[int]]) -> Tuple[str, Dict[int, int]]:
        """
        Create an input file with the hypergraph for hMETIS.exe based on variable_clause_id_dictionary
        :param variable_clause_id_dictionary: the hypergraph structure
        :return: (file string, mapping from node_id (file) to clause_id (CNF))
        """

        clause_id_node_id_dictionary: Dict[int, int] = dict()   # Mapping clause_id -> node_id
        node_id_clause_id_dictionary: Dict[int, int] = dict()   # Mapping node_id -> clause_id

        number_of_nodes = 0
        number_of_hyperedges = 0
        string_hyperedge = "% Hyperedges"
        string_weight = "% Weights"

        # Hyperedges
        for variable in variable_clause_id_dictionary:
            occurrence_list = variable_clause_id_dictionary[variable]

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

    def __get_cut_set_hmetis_exe(self, variable_clause_id_dictionary: Dict[int, Set[int]], ignored_variable_set: Set[int]) -> Set[int]:
        """
        Compute a cut set using hMETIS.exe
        :param variable_clause_id_dictionary: the hypergraph structure
        :param ignored_variable_set: the ignored variables
        :return: a cut set of the hypergraph
        """

        file_string, node_id_clause_id_dictionary = self.__create_hypergraph_hmetis_exe(variable_clause_id_dictionary)

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
        cut_set.difference_update(ignored_variable_set)

        # Delete temp files
        Path(Hypergraph.INPUT_FILE_EXE_HMETIS_PATH).unlink(missing_ok=True)
        Path(Hypergraph.OUTPUT_FILE_EXE_HMETIS_PATH).unlink(missing_ok=True)

        return cut_set
    # endregion
    # endregion

    # region Public method
    def get_cut_set(self, clause_id_set: Set[int], ignored_literal_list: List[int], use_cache: bool = True) -> Set[int]:
        """
        Create a hypergraph, where nodes (clauses) are restricted to the clause_id_set and
        hyperedges (variables) are restricted to all variables except those in the ignored_literal_list.
        :param clause_id_set: the subset of clauses
        :param ignored_literal_list: the ignored literals (a partial assignment)
        :param use_cache: True if the cache can be used
        :return: a cut set of the hypergraph
        """

        # Ignored variable/literal set
        ignored_variable_set = set()
        ignored_literal_set = set()
        for literal in ignored_literal_list:
            variable = abs(literal)
            if variable in self.__variable_set:
                ignored_variable_set.add(variable)
                ignored_literal_set.add(variable)
                ignored_literal_set.add(-variable)

        # Variable set
        variable_set = self.__cnf.get_variable_in_clauses(clause_id_set)
        variable_set.difference_update(ignored_variable_set)

        cut_set = set()
        self.__set_dynamic_weights(clause_id_set, ignored_literal_set)

        # TODO Subsumed / Identical (with respect to variables)
        # TODO equivSimpl

        variable_clause_id_dictionary: Dict[int, Set[int]] = dict()  # key: variable, value: a set of clauses (from the clause_id_set) which contain the variable
        for variable in variable_set:
            clause_set_temp = (self.__cnf._get_clause_set_variable(variable)).intersection(clause_id_set)
            variable_clause_id_dictionary[variable] = clause_set_temp

        # Cache
        key = ""  # initialization
        variable_id_order_id_dictionary = None
        if use_cache:
            key, (variable_id_order_id_dictionary, order_id_variable_id_dictionary) = self.__generate_key_cache(clause_id_set, variable_clause_id_dictionary)
            value = self.__get_cut_set_cache(key)
            if value is not None:
                cut_set = set()
                for var in value:
                    cut_set.add(order_id_variable_id_dictionary[var])

                print("Cache!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return cut_set

        # Windows -> hMETIS.exe
        if env.is_windows():
            cut_set = self.__get_cut_set_hmetis_exe(variable_clause_id_dictionary, ignored_variable_set)

        # Cache
        if use_cache:
            cut_set_cache = set()
            for var in cut_set:
                cut_set_cache.add(variable_id_order_id_dictionary[var])

            self.__add_cut_set_cache(key, cut_set_cache)

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
