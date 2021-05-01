# Import
from formula.cnf import Cnf
from circuit.circuit import Circuit
from typing import Set, Tuple, Union
from compiler.component import Component
from formula.incidence_graph import IncidenceGraph
from compiler_statistics.statistics import Statistics
from compiler.hypergraph_partitioning.hypergraph_partitioning import HypergraphPartitioning

# Import component caching
from compiler.component_caching.none_caching import NoneCaching
from compiler.component_caching.basic_caching_scheme import BasicCachingScheme
from compiler.component_caching.hybrid_caching_scheme import HybridCachingScheme
from compiler.component_caching.standard_caching_scheme import StandardCachingScheme

# Import decision heuristic
from compiler.decision_heuristic.random_heuristic import RandomHeuristic
from compiler.decision_heuristic.jeroslow_wang_heuristic import JeroslowWangHeuristic
from compiler.decision_heuristic.literal_count_heuristic import LiteralCountHeuristic
from compiler.decision_heuristic.eupc_heuristic import ExactUnitPropagationCountHeuristic
from compiler.decision_heuristic.clause_reduction_heuristic import ClauseReductionHeuristic
from compiler.decision_heuristic.weighted_binaries_heuristic import WeightedBinariesHeuristic

# Import preselection heuristic
from compiler.preselection_heuristic.none_heuristic import NoneHeuristic
from compiler.preselection_heuristic.prop_z_heuristic import PropZHeuristic
from compiler.preselection_heuristic.clause_reduction_approximation_heuristic import ClauseReductionApproximationHeuristic

# Import exception
import exception.cara_exception as c_exception

# Import enum
import compiler.enum.base_class_enum as bs_enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.enum.heuristic.decision_heuristic_enum as dh_enum
import formula.enum.eliminating_redundant_clauses_enum as erc_enum
import compiler.component_caching.component_caching_enum as cc_enum
import compiler.enum.heuristic.preselection_heuristic_enum as ph_enum
import compiler.enum.heuristic.mixed_difference_heuristic_enum as mdh_enum
import compiler.enum.heuristic.literal_count_heuristic_function_enum as lchf_enum
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
    Private float new_cut_set_threshold_reduction           # when the cache for cut sets can be used
    Private Set<BaseClassEnum> base_class_enum_set
    Private ComponentCachingAbstract component_caching
    Private int eliminating_redundant_clauses_threshold
    Private DecisionHeuristicAbstract decision_heuristic
    Private HypergraphPartitioning hypergraph_partitioning
    Private EliminatingRedundantClausesEnum eliminating_redundant_clauses_enum
    Private PreselectionHeuristicAbstract implied_literals_preselection_heuristic
    
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
                 subsumption_threshold: Union[int, None],
                 new_cut_set_threshold: float,
                 decision_heuristic_enum: dh_enum.DecisionHeuristicEnum,
                 sat_solver_enum: ss_enum.SatSolverEnum,
                 base_class_enum_set: Set[bs_enum.BaseClassEnum],
                 implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                 implied_literals_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum,
                 first_implied_literals_enum: il_enum.FirstImpliedLiteralsEnum,
                 component_caching_enum: cc_enum.ComponentCachingEnum,
                 eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum,
                 eliminating_redundant_clauses_threshold: Union[int, None],
                 hp_cache_enum: hpc_enum.HypergraphPartitioningCacheEnum,
                 hp_software_enum: hps_enum.HypergraphPartitioningSoftwareEnum,
                 hp_node_weight_type_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum,
                 hp_hyperedge_weight_type_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum,
                 hp_variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum,
                 hp_limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                 hp_limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                 cut_set_try_cache: bool = False,
                 new_cut_set_threshold_reduction: float = 1,
                 decision_heuristic_mixed_difference_enum: mdh_enum.MixedDifferenceHeuristicEnum = mdh_enum.MixedDifferenceHeuristicEnum.OK_SOLVER,
                 implied_literals_preselection_heuristic_prop_z_depth_threshold: int = 5,
                 implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound: Union[int, None] = 10,
                 implied_literals_preselection_heuristic_cra_rank: float = 0.1):

        # CNF
        if isinstance(cnf, Cnf):
            self.__cnf: Cnf = cnf
            self.__statistics: Statistics = Statistics(cnf_statistics=self.__cnf.cnf_statistics,
                                                       incidence_graph_statistics=self.__cnf.incidence_graph_statistics)
        else:
            self.__statistics: Statistics = Statistics()
            self.__cnf: Cnf = Cnf(dimacs_cnf_source=cnf,
                                  cnf_statistics=self.__statistics.cnf_statistics,
                                  incidence_graph_statistics=self.__statistics.incidence_graph_statistics)

        self.__smooth: bool = smooth
        self.__circuit: Circuit = Circuit()
        self.__preprocessing: bool = preprocessing
        self.__cut_set_try_cache: bool = cut_set_try_cache
        self.__new_cut_set_threshold: float = new_cut_set_threshold
        self.__new_cut_set_threshold_reduction: float = new_cut_set_threshold_reduction
        self.__base_class_enum_set: Set[bs_enum.BaseClassEnum] = base_class_enum_set
        self.__eliminating_redundant_clauses_threshold: Union[int, None] = eliminating_redundant_clauses_threshold

        self.__sat_solver_enum: ss_enum.SatSolverEnum = sat_solver_enum
        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum
        self.__first_implied_literals_enum: il_enum.FirstImpliedLiteralsEnum = first_implied_literals_enum
        self.__eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum = eliminating_redundant_clauses_enum

        # Component caching
        self.__set_component_caching(component_caching_enum)

        # Decision heuristic
        self.__set_decision_heuristic(decision_heuristic_enum, decision_heuristic_mixed_difference_enum)

        # Implied literals - preselection heuristic
        self.__set_implied_literals_preselection_heuristic(implied_literals_preselection_heuristic_enum=implied_literals_preselection_heuristic_enum,
                                                           prop_z_depth_threshold=implied_literals_preselection_heuristic_prop_z_depth_threshold,
                                                           prop_z_number_of_variables_lower_bound=implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound,
                                                           cra_rank=implied_literals_preselection_heuristic_cra_rank)

        self.__hypergraph_partitioning = HypergraphPartitioning(cnf=self.__cnf,
                                                                ub_factor=ub_factor,
                                                                subsumption_threshold=subsumption_threshold,
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

    def __set_decision_heuristic(self, decision_heuristic_enum: dh_enum.DecisionHeuristicEnum,
                                 mixed_difference_heuristic_enum: mdh_enum.MixedDifferenceHeuristicEnum):
        preselection_heuristic = NoneHeuristic()

        # RANDOM
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.RANDOM:
            self.__decision_heuristic = RandomHeuristic(preselection_heuristic=preselection_heuristic)
            return

        # JEROSLOW_WANG_ONE_SIDED, JEROSLOW_WANG_TWO_SIDED
        if (decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.JEROSLOW_WANG_ONE_SIDED) or \
           (decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.JEROSLOW_WANG_TWO_SIDED):
            one_sided = True if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.JEROSLOW_WANG_ONE_SIDED else False
            self.__decision_heuristic = JeroslowWangHeuristic(preselection_heuristic=preselection_heuristic,
                                                              one_sided=one_sided)
            return

        # CLAUSE_REDUCTION
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.CLAUSE_REDUCTION:
            self.__decision_heuristic = ClauseReductionHeuristic(preselection_heuristic=preselection_heuristic,
                                                                 weight_for_satisfied_clauses=True,
                                                                 mixed_difference_heuristic_enum=mixed_difference_heuristic_enum)
            return

        # WEIGHTED_BINARIES
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.WEIGHTED_BINARIES:
            self.__decision_heuristic = WeightedBinariesHeuristic(preselection_heuristic=preselection_heuristic)
            return

        # DLCS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.DLCS:
            self.__decision_heuristic = LiteralCountHeuristic(preselection_heuristic=preselection_heuristic,
                                                              function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.SUM,
                                                              tie_breaker_function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.SUM)
            return

        # DLIS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.DLIS:
            self.__decision_heuristic = LiteralCountHeuristic(preselection_heuristic=preselection_heuristic,
                                                              function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.MAX,
                                                              tie_breaker_function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.MAX)
            return

        # DLCS_DLIS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.DLCS_DLIS:
            self.__decision_heuristic = LiteralCountHeuristic(preselection_heuristic=preselection_heuristic,
                                                              function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.SUM,
                                                              tie_breaker_function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.MAX)
            return

        # EUPC
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.EUPC:
            self.__decision_heuristic = ExactUnitPropagationCountHeuristic(preselection_heuristic=preselection_heuristic,
                                                                           mixed_difference_heuristic_enum=mixed_difference_heuristic_enum)
            return

        raise c_exception.FunctionNotImplementedException("set_decision_heuristic",
                                                          f"this type of decision heuristic ({decision_heuristic_enum.name}) is not implemented")

    def __set_implied_literals_preselection_heuristic(self, implied_literals_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum,
                                                      prop_z_depth_threshold: int, prop_z_number_of_variables_lower_bound: Union[int, None],
                                                      cra_rank: float):
        # None
        if implied_literals_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.NONE:
            self.__implied_literals_preselection_heuristic = NoneHeuristic()
            return

        # PROP_Z
        if implied_literals_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.PROP_Z:
            self.__implied_literals_preselection_heuristic = PropZHeuristic(depth_threshold=prop_z_depth_threshold,
                                                                            number_of_variables_lower_bound=prop_z_number_of_variables_lower_bound)
            return

        # CRA
        if implied_literals_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.CRA:
            self.__implied_literals_preselection_heuristic = ClauseReductionApproximationHeuristic(rank=cra_rank,
                                                                                                   total_number_of_variables=self.__cnf.real_number_of_variables)
            return

        raise c_exception.FunctionNotImplementedException("set_implied_literals_preselection_heuristic",
                                                          f"this type of preselection heuristic ({implied_literals_preselection_heuristic_enum.name}) is not implemented")
    # endregion

    # region Public method
    def create_circuit(self) -> Circuit:
        """
        :return: the created circuit
        """

        self.__statistics.compiler_statistics.create_circuit.start_stopwatch()  # timer (start - create_circuit)

        incidence_graph: IncidenceGraph = self.__cnf.get_incidence_graph()
        incidence_graph_set: Set[IncidenceGraph] = {incidence_graph}

        # More components exist
        if incidence_graph.number_of_components() > 1:
            incidence_graph_set = incidence_graph.create_incidence_graphs_for_components()

        node_id_set: Set[int] = set()
        for incidence_graph in incidence_graph_set:
            # Renamable Horn CNF
            if bs_enum.BaseClassEnum.RENAMABLE_HORN_CNF in self.__base_class_enum_set:
                incidence_graph.initialize_renamable_horn_formula_recognition()

            component = Component(cnf=self.__cnf,
                                  assignment_list=[],
                                  circuit=self.__circuit,
                                  new_cut_set_threshold=self.__new_cut_set_threshold,
                                  new_cut_set_threshold_reduction=self.__new_cut_set_threshold_reduction,
                                  cut_set_try_cache=self.__cut_set_try_cache,
                                  incidence_graph=incidence_graph,
                                  decision_heuristic=self.__decision_heuristic,
                                  component_caching=self.__component_caching,
                                  eliminating_redundant_clauses_enum=self.__eliminating_redundant_clauses_enum,
                                  eliminating_redundant_clauses_threshold=self.__eliminating_redundant_clauses_threshold,
                                  hypergraph_partitioning=self.__hypergraph_partitioning,
                                  sat_solver_enum=self.__sat_solver_enum,
                                  base_class_enum_set=self.__base_class_enum_set,
                                  implied_literals_enum=self.__implied_literals_enum,
                                  implied_literals_preselection_heuristic=self.__implied_literals_preselection_heuristic,
                                  first_implied_literals_enum=self.__first_implied_literals_enum,
                                  statistics=self.__statistics,
                                  preprocessing=self.__preprocessing)
            node_id = component.create_circuit(depth=1)
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
        variable_in_circuit_set = self.__circuit.get_node(self.__circuit.root_id)._get_variable_in_circuit_set(copy=False)
        variable_in_formula_set = self.__cnf.get_variable_set(copy=False)
        unused_variable_set = variable_in_formula_set.difference(variable_in_circuit_set)

        number_of_unused_variables = self.__cnf.number_of_variables - self.__cnf.real_number_of_variables
        sorted_list_temp = sorted(set(range(1, self.__cnf.number_of_variables + 1)).difference(variable_in_formula_set))
        unused_variable_set.update(set(sorted_list_temp[:number_of_unused_variables]))

        for var in unused_variable_set:
            child_id_set = self.__circuit.create_literal_leaf_set({var, -var})
            node_id = self.__circuit.create_or_node(child_id_set, decision_variable=var)
            node_id_set.add(node_id)

        if node_id_set:
            node_id = self.__circuit.create_and_node({root_id}.union(node_id_set))
            self.__circuit.set_root(node_id)

        self.__statistics.compiler_statistics.smooth.start_stopwatch()  # timer (start - smooth)

        # Smooth
        if self.__smooth:
            self.__circuit.smooth()

        self.__statistics.compiler_statistics.smooth.stop_stopwatch()   # timer (stop - smooth)
        self.__statistics.compiler_statistics.create_circuit.stop_stopwatch()   # timer (stop - create_circuit)

        return self.circuit
    # endregion

    # region Property
    @property
    def circuit(self) -> Circuit:
        return self.__circuit

    @property
    def statistics(self) -> Statistics:
        return self.__statistics
    # endregion
