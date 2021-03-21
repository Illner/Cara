# Import
import os
import mmh3
import subprocess
from pathlib import Path
from formula.cnf import Cnf
import other.environment as env
from compiler.solver import Solver
from typing import Set, Dict, List, Tuple, Union
from formula.incidence_graph import IncidenceGraph
from compiler_statistics.compiler.hypergraph_partitioning_statistics import HypergraphPartitioningStatistics

# Import exception
import exception.cara_exception as c_exception
import exception.compiler.hypergraph_partitioning_exception as hp_exception

# Import enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


class HypergraphPartitioning:
    """
    Hypergraph partitioning
    """

    """
    Private Cnf cnf
    Private float ub_factor
    Private int subsumed_threshold
    Private int total_number_of_nodes
    Private int total_number_of_hyperedges
    
    Private HypergraphPartitioningStatistics statistics
    
    Private HypergraphPartitioningCacheEnum cache_enum
    Private HypergraphPartitioningSoftwareEnum software_enum
    Private HypergraphPartitioningNodeWeightEnum node_weight_enum
    Private HypergraphPartitioningHyperedgeWeightEnum hyperedge_weight_enum
    Private HypergraphPartitioningVariableSimplificationEnum variable_simplification_enum
    
    Private Tuple<int, int> limit_number_of_clauses_cache    # (lower_bound, upper_bound) - None = no limit
    Private Tuple<int, int> limit_number_of_variables_cache  # (lower_bound, upper_bound) - None = no limit
    
    Private Dict<int, int> node_weight_dictionary       # key: node = clause's id, value: the weight of the clause
    Private Dict<int, int> hyperedge_weight_dictionary  # key: edge = variable, value: the weight of the variable
    
    Private Dict<int, Set<int>> cut_set_cache           # key = hash, value = a cut set
    """

    # Static variable - Path
    __TEMP_DIRECTORY_PATH = Path(os.path.join(os.getcwd(), "temp"))
    __INPUT_FILE_EXE_HMETIS_PATH = Path(os.path.join(__TEMP_DIRECTORY_PATH, "input_file_hypergraph.graph"))
    __OUTPUT_FILE_1_EXE_HMETIS_PATH = Path(str(__INPUT_FILE_EXE_HMETIS_PATH) + ".part.1")
    __OUTPUT_FILE_2_EXE_HMETIS_PATH = Path(str(__INPUT_FILE_EXE_HMETIS_PATH) + ".part.2")
    __WIN_PROGRAM_EXE_HMETIS_PATH = Path(os.path.join(os.getcwd(), "external", "hypergraph_partitioning", "hMETIS", "win", "shmetis.exe"))

    def __init__(self, cnf: Cnf,
                 ub_factor: float,
                 subsumed_threshold: Union[int, None],
                 cache_enum: hpc_enum.HypergraphPartitioningCacheEnum,
                 software_enum: hps_enum.HypergraphPartitioningSoftwareEnum,
                 node_weight_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum,
                 hyperedge_weight_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum,
                 variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum,
                 limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]],
                 limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]],
                 statistics: Union[HypergraphPartitioningStatistics, None] = None):
        # Statistics
        if statistics is None:
            self.__statistics: HypergraphPartitioningStatistics = HypergraphPartitioningStatistics()
        else:
            self.__statistics: HypergraphPartitioningStatistics = statistics

        self.__cnf: Cnf = cnf
        self.__subsumed_threshold: Union[int, None] = subsumed_threshold
        self.__total_number_of_nodes: int = cnf.real_number_of_clauses
        self.__total_number_of_hyperedges: int = cnf.number_of_variables

        self.__cache_enum: hpc_enum.HypergraphPartitioningCacheEnum = cache_enum
        self.__software_enum: hps_enum.HypergraphPartitioningSoftwareEnum = software_enum
        self.__variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum = variable_simplification_enum
        self.__node_weight_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum = node_weight_enum
        self.__hyperedge_weight_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum = hyperedge_weight_enum

        self.__cut_set_cache: Dict[int, Set[int]] = dict()

        # limit_number_of_clauses_cache
        lnocc_l_temp = limit_number_of_clauses_cache[0]
        lnocc_u_temp = limit_number_of_clauses_cache[1]
        if (lnocc_l_temp is not None) and (lnocc_u_temp is not None) and (lnocc_l_temp > lnocc_u_temp):
            raise hp_exception.InvalidLimitCacheException(lnocc_l_temp, lnocc_u_temp, "limit_number_of_clauses_cache")
        self.__limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]] = limit_number_of_clauses_cache

        # limit_number_of_variables_cache
        lnovc_l_temp = limit_number_of_variables_cache[0]
        lnovc_u_temp = limit_number_of_variables_cache[1]
        if (lnovc_l_temp is not None) and (lnovc_u_temp is not None) and (lnovc_l_temp > lnovc_u_temp):
            raise hp_exception.InvalidLimitCacheException(lnovc_l_temp, lnovc_u_temp, "limit_number_of_variables_cache")
        self.__limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]] = limit_number_of_variables_cache

        # UBfactor
        ub_factor = round(ub_factor, 2)
        if ub_factor < 0.01 or ub_factor > 0.49:    # 1% - 49%
            raise hp_exception.InvalidUBfactorException(ub_factor)
        self.__ub_factor: float = ub_factor

        # Weights
        self.__node_weight_dictionary: Dict[int, int] = dict()
        self.__hyperedge_weight_dictionary: Dict[int, int] = dict()

        self.__check_files_and_directories()
        self.__set_static_weights()

    # region Private method
    def __check_files_and_directories(self) -> None:
        """
        Check if all necessary files and directories exist.
        If some file is missing, raise an exception (FileIsMissingException).
        If the chosen software is not supported on the system, raise an exception (SoftwareIsNotSupportedOnSystemException).
        :return: None
        """

        # Windows
        if env.is_windows():
            # hMETIS
            if self.__software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS:
                HypergraphPartitioning.__TEMP_DIRECTORY_PATH.mkdir(exist_ok=True)

                # The exe has not been found
                if not HypergraphPartitioning.__WIN_PROGRAM_EXE_HMETIS_PATH.exists():
                    raise hp_exception.FileIsMissingException(HypergraphPartitioning.__WIN_PROGRAM_EXE_HMETIS_PATH)
                return

            raise hp_exception.SoftwareIsNotSupportedOnSystemException(self.__software_enum.name)

        # Linux
        elif env.is_linux():
            pass    # TODO Linux

        # Mac
        elif env.is_mac():
            pass    # TODO Mac

        # Undefined
        raise c_exception.FunctionNotImplementedException("check_files_and_directories", f"not implemented for this OS ({env.get_os().name})")

    def __variable_simplification(self, solver: Solver, assignment: List[int]) -> Dict[int, Set[int]]:
        """
        Compute variable simplification using implicit unit propagation
        :param solver: the solver
        :param assignment: the (partial) assignment (for the solver)
        :return: a dictionary where a key is a variable (representant),
        and the value is a set of variables that can be merged with the variable to reduce the hypergraph size
        """

        # None
        if self.__variable_simplification_enum == hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.NONE:
            return dict()

        self.__statistics.variable_simplification.start_stopwatch()     # timer (start)

        implicit_bcp_dictionary = solver.implicit_unit_propagation(assignment)

        # The formula is unsatisfiable (it should not happen at all)
        if implicit_bcp_dictionary is None:
            self.__statistics.variable_simplification.stop_stopwatch()  # timer (stop)
            return dict()

        # EQUIV_SIMPL
        if self.__variable_simplification_enum == hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL:
            dominated_variable_set = set()
            equivalence_dictionary: Dict[int, Set[int]] = dict()

            for var in implicit_bcp_dictionary:
                first_temp, second_temp = implicit_bcp_dictionary[var]

                # var is an implied "variable" (should not happen if implicit unit propagation is used for implied literals)
                if first_temp is None:
                    first_temp = set()
                if second_temp is None:
                    second_temp = set()

                if len(first_temp) > len(second_temp):
                    first_temp, second_temp = second_temp, first_temp

                for lit in first_temp:
                    if -lit in second_temp:
                        var_temp = abs(lit)

                        if var not in equivalence_dictionary:
                            equivalence_dictionary[var] = {var_temp}
                        else:
                            equivalence_dictionary[var].add(var_temp)

                        dominated_variable_set.add(var_temp)

            for var in dominated_variable_set:
                if var in equivalence_dictionary:
                    del equivalence_dictionary[var]

            self.__statistics.variable_simplification.stop_stopwatch()  # timer (stop)
            return equivalence_dictionary

        self.__statistics.variable_simplification.stop_stopwatch()  # timer (stop)
        raise c_exception.FunctionNotImplementedException("variable_simplification",
                                                          f"this type of variable simplification ({self.__variable_simplification_enum.name}) is not implemented")

    def __subsumption(self, incidence_graph: IncidenceGraph) -> Set[int]:
        """
        Return a set of subsumed clauses
        :param incidence_graph: the incidence graph
        :return: a set of subsumed clauses
        """

        self.__statistics.subsumption.start_stopwatch()     # timer (start)

        subsumed_clause_set = set()
        neighbour_dictionary: [int, Set[int]] = dict()   # Cache
        clause_id_list = incidence_graph.clause_id_list()

        for i, clause_a in enumerate(clause_id_list):
            # Neighbours
            if clause_a in neighbour_dictionary:
                variable_set_a = neighbour_dictionary[clause_a]
            else:
                variable_set_a = incidence_graph.clause_id_neighbour_set(clause_a)
                neighbour_dictionary[clause_a] = variable_set_a

            for j in range(i + 1, len(clause_id_list)):
                clause_b = clause_id_list[j]

                if clause_b in subsumed_clause_set:
                    continue

                # Neighbours
                if clause_b in neighbour_dictionary:
                    variable_set_b = neighbour_dictionary[clause_b]
                else:
                    variable_set_b = incidence_graph.clause_id_neighbour_set(clause_b)
                    neighbour_dictionary[clause_b] = variable_set_b

                a_subset_b = variable_set_a.issubset(variable_set_b)
                b_subset_a = variable_set_b.issubset(variable_set_a)

                # Clauses are the same
                if a_subset_b and b_subset_a:
                    if clause_a < clause_b:
                        subsumed_clause_set.add(clause_a)
                    else:
                        subsumed_clause_set.add(clause_b)

                    continue

                # Clause A is subsumed
                if a_subset_b:
                    subsumed_clause_set.add(clause_a)

                    continue

                # Clause B is subsumed
                if b_subset_a:
                    subsumed_clause_set.add(clause_b)

                    continue

        self.__statistics.subsumption.stop_stopwatch()      # timer (stop)
        return subsumed_clause_set

    # region Weights
    def __set_static_weights(self) -> None:
        """
        Initialize the static weights.
        If the type of weights is not STATIC, nothing happens.
        Variable: node_weight_dictionary, hyperedge_weight_dictionary
        :return: None
        """

        self.__statistics.set_static_weights.start_stopwatch()  # timer (start)

        # Node's weight
        if self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.STATIC:
            for node_id in range(self.__total_number_of_nodes):
                self.__node_weight_dictionary[node_id] = 1  # TODO STATIC

        # Hyperedge's weight
        if self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.STATIC:
            for hyperedge_id in range(1, self.__total_number_of_hyperedges + 1):
                self.__hyperedge_weight_dictionary[hyperedge_id] = 1    # TODO STATIC

        self.__statistics.set_static_weights.stop_stopwatch()   # timer (stop)

    def __set_dynamic_weights(self, incidence_graph: IncidenceGraph) -> None:
        """
        Initialize the dynamic weights based on the incidence graph.
        If the type of weights is not Dynamic, nothing happens.
        Variable: node_weight_dictionary, hyperedge_weight_dictionary
        :param incidence_graph: the incidence graph
        :return: None
        """

        self.__statistics.set_dynamic_weights.start_stopwatch()     # timer (start)

        # Node's weight
        if self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.DYNAMIC:
            self.__node_weight_dictionary = dict()
            pass    # TODO DYNAMIC

        # Hyperedge's weight
        if self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.DYNAMIC:
            self.__hyperedge_weight_dictionary = dict()
            pass    # TODO DYNAMIC

        self.__statistics.set_dynamic_weights.stop_stopwatch()      # timer (stop)

    def __get_node_weight(self, node_id: int) -> int:
        """
        Return the weight of the node based on the node_weight_enum.
        If the node does not exist in the hypergraph, raise an exception (NodeDoesNotExistException).
        :param node_id: the node's ID
        :return: the weight of the node
        """

        # The node does not exist in the hypergraph
        if (node_id < 0) or (node_id >= self.__total_number_of_nodes):
            raise hp_exception.NodeDoesNotExistException(node_id)

        # No weights
        if self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE:
            return 1

        # STATIC/DYNAMIC weights
        if (self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.STATIC) or \
           (self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.DYNAMIC):
            # Something wrong
            if node_id not in self.__node_weight_dictionary:
                raise hp_exception.NodeDoesNotExistException(node_id)

            return self.__node_weight_dictionary[node_id]

        raise c_exception.FunctionNotImplementedException("get_node_weight",
                                                          f"this type of weights ({self.__node_weight_enum.name}) is not implemented")

    def __get_hyperedge_weight(self, hyperedge_id: int) -> int:
        """
        Return the weight of the hyperedge based on the hyperedge_weight_enum.
        If the hyperedge does not exist in the hypergraph, raise an exception (HyperedgeDoesNotExistException).
        :param hyperedge_id: the hyperedge's ID
        :return: the weight of the hyperedge
        """

        # The hyperedge does not exist in the hypergraph
        if (hyperedge_id < 1) or (hyperedge_id > self.__total_number_of_hyperedges):
            raise hp_exception.HyperedgeDoesNotExistException(hyperedge_id)

        # No weights
        if self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE:
            return 1

        # STATIC/DYNAMIC weights
        if (self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.STATIC) or \
           (self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.DYNAMIC):
            # Something wrong
            if hyperedge_id not in self.__hyperedge_weight_dictionary:
                raise hp_exception.HyperedgeDoesNotExistException(hyperedge_id)

            return self.__hyperedge_weight_dictionary[hyperedge_id]

        raise c_exception.FunctionNotImplementedException("get_hyperedge_weight",
                                                          f"this type of weights ({self.__hyperedge_weight_enum.name}) is not implemented")
    # endregion

    # region Cache
    def __add_cut_set_cache(self, key: int, cut_set: Set[int]) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        Cache: cut_set_cache
        :param key: the key
        :param cut_set: the value
        :return: None
        """

        self.__cut_set_cache[key] = cut_set

    def __get_cut_set_cache(self, key: int) -> Union[Set[int], None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        Cache: cut_set_cache
        :param key: the key
        :return: The record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if (key is None) or (key not in self.__cut_set_cache):
            return None

        return self.__cut_set_cache[key]

    def __clear_cut_set_cache(self) -> None:
        """
        Clear the cache
        Cache: cut_set_cache
        :return: None
        """

        self.__cut_set_cache = dict()

    def __generate_key_cache(self, incidence_graph: IncidenceGraph) -> Tuple[int, Tuple[Dict[int, int], Dict[int, int]]]:
        """
        Generate a key for caching
        Variable property: occurrence, mean, variance (optional)
        :return: the generated key based on the incidence graph and both mappings between variables (variable_id -> order_id, order_id -> variable_id)
        """

        self.__statistics.generate_key_cache.start_stopwatch()      # timer (start)

        # Variance
        use_variance = False
        if self.__cache_enum == hpc_enum.HypergraphPartitioningCacheEnum.ISOMORFISM_VARIANCE:
            use_variance = True

        # Initialize
        occurrence_dictionary: Dict[int, int] = dict()
        mean_dictionary: Dict[int, float] = dict()
        variance_dictionary: Dict[int, float] = dict()

        # Compute occurrences and means
        for variable in incidence_graph.variable_set():
            clause_id_set = incidence_graph.variable_neighbour_set(variable)

            # Occurrence
            occurrence_dictionary[variable] = len(clause_id_set)

            # Mean
            mean_temp = 0
            for clause_id in clause_id_set:
                mean_temp += incidence_graph.number_of_neighbours_clause_id(clause_id)
            # mean_temp = mean_temp / len(clause_id_set)
            mean_dictionary[variable] = mean_temp

        # Compute variances
        if use_variance:
            for variable in incidence_graph.variable_set():
                clause_id_set = incidence_graph.variable_neighbour_set(variable)
                mean_temp = mean_dictionary[variable]

                variance_temp = 0
                for clause_id in clause_id_set:
                    variance_temp += (incidence_graph.number_of_neighbours_clause_id(clause_id) - mean_temp) ** 2
                # variance_temp = variance_temp / (len(clause_id_set) - 1)
                variance_dictionary[variable] = variance_temp

        def variable_order(ordering: List[List[int]], mapping_dictionary: Dict[int, float]) -> List[List[int]]:
            result_ordering = []

            for group_func in ordering:
                last_value = None
                new_group = []

                for var_func in sorted(group_func, key=lambda v_func: mapping_dictionary[v_func]):
                    value = mapping_dictionary[var_func]

                    if (last_value is None) or (value == last_value):
                        new_group.append(var_func)
                    else:
                        result_ordering.append(new_group)
                        new_group = [var_func]

                    last_value = value

                result_ordering.append(new_group)

            return result_ordering

        variable_ordering = [incidence_graph.variable_list()]
        variable_ordering = variable_order(variable_ordering, occurrence_dictionary)
        variable_ordering = variable_order(variable_ordering, mean_dictionary)
        if use_variance:
            variable_ordering = variable_order(variable_ordering, variance_dictionary)

        # Mapping
        variable_id_order_id_dictionary: Dict[int, int] = dict()  # Mapping variable_id -> order_id
        order_id_variable_id_dictionary: Dict[int, int] = dict()  # Mapping order_id -> variable_id

        # Create an ordering
        counter_temp = 0
        for group in variable_ordering:
            for var in sorted(group):
                variable_id_order_id_dictionary[var] = counter_temp
                order_id_variable_id_dictionary[counter_temp] = var
                counter_temp += 1

        variable_clause_list = []
        for clause_id in incidence_graph.clause_id_set(multi_occurrence=False):
            variable_set = incidence_graph.clause_id_neighbour_set(clause_id)
            variable_sorted_list = sorted(map(lambda v: variable_id_order_id_dictionary[v], variable_set))
            variable_clause_list.append(variable_sorted_list)

        key_string = ",0,".join([",".join(map(str, variable_clause)) for variable_clause in sorted(variable_clause_list)])
        key = mmh3.hash(key_string)

        self.__statistics.generate_key_cache.stop_stopwatch()       # timer (stop)
        return key, (variable_id_order_id_dictionary, order_id_variable_id_dictionary)
    # endregion

    # region hMETIS.exe
    def __create_hypergraph_hmetis_exe(self, incidence_graph: IncidenceGraph) -> Tuple[str, Dict[int, int]]:
        """
        Create an input file string with the hypergraph for hMETIS.exe based on the incidence graph
        :param incidence_graph: the incidence graph
        :return: (file string, mapping from node_id (file) to clause_id (CNF))
        """

        # Mapping
        clause_id_node_id_dictionary: Dict[int, int] = dict()   # Mapping clause_id -> node_id
        node_id_clause_id_dictionary: Dict[int, int] = dict()   # Mapping node_id -> clause_id

        number_of_nodes = 0  # incidence_graph.number_of_clauses()
        number_of_hyperedges = incidence_graph.number_of_variables()

        # Hyperedges
        line_hyperedge = []
        for variable in incidence_graph.variable_set():
            clause_id_set = incidence_graph.variable_neighbour_set(variable)

            line_temp = [self.__get_hyperedge_weight(variable)]
            for clause_id in clause_id_set:
                # Add to the mapping
                if clause_id not in clause_id_node_id_dictionary:
                    number_of_nodes += 1
                    clause_id_node_id_dictionary[clause_id] = number_of_nodes
                    node_id_clause_id_dictionary[number_of_nodes] = clause_id

                line_temp.append(clause_id_node_id_dictionary[clause_id])

            line_hyperedge.append(line_temp)

        string_hyperedge = "\n".join([" ".join(map(str, hyperedge)) for hyperedge in line_hyperedge])

        # Weights
        line_weight = []
        for node_id in range(1, number_of_nodes + 1):
            line_weight.append(self.__get_node_weight(node_id_clause_id_dictionary[node_id]))

        string_weight = "\n".join(map(str, line_weight))

        string_result = "\n".join((f"{number_of_hyperedges} {number_of_nodes} 11",
                                   string_hyperedge,
                                   string_weight))

        return string_result, node_id_clause_id_dictionary

    def __get_cut_set_hmetis_exe(self, incidence_graph: IncidenceGraph) -> Set[int]:
        """
        Compute a cut set using hMETIS.exe
        :param incidence_graph: the incidence graph
        :return: a cut set of the hypergraph
        """

        file_string, node_id_clause_id_dictionary = self.__create_hypergraph_hmetis_exe(incidence_graph)

        # Delete temp files
        HypergraphPartitioning.__INPUT_FILE_EXE_HMETIS_PATH.unlink(missing_ok=True)
        HypergraphPartitioning.__OUTPUT_FILE_1_EXE_HMETIS_PATH.unlink(missing_ok=True)
        HypergraphPartitioning.__OUTPUT_FILE_2_EXE_HMETIS_PATH.unlink(missing_ok=True)

        # Save the input file
        with open(HypergraphPartitioning.__INPUT_FILE_EXE_HMETIS_PATH, "w", encoding="utf8") as input_file:
            input_file.write(file_string)

        devnull = open(os.devnull, 'w')
        subprocess.run([HypergraphPartitioning.__WIN_PROGRAM_EXE_HMETIS_PATH,
                        HypergraphPartitioning.__INPUT_FILE_EXE_HMETIS_PATH,
                        str(2), str(100 * self.__ub_factor)],
                       stdout=devnull, stderr=devnull)
        # TODO error => str

        # A cut set does not exist (because of balance etc.)
        if HypergraphPartitioning.__OUTPUT_FILE_1_EXE_HMETIS_PATH.exists():
            HypergraphPartitioning.__INPUT_FILE_EXE_HMETIS_PATH.unlink(missing_ok=True)
            HypergraphPartitioning.__OUTPUT_FILE_1_EXE_HMETIS_PATH.unlink(missing_ok=True)

            return set()

        # The output file has not been generated => an error occurred
        if not HypergraphPartitioning.__OUTPUT_FILE_2_EXE_HMETIS_PATH.exists():
            raise hp_exception.SomethingWrongException("the output file from hMETIS.exe has not been generated => an error occurred")

        # Get the cut set
        variable_partition_0_set = set()
        variable_partition_1_set = set()
        with open(HypergraphPartitioning.__OUTPUT_FILE_2_EXE_HMETIS_PATH, "r", encoding="utf8") as output_file:
            for line_id, line in enumerate(output_file.readlines()):
                try:
                    partition_temp = int(line)
                except ValueError:
                    raise hp_exception.SomethingWrongException(f"partition ({line}) in the output file from hMETIS.exe is not a number")

                if partition_temp != 0 and partition_temp != 1:
                    raise hp_exception.SomethingWrongException(f"invalid partition ({partition_temp}) in the output file from hMETIS.exe")

                variable_set_temp = incidence_graph.clause_id_neighbour_set(node_id_clause_id_dictionary[line_id + 1])

                if partition_temp == 0:
                    variable_partition_0_set.update(variable_set_temp)
                else:
                    variable_partition_1_set.update(variable_set_temp)

        cut_set = variable_partition_0_set.intersection(variable_partition_1_set)

        # Delete temp files
        HypergraphPartitioning.__INPUT_FILE_EXE_HMETIS_PATH.unlink(missing_ok=True)
        HypergraphPartitioning.__OUTPUT_FILE_2_EXE_HMETIS_PATH.unlink(missing_ok=True)

        return cut_set
    # endregion
    # endregion

    # region Public method
    def get_cut_set(self, incidence_graph: IncidenceGraph, solver: Solver, assignment: List[int]) -> Set[int]:
        """
        Create a hypergraph based on the incidence graph
        :param incidence_graph: the incidence graph
        :param solver: the solver (in case equivSimpl is used)
        :param assignment: the (partial) assignment (for the solver)
        :return: a cut set of the hypergraph
        """

        self.__statistics.get_cut_set.start_stopwatch()     # timer (start)

        self.__set_dynamic_weights(incidence_graph)

        self.reduce_incidence_graph(incidence_graph, solver, assignment)

        # Only one clause remains => all variables are in the cut set
        if incidence_graph.number_of_clauses() == 1:
            cut_set = incidence_graph.variable_set(copy=True)
            self.remove_reduction_incidence_graph(incidence_graph)

            self.__statistics.get_cut_set.stop_stopwatch()      # timer (stop)
            return cut_set

        # Cache
        key = None                              # initialization
        variable_id_order_id_dictionary = None  # initialization

        result_cache_cut_set, result_cache_key = self.check_cache(incidence_graph)
        # A cut set has been found
        if result_cache_cut_set is not None:
            self.remove_reduction_incidence_graph(incidence_graph)

            self.__statistics.cached.add_count(1)  # counter
            self.__statistics.get_cut_set.stop_stopwatch()  # timer (stop)
            return result_cache_cut_set
        else:
            if result_cache_key is not None:
                key, (variable_id_order_id_dictionary, _) = result_cache_key

            self.__statistics.cached.add_count(0)  # counter

        cut_set = set()

        # Windows -> hMETIS.exe
        if env.is_windows():
            cut_set = self.__get_cut_set_hmetis_exe(incidence_graph)

        # A cut set does not exist (because of balance etc.) => a variable with the most occurrences is selected
        if not cut_set:
            cut_set = {incidence_graph.variable_with_most_occurrences()}

        # Cache
        if key is not None:
            cut_set_cache = set()
            for var in cut_set:
                cut_set_cache.add(variable_id_order_id_dictionary[var])

            self.__add_cut_set_cache(key, cut_set_cache)

        self.remove_reduction_incidence_graph(incidence_graph)

        self.__statistics.get_cut_set.stop_stopwatch()  # timer (stop)
        return cut_set

    def check_cache(self, incidence_graph: IncidenceGraph) -> Tuple[Union[Set[int], None], Union[Tuple[int, Tuple[Dict[int, int], Dict[int, int]]], None]]:
        """
        Generate a key for caching based on the incidence graph and check if a cut set exists in the cache
        :return: (cut set, key, (mapping, mapping))
        """

        if not self.cache_can_be_used(incidence_graph):
            return None, None

        result_cache = self.__generate_key_cache(incidence_graph)
        key, (variable_id_order_id_dictionary, order_id_variable_id_dictionary) = result_cache
        value = self.__get_cut_set_cache(key)

        # A cut set has not been found in the cache
        if value is None:
            return None, result_cache
        # A cut set has been found in the cache
        else:
            cut_set_cache = set()
            for var in value:
                cut_set_cache.add(order_id_variable_id_dictionary[var])

            return cut_set_cache, result_cache

    def reduce_incidence_graph(self, incidence_graph: IncidenceGraph, solver: Solver, assignment: List[int]) -> None:
        """
        Do a variable simplification and subsumption (if the limit is satisfied)
        :return: None
        """

        # Variable simplification
        variable_simplification_dictionary = self.__variable_simplification(solver, assignment)
        incidence_graph.merge_variable_simplification(variable_simplification_dictionary)

        # Subsumption
        if (self.__subsumed_threshold is None) or (incidence_graph.number_of_clauses() <= self.__subsumed_threshold):
            subsumed_clause_set = self.__subsumption(incidence_graph)
            incidence_graph.remove_subsumed_clause_set(subsumed_clause_set)

    def cache_can_be_used(self, incidence_graph: IncidenceGraph) -> bool:
        """
        :return: True if a cache can be used. Otherwise, False is returned.
        """

        if self.__cache_enum == hpc_enum.HypergraphPartitioningCacheEnum.NONE:
            return False

        # Check limits - number of clauses
        number_of_clauses = incidence_graph.number_of_clauses()
        lnocc_l_temp = self.__limit_number_of_clauses_cache[0]
        lnocc_u_temp = self.__limit_number_of_clauses_cache[1]
        if ((lnocc_l_temp is not None) and (number_of_clauses < lnocc_l_temp)) or \
           ((lnocc_u_temp is not None) and (number_of_clauses > lnocc_u_temp)):
            return False

        # Check limits - number of variables
        number_of_variables = incidence_graph.number_of_variables()
        lnovc_l_temp = self.__limit_number_of_variables_cache[0]
        lnovc_u_temp = self.__limit_number_of_variables_cache[1]
        if ((lnovc_l_temp is not None) and (number_of_variables < lnovc_l_temp)) or \
           ((lnovc_u_temp is not None) and (number_of_variables > lnovc_u_temp)):
            return False

        return True
    # endregion

    # region Static method
    @staticmethod
    def remove_reduction_incidence_graph(incidence_graph: IncidenceGraph) -> None:
        incidence_graph.restore_backup_subsumption()                # Subsumption
        incidence_graph.restore_backup_variable_simplification()    # Variable simplification
    # endregion
