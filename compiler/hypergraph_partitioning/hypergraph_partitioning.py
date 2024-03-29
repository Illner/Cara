# Import
import os
import math
import ctypes
import warnings
import subprocess
from pathlib import Path
from formula.cnf import Cnf
from datetime import datetime
import other.environment as env
from compiler.solver import Solver
from typing import Set, Dict, List, Tuple, Union
from formula.incidence_graph import IncidenceGraph
from compiler.hypergraph_partitioning.patoh_data import PatohData
from compiler.hypergraph_partitioning.patoh_initialize_parameters import PatohInitializeParameters
from compiler_statistics.compiler.hypergraph_partitioning_statistics import HypergraphPartitioningStatistics

# Import exception
import exception.cara_exception as c_exception
import exception.compiler.hypergraph_partitioning_exception as hp_exception

# Import enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_patoh_sugparam_enum as hpps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


class HypergraphPartitioning:
    """
    Hypergraph partitioning
    """

    """
    Private Cnf cnf
    Private float imbalance_factor
    Private Set<int> hyperedge_set
    Private int subsumption_threshold
    Private int total_number_of_nodes
    Private bool disable_decomposition
    Private bool multi_occurrence_cache
    
    Private Tuple<int, int> limit_number_of_clauses_cache       # (lower_bound, upper_bound) - None = no limit
    Private Tuple<int, int> limit_number_of_variables_cache     # (lower_bound, upper_bound) - None = no limit
    
    Private Dict<int, int> node_weight_dictionary               # key: node = clause, value: the weight of the clause
    Private Dict<int, int> hyperedge_weight_dictionary          # key: edge = variable, value: the weight of the variable
    
    Private Dict<str, Set<int>> cut_set_cache                   # key: hash, value: a cut set
    
    Private HypergraphPartitioningStatistics statistics
    
    Private PatohSugparamEnum patoh_sugparam_enum
    Private HypergraphPartitioningCacheEnum cache_enum
    Private HypergraphPartitioningSoftwareEnum software_enum
    Private HypergraphPartitioningNodeWeightEnum node_weight_enum
    Private HypergraphPartitioningHyperedgeWeightEnum hyperedge_weight_enum
    Private HypergraphPartitioningVariableSimplificationEnum variable_simplification_enum
    
    Private Path input_file_hmetis_path
    Private Path output_file_1_hmetis_path
    Private Path output_file_2_hmetis_path
    
    Private PATOH_InitializeParameters
    Private PATOH_Alloc
    Private PATOH_Part
    Private PATOH_Free
    """

    # Static variable - Path
    __TEMP_DIRECTORY_PATH = Path(os.path.join(os.getcwd(), "temp"))
    # hMETIS
    __WIN_PROGRAM_HMETIS_PATH = Path(os.path.join(os.getcwd(), "external", "hypergraph_partitioning", "hMETIS", "windows", "shmetis.exe"))
    __LINUX_PROGRAM_HMETIS_PATH = Path(os.path.join(os.getcwd(), "external", "hypergraph_partitioning", "hMETIS", "linux", "shmetis"))
    # PaToH
    __LINUX_LIBRARY_PATOH_PATH = Path(os.path.join(os.getcwd(), "external", "hypergraph_partitioning", "PaToH", "linux", "libpatoh.so"))
    __MAC_OS_LIBRARY_PATOH_PATH = Path(os.path.join(os.getcwd(), "external", "hypergraph_partitioning", "PaToH", "macOS", "libpatoh.dylib"))
    # KaHyPar
    __CONFIG_KAHYPAR_PATH = Path(os.path.join(os.getcwd(), "external", "hypergraph_partitioning", "KaHyPar", "config.ini"))

    def __init__(self, cnf: Cnf,
                 imbalance_factor: Union[float, None],
                 subsumption_threshold: Union[int, None],
                 cache_enum: hpc_enum.HypergraphPartitioningCacheEnum,
                 software_enum: hps_enum.HypergraphPartitioningSoftwareEnum,
                 node_weight_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum,
                 hyperedge_weight_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum,
                 variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum,
                 multi_occurrence_cache: bool,
                 limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]],
                 limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]],
                 disable_decomposition: bool = False,
                 patoh_sugparam_enum: hpps_enum.PatohSugparamEnum = hpps_enum.PatohSugparamEnum.SPEED,
                 statistics: Union[HypergraphPartitioningStatistics, None] = None):
        # Statistics
        if statistics is None:
            self.__statistics: HypergraphPartitioningStatistics = HypergraphPartitioningStatistics(active=False)
        else:
            self.__statistics: HypergraphPartitioningStatistics = statistics

        self.__cnf: Cnf = cnf
        self.__hyperedge_set: Set[int] = cnf._variable_set
        self.__disable_decomposition: bool = disable_decomposition
        self.__multi_occurrence_cache: bool = multi_occurrence_cache
        self.__total_number_of_nodes: int = cnf.real_number_of_clauses
        self.__subsumption_threshold: Union[int, None] = subsumption_threshold

        self.__cache_enum: hpc_enum.HypergraphPartitioningCacheEnum = cache_enum
        self.__patoh_sugparam_enum: hpps_enum.PatohSugparamEnum = patoh_sugparam_enum
        self.__software_enum: hps_enum.HypergraphPartitioningSoftwareEnum = software_enum
        self.__node_weight_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum = node_weight_enum
        self.__hyperedge_weight_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum = hyperedge_weight_enum
        self.__variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum = variable_simplification_enum

        self.__cut_set_cache: Dict[str, Set[int]] = dict()

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

        # Imbalance factor
        if imbalance_factor is not None:
            imbalance_factor = round(imbalance_factor, 2)
            if (imbalance_factor < 0.01) or (imbalance_factor > 0.49):    # 1% - 49%
                raise hp_exception.InvalidImbalanceFactorException(imbalance_factor)
        self.__imbalance_factor: Union[float, None] = imbalance_factor

        # Weights
        self.__node_weight_dictionary: Dict[int, int] = dict()
        self.__hyperedge_weight_dictionary: Dict[int, int] = dict()

        self.__check_files_and_directories()
        self.__set_static_weights(initial_incidence_graph=cnf._incidence_graph)

        # hMETIS
        if self.__software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS:
            self.__create_hmetis_paths()

        # PaToH
        if self.__software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.PATOH:
            self.__load_patoh_library_and_functions()

    # region Private method
    def __create_hmetis_paths(self) -> None:
        """
        Create paths
        Path: input_file, output_file_1, output_file_2
        :return: None
        """

        now_time_str = str(datetime.now().time())
        now_postfix = now_time_str.replace(":", "_").replace(".", "_").replace(" ", "_")

        self.__input_file_hmetis_path = Path(os.path.join(HypergraphPartitioning.__TEMP_DIRECTORY_PATH, f"hmetis_hypergraph_{now_postfix}.graph"))
        self.__output_file_1_hmetis_path = Path(str(self.__input_file_hmetis_path) + ".part.1")
        self.__output_file_2_hmetis_path = Path(str(self.__input_file_hmetis_path) + ".part.2")

    def __load_patoh_library_and_functions(self) -> None:
        """
        Load the PaToH library and functions
        :return: None
        :raises SomethingWrongWithPatohLibraryException: if something is wrong with the PaToH library
        """

        library_patoh_path_temp = str(HypergraphPartitioning.__LINUX_LIBRARY_PATOH_PATH) if env.is_linux() else str(HypergraphPartitioning.__MAC_OS_LIBRARY_PATOH_PATH)

        try:
            clib = ctypes.cdll.LoadLibrary(library_patoh_path_temp)

            # PATOH_InitializeParameters
            self.__PATOH_InitializeParameters = clib.Patoh_Initialize_Parameters
            self.__PATOH_InitializeParameters.argtypes = (ctypes.POINTER(PatohInitializeParameters), ctypes.c_int, ctypes.c_int)

            # PATOH_Alloc
            self.__PATOH_Alloc = clib.Patoh_Alloc
            self.__PATOH_Alloc.argtypes = (ctypes.POINTER(PatohInitializeParameters), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)

            # PATOH_Part
            self.__PATOH_Part = clib.Patoh_Part
            self.__PATOH_Part.argtypes = (ctypes.POINTER(PatohInitializeParameters), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)

            # PATOH_Free
            self.__PATOH_Free = clib.Patoh_Free
        except Exception as err:
            raise hp_exception.SomethingWrongWithPatohLibraryException("library", str(err))

    def __check_files_and_directories(self) -> None:
        """
        Check if all necessary files and directories exist
        :return: None
        :raises FileIsMissingException: if some file is missing
        :raises SoftwareIsNotSupportedOnSystemException: if the chosen software is not supported on the system
        """

        # hMETIS
        if self.__software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS:
            HypergraphPartitioning.__TEMP_DIRECTORY_PATH.mkdir(exist_ok=True)

            # Windows
            if env.is_windows():
                # The exe file does not exist
                if not HypergraphPartitioning.__WIN_PROGRAM_HMETIS_PATH.exists():
                    raise hp_exception.FileIsMissingException(str(HypergraphPartitioning.__WIN_PROGRAM_HMETIS_PATH))

                return

            # Linux
            if env.is_linux():
                # The file does not exist
                if not HypergraphPartitioning.__LINUX_PROGRAM_HMETIS_PATH.exists():
                    raise hp_exception.FileIsMissingException(str(HypergraphPartitioning.__LINUX_PROGRAM_HMETIS_PATH))

                return

            # MacOS or undefined
            raise hp_exception.SoftwareIsNotSupportedOnSystemException(self.__software_enum.name)

        # PaToH
        if self.__software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.PATOH:
            # Linux
            if env.is_linux():
                # The library does not exist
                if not HypergraphPartitioning.__LINUX_LIBRARY_PATOH_PATH.exists():
                    raise hp_exception.FileIsMissingException(str(HypergraphPartitioning.__LINUX_LIBRARY_PATOH_PATH))

                return

            # MacOS
            if env.is_mac_os():
                # The library does not exist
                if not HypergraphPartitioning.__MAC_OS_LIBRARY_PATOH_PATH.exists():
                    raise hp_exception.FileIsMissingException(str(HypergraphPartitioning.__MAC_OS_LIBRARY_PATOH_PATH))

                return

            # Windows or undefined
            raise hp_exception.SoftwareIsNotSupportedOnSystemException(self.__software_enum.name)

        # KaHyPar
        if self.__software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.KAHYPAR:
            # Linux or macOS
            if env.is_linux() or env.is_mac_os():
                # The config file does not exist
                if not HypergraphPartitioning.__CONFIG_KAHYPAR_PATH.exists():
                    raise hp_exception.FileIsMissingException(str(HypergraphPartitioning.__CONFIG_KAHYPAR_PATH))

                return

            # Windows or undefined
            raise hp_exception.SoftwareIsNotSupportedOnSystemException(self.__software_enum.name)

        warnings.warn("No software for hypergraph partitioning is being used!")

    def __variable_simplification(self, solver: Solver, assignment_list: List[int],
                                  variable_restriction_set: Union[Set[int], None] = None) -> Dict[int, Set[int]]:
        """
        Compute variable simplification using implicit unit propagation
        :param solver: the solver
        :param assignment_list: a partial assignment (for the solver)
        :param variable_restriction_set: a set of variables that will be taken into account
        :return: a dictionary where a key is a variable (representant),
        and the value is a set of variables that can be merged with the variable to reduce the hypergraph size
        """

        self.__statistics.variable_simplification.start_stopwatch()     # timer (start)

        # None
        if self.__variable_simplification_enum == hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.NONE:
            self.__statistics.variable_simplification.stop_stopwatch()  # timer (stop)
            return dict()

        # EQUIV_SIMPL
        if self.__variable_simplification_enum == hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL:
            implicit_bcp_dictionary = solver.implicit_unit_propagation(assignment_list=assignment_list,
                                                                       variable_restriction_set=variable_restriction_set)

            # The formula is unsatisfiable (it should not happen at all)
            if implicit_bcp_dictionary is None:
                warnings.warn("Unexpected situation (variable simplification - unsatisfiable formula)!")

                self.__statistics.variable_simplification.stop_stopwatch()  # timer (stop)
                return dict()

            dominated_variable_set = set()
            equivalence_dictionary: Dict[int, Set[int]] = dict()

            for var in implicit_bcp_dictionary:
                # The variable is already dominated
                if var in dominated_variable_set:
                    continue

                first_temp, second_temp = implicit_bcp_dictionary[var]

                first_temp = set() if first_temp is None else first_temp
                second_temp = set() if second_temp is None else second_temp

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

        raise c_exception.FunctionNotImplementedException("variable_simplification",
                                                          f"this type of variable simplification ({self.__variable_simplification_enum.name}) is not implemented")

    # region Weights
    def __set_static_weights(self, initial_incidence_graph: IncidenceGraph) -> None:
        """
        Initialize the static weights.
        If the type of weights is not STATIC, nothing happens.
        Variable: node_weight_dictionary, hyperedge_weight_dictionary
        :param initial_incidence_graph: an initial incidence graph
        :return: None
        """

        self.__statistics.set_static_weights.start_stopwatch()  # timer (start)

        # Nodes' weight
        if self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.STATIC:
            for node_id in range(self.__total_number_of_nodes):
                self.__node_weight_dictionary[node_id] = 1

        # Hyperedges' weight
        if self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.STATIC:
            for hyperedge_id in self.__hyperedge_set:
                self.__hyperedge_weight_dictionary[hyperedge_id] = 1

        self.__statistics.set_static_weights.stop_stopwatch()   # timer (stop)

    def __set_dynamic_weights(self, incidence_graph: IncidenceGraph) -> None:
        """
        Initialize the dynamic weights based on the incidence graph.
        If the type of weights is not DYNAMIC, nothing happens.
        Variable: node_weight_dictionary, hyperedge_weight_dictionary
        :param incidence_graph: an incidence graph
        :return: None
        """

        self.__statistics.set_dynamic_weights.start_stopwatch()     # timer (start)

        # Nodes' weight
        if self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.DYNAMIC:
            self.__node_weight_dictionary = dict()  # reset
            pass

        # Hyperedges' weight
        if self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.DYNAMIC:
            self.__hyperedge_weight_dictionary = dict()     # reset
            pass

        self.__statistics.set_dynamic_weights.stop_stopwatch()      # timer (stop)

    def __get_node_weight(self, node_id: int) -> int:
        """
        Return the weight of the node based on the node_weight_enum
        :param node_id: the identifier of the node
        :return: the weight of the node
        :raises NodeDoesNotExistException: if the node does not exist in the hypergraph
        """

        # The node does not exist in the hypergraph
        if (node_id < 0) or (node_id >= self.__total_number_of_nodes):
            raise hp_exception.NodeDoesNotExistException(node_id)

        # NONE
        if self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE:
            return 1

        # STATIC or DYNAMIC
        if (self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.STATIC) or \
           (self.__node_weight_enum == hpwt_enum.HypergraphPartitioningNodeWeightEnum.DYNAMIC):
            # The weight has not been created
            if node_id not in self.__node_weight_dictionary:
                raise hp_exception.NodeDoesNotExistException(node_id)

            return self.__node_weight_dictionary[node_id]

        raise c_exception.FunctionNotImplementedException("get_node_weight",
                                                          f"this type of weight ({self.__node_weight_enum.name}) is not implemented")

    def __get_hyperedge_weight(self, hyperedge_id: int) -> int:
        """
        Return the weight of the hyperedge based on the hyperedge_weight_enum
        :param hyperedge_id: the identifier of the hyperedge
        :return: the weight of the hyperedge
        :raises HyperedgeDoesNotExistException: if the hyperedge does not exist in the hypergraph
        """

        # The hyperedge does not exist in the hypergraph
        if hyperedge_id not in self.__hyperedge_set:
            raise hp_exception.HyperedgeDoesNotExistException(hyperedge_id)

        # NONE
        if self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE:
            return 1

        # STATIC or DYNAMIC
        if (self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.STATIC) or \
           (self.__hyperedge_weight_enum == hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.DYNAMIC):
            # The weight has not been created
            if hyperedge_id not in self.__hyperedge_weight_dictionary:
                raise hp_exception.HyperedgeDoesNotExistException(hyperedge_id)

            return self.__hyperedge_weight_dictionary[hyperedge_id]

        raise c_exception.FunctionNotImplementedException("get_hyperedge_weight",
                                                          f"this type of weight ({self.__hyperedge_weight_enum.name}) is not implemented")
    # endregion

    # region Cache
    def __add_cut_set_cache(self, key: str, cut_set: Set[int]) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        Cache: cut_set_cache
        :param key: the key
        :param cut_set: the value
        :return: None
        """

        self.__cut_set_cache[key] = cut_set

    def __get_cut_set_cache(self, key: Union[str, None]) -> Union[Set[int], None]:
        """
        Return a value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        Cache: cut_set_cache
        :param key: the key
        :return: the record's value if the record exists. Otherwise, None is returned.
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

    def __generate_key_cache(self, incidence_graph: IncidenceGraph) -> Tuple[str, Tuple[Dict[int, int], Dict[int, int]]]:
        """
        Generate a key for caching
        Variable property: occurrence, mean, variance (optional)
        :param incidence_graph: an incidence graph
        :return: the generated key based on the incidence graph and both mappings between variables (variable_id -> order_id, order_id -> variable_id)
        """

        self.__statistics.generate_key_cache.start_stopwatch()      # timer (start)

        # Variance
        use_variance = False
        if self.__cache_enum == hpc_enum.HypergraphPartitioningCacheEnum.ISOMORFISM_VARIANCE:
            use_variance = True

        # Initialize
        used_clause_set = set()
        occurrence_dictionary: Dict[int, int] = dict()
        mean_dictionary: Dict[int, float] = dict()
        variance_dictionary: Dict[int, float] = dict()

        neighbour_cache: Dict[int, Set[int]] = dict()   # key: clause's ID, value: a set of neighbours

        # Compute occurrences and means
        for clause_id in incidence_graph.clause_id_set(copy=False,
                                                       multi_occurrence=self.__multi_occurrence_cache,
                                                       multi_occurrence_literal=False):
            used_clause_set.add(clause_id)

            clause_variable_set = incidence_graph.clause_id_neighbour_set(clause_id)
            clause_variable_len = len(clause_variable_set)

            neighbour_cache[clause_id] = clause_variable_set

            for variable in clause_variable_set:
                # Initialize
                if variable not in occurrence_dictionary:
                    occurrence_dictionary[variable] = 0
                    mean_dictionary[variable] = 0
                    variance_dictionary[variable] = 0

                occurrence_dictionary[variable] += 1
                mean_dictionary[variable] += clause_variable_len

        self.__statistics.cache_multi_occurrent_clauses.add_count(incidence_graph.number_of_clauses() - len(used_clause_set))   # counter

        # Compute variances
        if use_variance:
            # Normalization
            for variable in occurrence_dictionary:
                occurrence = occurrence_dictionary[variable]
                mean_dictionary[variable] /= occurrence

            for clause_id in used_clause_set:
                clause_variable_set = neighbour_cache[clause_id]
                clause_variable_len = len(clause_variable_set)

                for variable in clause_variable_set:
                    mean = mean_dictionary[variable]
                    variance_dictionary[variable] += (clause_variable_len - mean) ** 2

        variable_property_dictionary: Dict[int, Tuple[int, float, float, int]] = dict()
        for variable in occurrence_dictionary:
            occurrence = occurrence_dictionary[variable]
            mean = mean_dictionary[variable]
            variance = variance_dictionary[variable]

            variable_property_dictionary[variable] = occurrence, mean, variance, variable

        variable_sorted_list = sorted(variable_property_dictionary, key=variable_property_dictionary.get)

        # Mapping
        variable_id_order_id_dictionary: Dict[int, int] = dict()  # mapping variable_id -> order_id
        order_id_variable_id_dictionary: Dict[int, int] = dict()  # mapping order_id -> variable_id

        for i, variable in enumerate(variable_sorted_list):
            variable_id_order_id_dictionary[variable] = i
            order_id_variable_id_dictionary[i] = variable

        variable_clause_list = []
        for clause_id in used_clause_set:
            clause_variable_set = neighbour_cache[clause_id]
            variable_sorted_list = sorted(map(lambda v: variable_id_order_id_dictionary[v], clause_variable_set))
            variable_clause_list.append(",".join([str(v) for v in variable_sorted_list]))

        variable_clause_sorted_list = sorted(variable_clause_list)

        key_string = "_".join(variable_clause_sorted_list)

        self.__statistics.generate_key_cache.stop_stopwatch()       # timer (stop)
        return key_string, (variable_id_order_id_dictionary, order_id_variable_id_dictionary)
    # endregion

    # region PaToH, KaHyPar
    def __create_hypergraph(self, incidence_graph: IncidenceGraph) -> Tuple[int, int, List[int], List[int], List[int], List[int], Dict[int, int]]:
        """
        Create the hypergraph based on the incidence graph
        Software: PaToH, KaHyPar
        :param incidence_graph: an incidence graph
        :return: (number of nodes, number of hyperedges, xpins, pins, node weights, hyperedge weights, mapping from node_id (hypergraph) to clause_id (CNF))
        """

        # Mapping
        clause_id_node_id_dictionary: Dict[int, int] = dict()   # mapping clause_id -> node_id
        node_id_clause_id_dictionary: Dict[int, int] = dict()   # mapping node_id -> clause_id

        number_of_nodes: int = 0
        number_of_hyperedges: int = incidence_graph.number_of_variables()
        xpins_list: List[int] = [0]
        pins_list: List[int] = []
        node_weight_list: List[int] = []
        hyperedge_weight_list: List[int] = []

        # Hyperedges
        for variable in incidence_graph._variable_set:
            clause_id_set = incidence_graph.variable_neighbour_set(variable)

            pin_temp = []
            hyperedge_weight_list.append(self.__get_hyperedge_weight(variable))
            for clause_id in clause_id_set:
                # Add to the mapping
                if clause_id not in clause_id_node_id_dictionary:
                    clause_id_node_id_dictionary[clause_id] = number_of_nodes
                    node_id_clause_id_dictionary[number_of_nodes] = clause_id
                    number_of_nodes += 1

                pin_temp.append(clause_id_node_id_dictionary[clause_id])

            xpins_list.append(xpins_list[-1] + len(pin_temp))
            pins_list.extend(pin_temp)

        # Node weights
        for node_id in range(number_of_nodes):
            node_weight_list.append(self.__get_node_weight(node_id_clause_id_dictionary[node_id]))

        return number_of_nodes, number_of_hyperedges, xpins_list, pins_list, node_weight_list, hyperedge_weight_list, node_id_clause_id_dictionary

    def __get_cut_set_from_partition(self, incidence_graph: IncidenceGraph, partition_list: List[int], node_id_clause_id_dictionary: Dict[int, int]) -> Set[int]:
        """
        Create a cut set from the partition
        Software: PaToh, KaHyPar
        :param incidence_graph: an incidence graph
        :param partition_list: a partition list {0|1}*
        :param node_id_clause_id_dictionary: mapping from node_id (hypergraph) to clause_id (CNF)
        :return: a cut set
        :raises SomethingWrongException: if the partition is invalid
        """

        variable_partition_0_set = set()
        variable_partition_1_set = set()

        for i, partition in enumerate(partition_list):
            if (partition != 0) and (partition != 1):
                raise hp_exception.SomethingWrongException(f"invalid partition ({partition})")

            variable_set_temp = incidence_graph.clause_id_neighbour_set(node_id_clause_id_dictionary[i])

            if partition == 0:
                variable_partition_0_set.update(variable_set_temp)
            else:
                variable_partition_1_set.update(variable_set_temp)

        cut_set = variable_partition_0_set.intersection(variable_partition_1_set)
        return cut_set

    def __get_cut_set_patoh(self, incidence_graph: IncidenceGraph) -> Set[int]:
        """
        Compute a cut set using PaToH
        :param incidence_graph: an incidence graph
        :return: a cut set of the hypergraph
        :raises SomethingWrongWithPatohLibraryException: if something is wrong with the PaToH library
        """

        number_of_nodes, number_of_hyperedges, xpins_list, pins_list, node_weight_list, hyperedge_weight_list, node_id_clause_id_dictionary = self.__create_hypergraph(incidence_graph)
        patoh_data: PatohData = PatohData(number_of_nodes=number_of_nodes, number_of_hyperedges=number_of_hyperedges,
                                          node_weight_list=node_weight_list, hyperedge_weight_list=hyperedge_weight_list,
                                          xpins=xpins_list, pins=pins_list, epsilon=self.__imbalance_factor)

        # PaToH library
        try:
            # PATOH_InitializeParameters
            result_code = self.__PATOH_InitializeParameters(patoh_data.parameters_ref(), 1, self.__patoh_sugparam_enum.value)
            if result_code:
                raise hp_exception.SomethingWrongWithPatohLibraryException("PATOH_InitializeParameters", str(result_code))

            # PATOH_Alloc
            result_code = self.__PATOH_Alloc(patoh_data.parameters_ref(), patoh_data.c, patoh_data.n, patoh_data.nconst,
                                             patoh_data.cwghts_ctypes(), patoh_data.nwghts_ctypes(), patoh_data.xpins_ctypes(), patoh_data.pins_ctypes())
            if result_code:
                raise hp_exception.SomethingWrongWithPatohLibraryException("PATOH_Alloc", str(result_code))

            # PATOH_Part
            result_code = self.__PATOH_Part(patoh_data.parameters_ref(), patoh_data.c, patoh_data.n, patoh_data.nconst, patoh_data.useFixCells,
                                            patoh_data.cwghts_ctypes(), patoh_data.nwghts_ctypes(), patoh_data.xpins_ctypes(), patoh_data.pins_ctypes(),
                                            patoh_data.targetweights_ctypes(), patoh_data.partvec_ctypes(), patoh_data.partweights_ctypes(), patoh_data.cut_addr())
            if result_code:
                raise hp_exception.SomethingWrongWithPatohLibraryException("PATOH_Part", str(result_code))
        except Exception as err:
            raise hp_exception.SomethingWrongWithPatohLibraryException("library", str(err))

        # Get the cut set
        cut_set = self.__get_cut_set_from_partition(incidence_graph, patoh_data.partvec(), node_id_clause_id_dictionary)

        # PATOH_Free
        result_code = self.__PATOH_Free()
        if result_code:
            raise hp_exception.SomethingWrongWithPatohLibraryException("PATOH_Free", str(result_code))

        del patoh_data
        return cut_set

    def __get_cut_set_kahypar(self, incidence_graph: IncidenceGraph) -> Set[int]:
        """
        Compute a cut set using KaHyPar
        :param incidence_graph: an incidence graph
        :return: a cut set of the hypergraph
        """

        import kahypar as kahypar

        kahypar_context = kahypar.Context()
        kahypar_context.loadINIconfiguration(str(HypergraphPartitioning.__CONFIG_KAHYPAR_PATH))

        kahypar_context.setK(2)
        kahypar_context.setEpsilon(self.__imbalance_factor)
        kahypar_context.suppressOutput(True)

        number_of_nodes, number_of_hyperedges, xpins_list, pins_list, node_weight_list, hyperedge_weight_list, node_id_clause_id_dictionary = self.__create_hypergraph(incidence_graph)
        hypergraph = kahypar.Hypergraph(number_of_nodes, number_of_hyperedges, xpins_list, pins_list, 2, hyperedge_weight_list, node_weight_list)

        kahypar.partition(hypergraph, kahypar_context)
        partition_list = [hypergraph.blockID(i) for i in hypergraph.nodes()]

        # Get the cut set
        cut_set = self.__get_cut_set_from_partition(incidence_graph, partition_list, node_id_clause_id_dictionary)

        return cut_set
    # endregion

    # region hMETIS
    def __create_hypergraph_hmetis(self, incidence_graph: IncidenceGraph) -> Tuple[str, Dict[int, int]]:
        """
        Create an input file string with the hypergraph for hMETIS based on the incidence graph
        Software: hMETIS
        :param incidence_graph: an incidence graph
        :return: (file string, mapping from node_id (file) to clause_id (CNF))
        """

        # Mapping
        clause_id_node_id_dictionary: Dict[int, int] = dict()   # mapping clause_id -> node_id
        node_id_clause_id_dictionary: Dict[int, int] = dict()   # mapping node_id -> clause_id

        number_of_nodes = 0
        number_of_hyperedges = incidence_graph.number_of_variables()

        # Hyperedges
        line_hyperedge = []
        for variable in incidence_graph._variable_set:
            clause_id_set = incidence_graph.variable_neighbour_set(variable)

            line_temp = [self.__get_hyperedge_weight(variable)]
            for clause_id in clause_id_set:
                # Add to the mapping
                if clause_id not in clause_id_node_id_dictionary:
                    number_of_nodes += 1
                    clause_id_node_id_dictionary[clause_id] = number_of_nodes
                    node_id_clause_id_dictionary[number_of_nodes] = clause_id

                line_temp.append(clause_id_node_id_dictionary[clause_id])

            line_hyperedge.append(" ".join([str(temp) for temp in line_temp]))

        string_hyperedge = "\n".join(line_hyperedge)

        # Node weights
        line_weight = []
        for node_id in range(1, number_of_nodes + 1):
            line_weight.append(str(self.__get_node_weight(node_id_clause_id_dictionary[node_id])))

        string_weight = "\n".join(line_weight)

        string_result = "\n".join((f"{number_of_hyperedges} {number_of_nodes} 11",
                                   string_hyperedge,
                                   string_weight))

        return string_result, node_id_clause_id_dictionary

    def __get_cut_set_hmetis(self, incidence_graph: IncidenceGraph) -> Set[int]:
        """
        Compute a cut set using hMETIS
        :param incidence_graph: an incidence graph
        :return: a cut set of the hypergraph
        """

        file_string, node_id_clause_id_dictionary = self.__create_hypergraph_hmetis(incidence_graph)

        # Delete temp files
        self.__input_file_hmetis_path.unlink(missing_ok=True)
        self.__output_file_1_hmetis_path.unlink(missing_ok=True)
        self.__output_file_2_hmetis_path.unlink(missing_ok=True)

        # Save the input file
        with open(self.__input_file_hmetis_path, "w", encoding="utf-8") as input_file:
            input_file.write(file_string)

        program_hmetis_path_temp = HypergraphPartitioning.__WIN_PROGRAM_HMETIS_PATH if env.is_windows() else HypergraphPartitioning.__LINUX_PROGRAM_HMETIS_PATH

        devnull = open(os.devnull, 'w')
        subprocess.run([program_hmetis_path_temp,
                        self.__input_file_hmetis_path,
                        str(2), str(100 * self.__imbalance_factor)],
                       stdout=devnull)

        # A cut set does not exist (because of balance etc.)
        if self.__output_file_1_hmetis_path.exists():
            self.__input_file_hmetis_path.unlink(missing_ok=True)
            self.__output_file_1_hmetis_path.unlink(missing_ok=True)

            return set()

        # The output file has not been generated => an error occurred
        if not self.__output_file_2_hmetis_path.exists():
            raise hp_exception.SomethingWrongException("the output file from hMETIS.exe has not been generated => an error occurred")

        # Get the cut set
        variable_partition_0_set = set()
        variable_partition_1_set = set()

        with open(self.__output_file_2_hmetis_path, "r", encoding="utf-8") as output_file:
            line_id = 0

            while True:
                line = output_file.readline()
                line_id += 1

                # End of the file
                if not line:
                    break

                try:
                    partition_temp = int(line)
                except ValueError:
                    raise hp_exception.SomethingWrongException(f"partition ({line}) in the output file generated from hMETIS.exe is not a number")

                if (partition_temp != 0) and (partition_temp != 1):
                    raise hp_exception.SomethingWrongException(f"invalid partition ({partition_temp}) in the output file generated from hMETIS.exe")

                variable_set_temp = incidence_graph.clause_id_neighbour_set(node_id_clause_id_dictionary[line_id])

                if partition_temp == 0:
                    variable_partition_0_set.update(variable_set_temp)
                else:
                    variable_partition_1_set.update(variable_set_temp)

        cut_set = variable_partition_0_set.intersection(variable_partition_1_set)

        # Delete temp files
        self.__input_file_hmetis_path.unlink(missing_ok=True)
        self.__output_file_2_hmetis_path.unlink(missing_ok=True)

        return cut_set
    # endregion
    # endregion

    # region Public method
    def get_cut_set(self, incidence_graph: IncidenceGraph, solver: Solver, assignment: List[int],
                    incidence_graph_is_reduced: bool = False, use_restriction: bool = False) -> Set[int]:
        """
        Create a hypergraph based on the incidence graph
        :param incidence_graph: an incidence graph
        :param solver: the solver (in case equivSimpl is used)
        :param assignment: a partial assignment (for the solver)
        :param use_restriction: use restriction in the implicit unit propagation
        :param incidence_graph_is_reduced: True if the incidence graph has been already reduced
        :return: a cut set of the hypergraph
        """

        self.__statistics.get_cut_set.start_stopwatch()     # timer (start)

        # The decomposition is disabled
        if self.__disable_decomposition:
            cut_set = incidence_graph.variable_set(copy=True)
            HypergraphPartitioning.remove_reduction_incidence_graph(incidence_graph)

            self.__statistics.get_cut_set.stop_stopwatch()  # timer (stop)
            return cut_set

        self.__set_dynamic_weights(incidence_graph)

        if not incidence_graph_is_reduced:
            self.reduce_incidence_graph(incidence_graph=incidence_graph,
                                        solver=solver,
                                        assignment=assignment,
                                        use_restriction=use_restriction)

        # Only one clause remains => all variables are in the cut set
        if incidence_graph.number_of_clauses() == 1:
            cut_set = incidence_graph.variable_set(copy=True)
            HypergraphPartitioning.remove_reduction_incidence_graph(incidence_graph)

            self.__statistics.get_cut_set.stop_stopwatch()      # timer (stop)
            return cut_set

        # Cache
        key = None                              # initialization
        variable_id_order_id_dictionary = None  # initialization

        result_cache_cut_set, result_cache_key = self.check_cache(incidence_graph)
        # A cut set has been found
        if result_cache_cut_set is not None:
            HypergraphPartitioning.remove_reduction_incidence_graph(incidence_graph)

            self.__statistics.cache_hit.add_count(1)  # counter
            self.__statistics.get_cut_set.stop_stopwatch()  # timer (stop)
            return result_cache_cut_set
        else:
            if result_cache_key is not None:
                key, (variable_id_order_id_dictionary, _) = result_cache_key
                self.__statistics.cache_hit.add_count(0)  # counter

        cut_set = set()

        # hMETIS
        if self.__software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS:
            cut_set = self.__get_cut_set_hmetis(incidence_graph)

        # PaToH
        if self.__software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.PATOH:
            cut_set = self.__get_cut_set_patoh(incidence_graph)

        # KaHyPar
        if self.__software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.KAHYPAR:
            cut_set = self.__get_cut_set_kahypar(incidence_graph)

        # A cut set does not exist (because of balance etc.) => a variable with the most occurrences is selected
        if not cut_set:
            self.__statistics.empty_cut_set.add_count(1)    # counter
            cut_set = {incidence_graph.variable_with_most_occurrences()}

        # Cache
        if key is not None:
            cut_set_cache = set()
            for var in cut_set:
                cut_set_cache.add(variable_id_order_id_dictionary[var])

            self.__add_cut_set_cache(key, cut_set_cache)

        cut_set_size = len(cut_set)
        number_of_nodes = incidence_graph.number_of_clauses()
        number_of_hyperedges = incidence_graph.number_of_variables()
        temp = 1 if number_of_hyperedges == 1 else math.log(cut_set_size)/math.log(number_of_hyperedges)
        self.__statistics.hypergraph_number_of_nodes.add_count(number_of_nodes)                 # counter
        self.__statistics.hypergraph_number_of_hyperedges.add_count(number_of_hyperedges)       # counter
        self.__statistics.ratio_log_cut_set_size_and_log_number_of_hyperedges.add_count(temp)   # counter

        HypergraphPartitioning.remove_reduction_incidence_graph(incidence_graph)

        self.__statistics.cut_set_size.add_count(cut_set_size)  # counter
        self.__statistics.get_cut_set.stop_stopwatch()  # timer (stop)
        return cut_set

    def check_cache(self, incidence_graph: IncidenceGraph) -> Tuple[Union[Set[int], None], Union[Tuple[str, Tuple[Dict[int, int], Dict[int, int]]], None]]:
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

    def reduce_incidence_graph(self, incidence_graph: IncidenceGraph, solver: Solver, assignment: List[int], use_restriction: bool) -> None:
        """
        Do a variable simplification and subsumption (if the limit is satisfied)
        :param incidence_graph: an incidence graph
        :param solver: the solver
        :param assignment: a partial assignment (for the solver)
        :param use_restriction: use restriction in the implicit unit propagation
        :return: None
        """

        # Variable simplification
        variable_simplification_dictionary = self.__variable_simplification(solver=solver,
                                                                            assignment_list=assignment,
                                                                            variable_restriction_set=None if not use_restriction else incidence_graph._variable_set)
        incidence_graph.merge_variable_simplification(variable_simplification_dictionary)

        # Subsumption
        if (self.__subsumption_threshold is None) or (incidence_graph.number_of_clauses() <= self.__subsumption_threshold):
            subsumed_clause_set = incidence_graph.subsumption_variable()
            incidence_graph.remove_subsumed_clause_variable_set(subsumed_clause_set)

    def cache_can_be_used(self, incidence_graph: IncidenceGraph) -> bool:
        """
        :return: True if the cache can be used. Otherwise, False is returned.
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
        incidence_graph.restore_backup_subsumption_variable()       # subsumption
        incidence_graph.restore_backup_variable_simplification()    # variable simplification
    # endregion
