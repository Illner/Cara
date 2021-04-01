# Import
from formula.cnf import Cnf
from circuit.circuit import Circuit
from typing import Set, Tuple, Union
from compiler.component import Component
from formula.incidence_graph import IncidenceGraph
from compiler_statistics.statistics import Statistics
from compiler.hypergraph_partitioning import HypergraphPartitioning

# Import component caching
from compiler.component_caching.none_caching import NoneCaching
from compiler.component_caching.basic_caching_scheme import BasicCachingScheme
from compiler.component_caching.hybrid_caching_scheme import HybridCachingScheme
from compiler.component_caching.standard_caching_scheme import StandardCachingScheme

# Import exception
import exception.cara_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.component_caching.component_caching_enum as cc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


class Compiler:
    """
    Compiler
    """

    """
    Private Cnf cnf
    Private bool smooth
    Private Circuit circuit
    Private bool preprocessing
    Private Statistics statistics
    Private bool cut_set_try_cache
    Private float new_cut_set_threshold
    Private float new_cut_set_threshold_reduction   # when cut set cache can be used
    Private ComponentCachingAbstract component_caching
    Private HypergraphPartitioning hypergraph_partitioning
    
    Private SatSolverEnum sat_solver_enum
    Private ImpliedLiteralsEnum implied_literals_enum
    Private FirstImpliedLiteralsEnum first_implied_literals_enum
    Private HypergraphPartitioningCacheEnum hp_cache_enum
    Private HypergraphPartitioningSoftwareEnum hp_software_enum
    Private HypergraphPartitioningNodeWeightEnum hp_node_weight_type_enum
    Private HypergraphPartitioningHyperedgeWeightEnum hp_hyperedge_weight_type_enum
    Private HypergraphPartitioningVariableSimplificationEnum hp_variable_simplification_enum
    """

    def __init__(self, cnf: Union[Cnf, str],
                 smooth: bool,
                 ub_factor: float,
                 preprocessing: bool,
                 subsumed_threshold: Union[int, None],
                 new_cut_set_threshold: float,
                 sat_solver_enum: ss_enum.SatSolverEnum,
                 implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                 first_implied_literals_enum: il_enum.FirstImpliedLiteralsEnum,
                 component_caching_enum: cc_enum.ComponentCachingEnum,
                 hp_cache_enum: hpc_enum.HypergraphPartitioningCacheEnum,
                 hp_software_enum: hps_enum.HypergraphPartitioningSoftwareEnum,
                 hp_node_weight_type_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum,
                 hp_hyperedge_weight_type_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum,
                 hp_variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum,
                 hp_limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                 hp_limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                 cut_set_try_cache: bool = False,
                 new_cut_set_threshold_reduction: float = 1):

        # CNF
        if isinstance(cnf, Cnf):
            self.__cnf: Cnf = cnf
            self.__statistics: Statistics = Statistics(cnf_statistics=self.__cnf.cnf_statistics,
                                                       incidence_graph_statistics=self.__cnf.incidence_graph_statistics)   # statistics
        else:
            self.__statistics: Statistics = Statistics()    # statistics
            self.__cnf: Cnf = Cnf(dimacs_cnf_file_path=cnf,
                                  cnf_statistics=self.__statistics.cnf_statistics,
                                  incidence_graph_statistics=self.__statistics.incidence_graph_statistics)

        self.__smooth: bool = smooth
        self.__circuit: Circuit = Circuit()
        self.__preprocessing: bool = preprocessing
        self.__cut_set_try_cache: bool = cut_set_try_cache
        self.__new_cut_set_threshold: float = new_cut_set_threshold
        self.__new_cut_set_threshold_reduction: float = new_cut_set_threshold_reduction

        self.__sat_solver_enum: ss_enum.SatSolverEnum = sat_solver_enum
        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum
        self.__first_implied_literals_enum: il_enum.FirstImpliedLiteralsEnum = first_implied_literals_enum

        # Component caching
        self.__set_component_caching(component_caching_enum)

        self.__hypergraph_partitioning = HypergraphPartitioning(cnf=self.__cnf,
                                                                ub_factor=ub_factor,
                                                                subsumed_threshold=subsumed_threshold,
                                                                cache_enum=hp_cache_enum,
                                                                software_enum=hp_software_enum,
                                                                node_weight_enum=hp_node_weight_type_enum,
                                                                hyperedge_weight_enum=hp_hyperedge_weight_type_enum,
                                                                variable_simplification_enum=hp_variable_simplification_enum,
                                                                limit_number_of_clauses_cache=hp_limit_number_of_clauses_cache,
                                                                limit_number_of_variables_cache=hp_limit_number_of_variables_cache,
                                                                statistics=self.__statistics.hypergraph_partitioning_statistics)

    # region Private method
    def __set_component_caching(self, component_caching_enum: cc_enum.ComponentCachingEnum):
        # None
        if component_caching_enum == cc_enum.ComponentCachingEnum.NONE:
            self.__component_caching = NoneCaching()
            return

        # STANDARD_CACHING_SCHEME
        if component_caching_enum == cc_enum.ComponentCachingEnum.STANDARD_CACHING_SCHEME:
            self.__component_caching = StandardCachingScheme()
            return

        # HYBRID_CACHING_SCHEME
        if component_caching_enum == cc_enum.ComponentCachingEnum.HYBRID_CACHING_SCHEME:
            self.__component_caching = HybridCachingScheme()
            return

        # BASIC_CACHING_SCHEME
        if component_caching_enum == cc_enum.ComponentCachingEnum.BASIC_CACHING_SCHEME:
            self.__component_caching = BasicCachingScheme()
            return

        raise c_exception.FunctionNotImplementedException("set_component_caching",
                                                          f"this type of component caching ({component_caching_enum.name}) is not implemented")
    # endregion

    # region Public method
    def create_circuit(self) -> Circuit:
        """
        :return: the created circuit
        """

        self.__statistics.compiler_statistics.create_circuit.start_stopwatch()  # timer (start)

        incidence_graph: IncidenceGraph = self.__cnf.get_incidence_graph()
        incidence_graph_set: Set[IncidenceGraph] = {incidence_graph}

        # More components exist
        if incidence_graph.number_of_components() > 1:
            incidence_graph_set = incidence_graph.create_incidence_graphs_for_components()

        node_id_set: Set[int] = set()
        for incidence_graph in incidence_graph_set:
            # TODO Renamable Horn formula recognition
            incidence_graph.initialize_renamable_horn_formula_recognition()

            component = Component(cnf=self.__cnf,
                                  assignment_list=[],
                                  circuit=self.__circuit,
                                  new_cut_set_threshold=self.__new_cut_set_threshold,
                                  new_cut_set_threshold_reduction=self.__new_cut_set_threshold_reduction,
                                  cut_set_try_cache=self.__cut_set_try_cache,
                                  incidence_graph=incidence_graph,
                                  component_caching=self.__component_caching,
                                  hypergraph_partitioning=self.__hypergraph_partitioning,
                                  sat_solver_enum=self.__sat_solver_enum,
                                  implied_literals_enum=self.__implied_literals_enum,
                                  first_implied_literals_enum=self.__first_implied_literals_enum,
                                  statistics=self.__statistics,
                                  preprocessing=self.__preprocessing)
            node_id = component.create_circuit()
            node_id_set.add(node_id)

        # More components have to be connected
        if len(node_id_set) > 1:
            root_id = self.__circuit.create_and_node(node_id_set)
            self.__circuit.set_root(root_id)
        # Only one component exists
        else:
            root_id = (list(node_id_set))[0]
            self.__circuit.set_root(root_id)

        # Add unused variables
        node_id_set = set()
        variable_in_circuit_set = self.__circuit.get_node(self.__circuit.root_id)._get_variable_in_circuit_set()
        unused_variable_set = self.__cnf._get_variable_set().difference(variable_in_circuit_set)

        for var in unused_variable_set:
            child_id_set = self.__circuit.create_literal_leaf_set({var, -var})
            node_id = self.__circuit.create_or_node(child_id_set, decision_variable=var)
            node_id_set.add(node_id)

        if node_id_set:
            node_id = self.__circuit.create_and_node({root_id}.union(node_id_set))
            self.__circuit.set_root(node_id)

        self.__statistics.compiler_statistics.smooth.start_stopwatch()  # timer (start)

        # Smooth
        if self.__smooth:
            self.__circuit.smooth()

        self.__statistics.compiler_statistics.smooth.stop_stopwatch()   # timer (stop)

        self.__statistics.compiler_statistics.create_circuit.stop_stopwatch()   # timer (stop)
        return self.circuit
    # endregion

    # region Property
    @property
    def circuit(self):
        return self.__circuit

    @property
    def statistics(self):
        return self.__statistics
    # endregion
