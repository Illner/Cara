# Import
from formula.cnf import Cnf
from compiler.solver import Solver
from circuit.circuit import Circuit
from typing import Set, Tuple, Union
from compiler.component import Component
from formula.incidence_graph import IncidenceGraph
from compiler_statistics.statistics import Statistics
from compiler.hypergraph_partitioning.hypergraph_partitioning import HypergraphPartitioning

# Import component caching
from compiler.component_caching.none_caching import NoneCaching
from compiler.component_caching.cara_caching_scheme import CaraCachingScheme
from compiler.component_caching.basic_caching_scheme import BasicCachingScheme
from compiler.component_caching.hybrid_caching_scheme import HybridCachingScheme
from compiler.component_caching.standard_caching_scheme import StandardCachingScheme

# Import decision heuristic
from compiler.decision_heuristic.vsids_heuristic import VsidsHeuristic
from compiler.decision_heuristic.vsads_heuristic import VsadsHeuristic
from compiler.decision_heuristic.random_heuristic import RandomHeuristic
from compiler.decision_heuristic.jeroslow_wang_heuristic import JeroslowWangHeuristic
from compiler.decision_heuristic.literal_count_heuristic import LiteralCountHeuristic
from compiler.decision_heuristic.renamable_horn_heuristic import RenamableHornHeuristic
from compiler.decision_heuristic.eupc_heuristic import ExactUnitPropagationCountHeuristic
from compiler.decision_heuristic.clause_reduction_heuristic import ClauseReductionHeuristic
from compiler.decision_heuristic.weighted_binaries_heuristic import WeightedBinariesHeuristic
from compiler.decision_heuristic.maximum_renamable_horn_heuristic import MaximumRenamableHornHeuristic

# Import preselection heuristic
from compiler.preselection_heuristic.none_heuristic import NoneHeuristic
from compiler.preselection_heuristic.prop_z_heuristic import PropZHeuristic
from compiler.preselection_heuristic.clause_reduction_approximation_heuristic import ClauseReductionApproximationHeuristic

# Import exception
import exception.cara_exception as c_exception

# Import enum
import compiler.enum.base_class_enum as bc_enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.enum.component_caching_enum as cc_enum
import formula.enum.lp_formulation_type_enum as lpft_enum
import compiler.enum.heuristic.decision_heuristic_enum as dh_enum
import formula.enum.eliminating_redundant_clauses_enum as erc_enum
import compiler.enum.heuristic.preselection_heuristic_enum as ph_enum
import compiler.enum.heuristic.mixed_difference_heuristic_enum as mdh_enum
import compiler.enum.heuristic.literal_count_heuristic_function_enum as lchf_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_patoh_sugparam_enum as hpps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


class Compiler:
    """
    Compiler
    """

    """    
    Private Cnf cnf
    Private Circuit circuit
    Private Statistics statistics
    Private ComponentCachingAbstract component_caching
    Private DecisionHeuristicAbstract decision_heuristic
    Private HypergraphPartitioning hypergraph_partitioning
    Private PreselectionHeuristicAbstract implied_literals_preselection_heuristic
    Private PreselectionHeuristicAbstract first_implied_literals_preselection_heuristic
    
    Private bool smooth
    Private bool disable_sat
    Private bool cara_circuit
    Private bool preprocessing
    Private str node_statistics
    Private bool cut_set_try_cache
    Private bool strong_determinism
    Private int base_class_threshold
    Private int strong_determinism_max
    Private str mapping_node_statistics
    Private float new_cut_set_threshold
    Private float base_class_ratio_threshold
    Private float new_cut_set_threshold_reduction           # when the cache for cut sets can be used
    Private Set<BaseClassEnum> base_class_enum_set
    Private int eliminating_redundant_clauses_threshold
    Private bool component_caching_after_unit_propagation
    Private bool component_caching_before_unit_propagation
    
    Private SatSolverEnum sat_solver_enum
    Private ImpliedLiteralsEnum implied_literals_enum
    Private HypergraphPartitioningCacheEnum hp_cache_enum
    Private ImpliedLiteralsEnum first_implied_literals_enum
    Private HypergraphPartitioningSoftwareEnum hp_software_enum
    Private HypergraphPartitioningNodeWeightEnum hp_node_weight_type_enum
    Private EliminatingRedundantClausesEnum eliminating_redundant_clauses_enum
    Private HypergraphPartitioningHyperedgeWeightEnum hp_hyperedge_weight_type_enum
    Private HypergraphPartitioningVariableSimplificationEnum hp_variable_simplification_enum
    """

    def __init__(self, cnf: Union[Cnf, str],
                 smooth: bool,
                 statistics: bool,
                 preprocessing: bool,
                 imbalance_factor: Union[float, None],
                 subsumption_threshold: Union[int, None],
                 new_cut_set_threshold: float,
                 decision_heuristic_enum: dh_enum.DecisionHeuristicEnum,
                 sat_solver_enum: ss_enum.SatSolverEnum,
                 base_class_enum_set: Set[bc_enum.BaseClassEnum],
                 implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                 implied_literals_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum,
                 first_implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                 first_implied_literals_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum,
                 component_caching_enum: cc_enum.ComponentCachingEnum,
                 component_caching_before_unit_propagation: bool,
                 component_caching_after_unit_propagation: bool,
                 eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum,
                 eliminating_redundant_clauses_threshold: Union[int, None],
                 hp_cache_enum: hpc_enum.HypergraphPartitioningCacheEnum,
                 hp_software_enum: hps_enum.HypergraphPartitioningSoftwareEnum,
                 hp_node_weight_type_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum,
                 hp_hyperedge_weight_type_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum,
                 hp_variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum,
                 hp_patoh_sugparam_enum: hpps_enum.PatohSugparamEnum = hpps_enum.PatohSugparamEnum.SPEED,
                 hp_multi_occurrence_cache: bool = True,
                 hp_limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                 hp_limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                 base_class_threshold: Union[int, None] = None,
                 base_class_ratio_threshold: Union[float, None] = None,
                 cut_set_try_cache: bool = False,
                 new_cut_set_threshold_reduction: float = 1,
                 implied_literals_preselection_heuristic_prop_z_depth_threshold: int = 5,
                 implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound: Union[int, None] = 10,
                 implied_literals_preselection_heuristic_cra_rank: float = 0.1,
                 first_implied_literals_preselection_heuristic_prop_z_depth_threshold: int = 5,
                 first_implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound: Union[int, None] = 10,
                 first_implied_literals_preselection_heuristic_cra_rank: float = 0.1,
                 decision_heuristic_mixed_difference_enum: mdh_enum.MixedDifferenceHeuristicEnum = mdh_enum.MixedDifferenceHeuristicEnum.OK_SOLVER,
                 decision_heuristic_vsids_d4_version: bool = True,
                 decision_heuristic_vsads_p_constant_factor: float = 1,
                 decision_heuristic_vsads_q_constant_factor: float = 0.5,
                 decision_heuristic_weight_for_satisfied_clauses: bool = True,
                 decision_heuristic_ignore_binary_clauses: bool = False,
                 decision_heuristic_renamable_horn_use_total_number_of_conflict_variables: bool = True,
                 decision_heuristic_renamable_horn_use_conflicts: bool = True,
                 decision_heuristic_renamable_horn_use_auxiliary_variables: bool = False,
                 decision_heuristic_renamable_horn_prefer_conflict_variables: bool = True,
                 decision_heuristic_maximum_renamable_horn_is_exact: bool = True,
                 decision_heuristic_maximum_renamable_horn_use_conflicts: bool = True,
                 decision_heuristic_maximum_renamable_horn_prefer_conflict_variables: bool = True,
                 decision_heuristic_maximum_renamable_horn_lp_formulation_type: lpft_enum.LpFormulationTypeEnum = lpft_enum.LpFormulationTypeEnum.HORN_FORMULA,
                 decision_heuristic_maximum_renamable_horn_weight_for_variables_not_in_cut_set: int = 2,
                 decision_heuristic_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum = ph_enum.PreselectionHeuristicEnum.NONE,
                 decision_heuristic_preselection_heuristic_prop_z_depth_threshold: int = 5,
                 decision_heuristic_preselection_heuristic_prop_z_number_of_variables_lower_bound: Union[int, None] = 10,
                 decision_heuristic_preselection_heuristic_cra_rank: float = 0.1,
                 component_caching_cara_caching_scheme_multi_occurrence: bool = False,
                 component_caching_cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold: int = 0,
                 name: str = "",
                 mapping_node_statistics: Union[str, None] = None,
                 node_statistics: Union[str, None] = None,
                 disable_sat: bool = False,
                 disable_decomposition: bool = False,
                 cara_circuit: bool = True,
                 strong_determinism: bool = False,
                 strong_determinism_max: Union[int, None] = None):
        # Invalid configurations
        if disable_sat and ((implied_literals_enum != il_enum.ImpliedLiteralsEnum.BCP) or (first_implied_literals_enum != il_enum.ImpliedLiteralsEnum.BCP)):
            raise c_exception.InvalidConfigurationException("BCP is needed for disable_sat")

        # CNF
        if isinstance(cnf, Cnf):
            self.__cnf: Cnf = cnf
            self.__statistics: Statistics = Statistics(active=statistics,
                                                       cnf_statistics=self.__cnf.cnf_statistics,
                                                       incidence_graph_statistics=self.__cnf.incidence_graph_statistics,
                                                       renamable_horn_formula_lp_formulation_statistics=self.__cnf.renamable_horn_formula_lp_formulation_statistics)
        else:
            self.__statistics: Statistics = Statistics(active=statistics)
            self.__cnf: Cnf = Cnf(dimacs_cnf_source=cnf,
                                  cnf_statistics=self.__statistics.cnf_statistics,
                                  incidence_graph_statistics=self.__statistics.incidence_graph_statistics,
                                  renamable_horn_formula_lp_formulation_statistics=self.__statistics.renamable_horn_formula_lp_formulation_statistics)

        self.__statistics.set_name(name)

        self.__smooth: bool = smooth
        self.__circuit: Circuit = Circuit()
        self.__disable_sat: bool = disable_sat
        self.__cara_circuit: bool = cara_circuit
        self.__preprocessing: bool = preprocessing
        self.__cut_set_try_cache: bool = cut_set_try_cache
        self.__strong_determinism: bool = strong_determinism
        self.__node_statistics: Union[str, None] = node_statistics
        self.__new_cut_set_threshold: float = new_cut_set_threshold
        self.__base_class_threshold: Union[int, None] = base_class_threshold
        self.__strong_determinism_max: Union[int, None] = strong_determinism_max
        self.__mapping_node_statistics: Union[str, None] = mapping_node_statistics
        self.__base_class_enum_set: Set[bc_enum.BaseClassEnum] = base_class_enum_set
        self.__new_cut_set_threshold_reduction: float = new_cut_set_threshold_reduction
        self.__base_class_ratio_threshold: Union[float, None] = base_class_ratio_threshold
        self.__component_caching_after_unit_propagation: bool = component_caching_after_unit_propagation
        self.__component_caching_before_unit_propagation: bool = component_caching_before_unit_propagation
        self.__eliminating_redundant_clauses_threshold: Union[int, None] = eliminating_redundant_clauses_threshold

        self.__sat_solver_enum: ss_enum.SatSolverEnum = sat_solver_enum
        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum
        self.__first_implied_literals_enum: il_enum.ImpliedLiteralsEnum = first_implied_literals_enum
        self.__eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum = eliminating_redundant_clauses_enum

        # Component caching
        self.__set_component_caching(component_caching_enum=component_caching_enum,
                                     cara_caching_scheme_multi_occurrence=component_caching_cara_caching_scheme_multi_occurrence,
                                     cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold=component_caching_cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold)

        # Decision heuristic
        self.__set_decision_heuristic(decision_heuristic_enum=decision_heuristic_enum,
                                      mixed_difference_heuristic_enum=decision_heuristic_mixed_difference_enum,
                                      vsids_d4_version=decision_heuristic_vsids_d4_version,
                                      vsads_p_constant_factor=decision_heuristic_vsads_p_constant_factor,
                                      vsads_q_constant_factor=decision_heuristic_vsads_q_constant_factor,
                                      weight_for_satisfied_clauses=decision_heuristic_weight_for_satisfied_clauses,
                                      ignore_binary_clauses=decision_heuristic_ignore_binary_clauses,
                                      decision_heuristic_preselection_heuristic_enum=decision_heuristic_preselection_heuristic_enum,
                                      prop_z_depth_threshold=decision_heuristic_preselection_heuristic_prop_z_depth_threshold,
                                      prop_z_number_of_variables_lower_bound=decision_heuristic_preselection_heuristic_prop_z_number_of_variables_lower_bound,
                                      cra_rank=decision_heuristic_preselection_heuristic_cra_rank,
                                      renamable_horn_use_total_number_of_conflict_variables=decision_heuristic_renamable_horn_use_total_number_of_conflict_variables,
                                      renamable_horn_use_conflicts=decision_heuristic_renamable_horn_use_conflicts,
                                      renamable_horn_use_auxiliary_variables=decision_heuristic_renamable_horn_use_auxiliary_variables,
                                      renamable_horn_prefer_conflict_variables=decision_heuristic_renamable_horn_prefer_conflict_variables,
                                      maximum_renamable_horn_is_exact=decision_heuristic_maximum_renamable_horn_is_exact,
                                      maximum_renamable_horn_use_conflicts=decision_heuristic_maximum_renamable_horn_use_conflicts,
                                      maximum_renamable_horn_prefer_conflict_variables=decision_heuristic_maximum_renamable_horn_prefer_conflict_variables,
                                      maximum_renamable_horn_lp_formulation_type=decision_heuristic_maximum_renamable_horn_lp_formulation_type,
                                      maximum_renamable_horn_weight_for_variables_not_in_cut_set=decision_heuristic_maximum_renamable_horn_weight_for_variables_not_in_cut_set)

        # Implied literals - preselection heuristic
        self.__set_implied_literals_preselection_heuristic(implied_literals_preselection_heuristic_enum=implied_literals_preselection_heuristic_enum,
                                                           prop_z_depth_threshold=implied_literals_preselection_heuristic_prop_z_depth_threshold,
                                                           prop_z_number_of_variables_lower_bound=implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound,
                                                           cra_rank=implied_literals_preselection_heuristic_cra_rank)

        # First implied literals - preselection heuristic
        self.__set_first_implied_literals_preselection_heuristic(first_implied_literals_preselection_heuristic_enum=first_implied_literals_preselection_heuristic_enum,
                                                                 prop_z_depth_threshold=first_implied_literals_preselection_heuristic_prop_z_depth_threshold,
                                                                 prop_z_number_of_variables_lower_bound=first_implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound,
                                                                 cra_rank=first_implied_literals_preselection_heuristic_cra_rank)

        # Hypergraph partitioning
        self.__hypergraph_partitioning = HypergraphPartitioning(cnf=self.__cnf,
                                                                imbalance_factor=imbalance_factor,
                                                                subsumption_threshold=subsumption_threshold,
                                                                cache_enum=hp_cache_enum,
                                                                software_enum=hp_software_enum,
                                                                node_weight_enum=hp_node_weight_type_enum,
                                                                hyperedge_weight_enum=hp_hyperedge_weight_type_enum,
                                                                variable_simplification_enum=hp_variable_simplification_enum,
                                                                multi_occurrence_cache=hp_multi_occurrence_cache,
                                                                limit_number_of_clauses_cache=hp_limit_number_of_clauses_cache,
                                                                limit_number_of_variables_cache=hp_limit_number_of_variables_cache,
                                                                disable_decomposition=disable_decomposition,
                                                                patoh_sugparam_enum=hp_patoh_sugparam_enum,
                                                                statistics=self.__statistics.hypergraph_partitioning_statistics)

    # region Private method
    def __set_component_caching(self, component_caching_enum: cc_enum.ComponentCachingEnum,
                                cara_caching_scheme_multi_occurrence: bool,
                                cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold: int) -> None:
        # NONE
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

        # CARA_CACHING_SCHEME
        if component_caching_enum == cc_enum.ComponentCachingEnum.CARA_CACHING_SCHEME:
            self.__component_caching = CaraCachingScheme(multi_occurrence=cara_caching_scheme_multi_occurrence,
                                                         basic_caching_scheme_number_of_variables_threshold=cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold)
            return

        raise c_exception.FunctionNotImplementedException("set_component_caching",
                                                          f"this type of component caching ({component_caching_enum.name}) is not implemented")

    def __set_decision_heuristic(self, decision_heuristic_enum: dh_enum.DecisionHeuristicEnum,
                                 mixed_difference_heuristic_enum: mdh_enum.MixedDifferenceHeuristicEnum,
                                 vsids_d4_version: bool,
                                 vsads_p_constant_factor: float,
                                 vsads_q_constant_factor: float,
                                 weight_for_satisfied_clauses: bool,
                                 ignore_binary_clauses: bool,
                                 decision_heuristic_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum,
                                 prop_z_depth_threshold: int,
                                 prop_z_number_of_variables_lower_bound: Union[int, None],
                                 cra_rank: float,
                                 renamable_horn_use_total_number_of_conflict_variables: bool,
                                 renamable_horn_use_conflicts: bool,
                                 renamable_horn_use_auxiliary_variables: bool,
                                 renamable_horn_prefer_conflict_variables: bool,
                                 maximum_renamable_horn_is_exact: bool,
                                 maximum_renamable_horn_use_conflicts: bool,
                                 maximum_renamable_horn_prefer_conflict_variables: bool,
                                 maximum_renamable_horn_lp_formulation_type: lpft_enum.LpFormulationTypeEnum,
                                 maximum_renamable_horn_weight_for_variables_not_in_cut_set) -> None:

        # Preselection heuristic
        # NONE
        if decision_heuristic_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.NONE:
            preselection_heuristic = NoneHeuristic(statistics=self.__statistics.preselection_heuristic_decision_heuristic_statistics)

        # PROP_Z
        elif decision_heuristic_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.PROP_Z:
            preselection_heuristic = PropZHeuristic(depth_threshold=prop_z_depth_threshold,
                                                    number_of_variables_lower_bound=prop_z_number_of_variables_lower_bound,
                                                    statistics=self.__statistics.preselection_heuristic_decision_heuristic_statistics)

        # CRA
        elif decision_heuristic_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.CRA:
            preselection_heuristic = ClauseReductionApproximationHeuristic(rank=cra_rank,
                                                                           total_number_of_variables=self.__cnf.real_number_of_variables,
                                                                           statistics=self.__statistics.preselection_heuristic_decision_heuristic_statistics)

        # Undefined
        else:
            raise c_exception.FunctionNotImplementedException("set_decision_heuristic",
                                                              f"this type of preselection heuristic ({decision_heuristic_preselection_heuristic_enum.name}) is not implemented")

        # Decision heuristic
        # RANDOM
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.RANDOM:
            self.__decision_heuristic = RandomHeuristic(preselection_heuristic=preselection_heuristic)
            return

        # JEROSLOW_WANG_ONE_SIDED, JEROSLOW_WANG_TWO_SIDED
        if (decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.JEROSLOW_WANG_ONE_SIDED) or \
           (decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.JEROSLOW_WANG_TWO_SIDED):
            one_sided = True if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.JEROSLOW_WANG_ONE_SIDED else False
            self.__decision_heuristic = JeroslowWangHeuristic(preselection_heuristic=preselection_heuristic,
                                                              one_sided=one_sided,
                                                              ignore_binary_clauses=ignore_binary_clauses)
            return

        # CLAUSE_REDUCTION
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.CLAUSE_REDUCTION:
            self.__decision_heuristic = ClauseReductionHeuristic(preselection_heuristic=preselection_heuristic,
                                                                 weight_for_satisfied_clauses=weight_for_satisfied_clauses,
                                                                 mixed_difference_heuristic_enum=mixed_difference_heuristic_enum)
            return

        # WEIGHTED_BINARIES
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.WEIGHTED_BINARIES:
            self.__decision_heuristic = WeightedBinariesHeuristic(preselection_heuristic=preselection_heuristic,
                                                                  mixed_difference_heuristic_enum=mixed_difference_heuristic_enum,
                                                                  weight_for_satisfied_clauses=weight_for_satisfied_clauses,
                                                                  backbone_search_heuristic=False)
            return

        # BACKBONE_SEARCH
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.BACKBONE_SEARCH:
            self.__decision_heuristic = WeightedBinariesHeuristic(preselection_heuristic=preselection_heuristic,
                                                                  mixed_difference_heuristic_enum=mixed_difference_heuristic_enum,
                                                                  weight_for_satisfied_clauses=weight_for_satisfied_clauses,
                                                                  backbone_search_heuristic=True)
            return

        # DLCS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.DLCS:
            self.__decision_heuristic = LiteralCountHeuristic(preselection_heuristic=preselection_heuristic,
                                                              ignore_binary_clauses=ignore_binary_clauses,
                                                              function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.SUM,
                                                              tie_breaker_function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.SUM)
            return

        # DLIS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.DLIS:
            self.__decision_heuristic = LiteralCountHeuristic(preselection_heuristic=preselection_heuristic,
                                                              ignore_binary_clauses=ignore_binary_clauses,
                                                              function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.MAX,
                                                              tie_breaker_function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.MAX)
            return

        # DLCS_DLIS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.DLCS_DLIS:
            self.__decision_heuristic = LiteralCountHeuristic(preselection_heuristic=preselection_heuristic,
                                                              ignore_binary_clauses=ignore_binary_clauses,
                                                              function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.SUM,
                                                              tie_breaker_function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.MAX)
            return

        # EUPC
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.EUPC:
            self.__decision_heuristic = ExactUnitPropagationCountHeuristic(preselection_heuristic=preselection_heuristic,
                                                                           mixed_difference_heuristic_enum=mixed_difference_heuristic_enum)
            return

        # VSIDS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.VSIDS:
            self.__decision_heuristic = VsidsHeuristic(preselection_heuristic=preselection_heuristic,
                                                       d4_version=vsids_d4_version)
            return

        # VSADS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.VSADS:
            self.__decision_heuristic = VsadsHeuristic(preselection_heuristic=preselection_heuristic,
                                                       ignore_binary_clauses=ignore_binary_clauses,
                                                       p_constant_factor=vsads_p_constant_factor,
                                                       q_constant_factor=vsads_q_constant_factor,
                                                       vsids_d4_version=vsids_d4_version)
            return

        # RENAMABLE_HORN_JEROSLOW_WANG_TWO_SIDED
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.RENAMABLE_HORN_JEROSLOW_WANG_TWO_SIDED:
            decision_heuristic = JeroslowWangHeuristic(preselection_heuristic=NoneHeuristic(),
                                                       one_sided=False,
                                                       ignore_binary_clauses=ignore_binary_clauses)

            self.__decision_heuristic = RenamableHornHeuristic(preselection_heuristic=preselection_heuristic,
                                                               decision_heuristic=decision_heuristic,
                                                               use_total_number_of_conflict_variables=renamable_horn_use_total_number_of_conflict_variables,
                                                               use_conflicts=renamable_horn_use_conflicts,
                                                               use_auxiliary_variables=renamable_horn_use_auxiliary_variables,
                                                               prefer_conflict_variables=renamable_horn_prefer_conflict_variables)
            return

        # RENAMABLE_HORN_DLCS_DLIS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.RENAMABLE_HORN_DLCS_DLIS:
            decision_heuristic = LiteralCountHeuristic(preselection_heuristic=NoneHeuristic(),
                                                       ignore_binary_clauses=ignore_binary_clauses,
                                                       function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.SUM,
                                                       tie_breaker_function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.MAX)

            self.__decision_heuristic = RenamableHornHeuristic(preselection_heuristic=preselection_heuristic,
                                                               decision_heuristic=decision_heuristic,
                                                               use_total_number_of_conflict_variables=renamable_horn_use_total_number_of_conflict_variables,
                                                               use_conflicts=renamable_horn_use_conflicts,
                                                               use_auxiliary_variables=renamable_horn_use_auxiliary_variables,
                                                               prefer_conflict_variables=renamable_horn_prefer_conflict_variables)
            return

        # RENAMABLE_HORN_VSADS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.RENAMABLE_HORN_VSADS:
            decision_heuristic = VsadsHeuristic(preselection_heuristic=NoneHeuristic(),
                                                ignore_binary_clauses=ignore_binary_clauses,
                                                p_constant_factor=vsads_p_constant_factor,
                                                q_constant_factor=vsads_q_constant_factor,
                                                vsids_d4_version=vsids_d4_version)

            self.__decision_heuristic = RenamableHornHeuristic(preselection_heuristic=preselection_heuristic,
                                                               decision_heuristic=decision_heuristic,
                                                               use_total_number_of_conflict_variables=renamable_horn_use_total_number_of_conflict_variables,
                                                               use_conflicts=renamable_horn_use_conflicts,
                                                               use_auxiliary_variables=renamable_horn_use_auxiliary_variables,
                                                               prefer_conflict_variables=renamable_horn_prefer_conflict_variables)
            return

        # MAXIMUM_RENAMABLE_HORN_JEROSLOW_WANG_TWO_SIDED
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.MAXIMUM_RENAMABLE_HORN_JEROSLOW_WANG_TWO_SIDED:
            decision_heuristic = JeroslowWangHeuristic(preselection_heuristic=NoneHeuristic(),
                                                       one_sided=False,
                                                       ignore_binary_clauses=ignore_binary_clauses)

            self.__decision_heuristic = MaximumRenamableHornHeuristic(preselection_heuristic=preselection_heuristic,
                                                                      decision_heuristic=decision_heuristic,
                                                                      is_exact=maximum_renamable_horn_is_exact,
                                                                      use_conflicts=maximum_renamable_horn_use_conflicts,
                                                                      prefer_conflict_variables=maximum_renamable_horn_prefer_conflict_variables,
                                                                      lp_formulation_type=maximum_renamable_horn_lp_formulation_type,
                                                                      weight_for_variables_not_in_cut_set=maximum_renamable_horn_weight_for_variables_not_in_cut_set)
            return

        # MAXIMUM_RENAMABLE_HORN_DLCS_DLIS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.MAXIMUM_RENAMABLE_HORN_DLCS_DLIS:
            decision_heuristic = LiteralCountHeuristic(preselection_heuristic=NoneHeuristic(),
                                                       ignore_binary_clauses=ignore_binary_clauses,
                                                       function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.SUM,
                                                       tie_breaker_function_enum=lchf_enum.LiteralCountHeuristicFunctionEnum.MAX)

            self.__decision_heuristic = MaximumRenamableHornHeuristic(preselection_heuristic=preselection_heuristic,
                                                                      decision_heuristic=decision_heuristic,
                                                                      is_exact=maximum_renamable_horn_is_exact,
                                                                      use_conflicts=maximum_renamable_horn_use_conflicts,
                                                                      prefer_conflict_variables=maximum_renamable_horn_prefer_conflict_variables,
                                                                      lp_formulation_type=maximum_renamable_horn_lp_formulation_type,
                                                                      weight_for_variables_not_in_cut_set=maximum_renamable_horn_weight_for_variables_not_in_cut_set)
            return

        # MAXIMUM_RENAMABLE_HORN_VSADS
        if decision_heuristic_enum == dh_enum.DecisionHeuristicEnum.MAXIMUM_RENAMABLE_HORN_VSADS:
            decision_heuristic = VsadsHeuristic(preselection_heuristic=NoneHeuristic(),
                                                ignore_binary_clauses=ignore_binary_clauses,
                                                p_constant_factor=vsads_p_constant_factor,
                                                q_constant_factor=vsads_q_constant_factor,
                                                vsids_d4_version=vsids_d4_version)

            self.__decision_heuristic = MaximumRenamableHornHeuristic(preselection_heuristic=preselection_heuristic,
                                                                      decision_heuristic=decision_heuristic,
                                                                      is_exact=maximum_renamable_horn_is_exact,
                                                                      use_conflicts=maximum_renamable_horn_use_conflicts,
                                                                      prefer_conflict_variables=maximum_renamable_horn_prefer_conflict_variables,
                                                                      lp_formulation_type=maximum_renamable_horn_lp_formulation_type,
                                                                      weight_for_variables_not_in_cut_set=maximum_renamable_horn_weight_for_variables_not_in_cut_set)
            return

        raise c_exception.FunctionNotImplementedException("set_decision_heuristic",
                                                          f"this type of decision heuristic ({decision_heuristic_enum.name}) is not implemented")

    def __set_implied_literals_preselection_heuristic(self, implied_literals_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum,
                                                      prop_z_depth_threshold: int, prop_z_number_of_variables_lower_bound: Union[int, None],
                                                      cra_rank: float) -> None:
        # NONE
        if implied_literals_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.NONE:
            self.__implied_literals_preselection_heuristic = NoneHeuristic(statistics=self.__statistics.preselection_heuristic_implied_literals_statistics)
            return

        # PROP_Z
        if implied_literals_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.PROP_Z:
            self.__implied_literals_preselection_heuristic = PropZHeuristic(depth_threshold=prop_z_depth_threshold,
                                                                            number_of_variables_lower_bound=prop_z_number_of_variables_lower_bound,
                                                                            statistics=self.__statistics.preselection_heuristic_implied_literals_statistics)
            return

        # CRA
        if implied_literals_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.CRA:
            self.__implied_literals_preselection_heuristic = ClauseReductionApproximationHeuristic(rank=cra_rank,
                                                                                                   total_number_of_variables=self.__cnf.real_number_of_variables,
                                                                                                   statistics=self.__statistics.preselection_heuristic_implied_literals_statistics)
            return

        raise c_exception.FunctionNotImplementedException("set_implied_literals_preselection_heuristic",
                                                          f"this type of preselection heuristic ({implied_literals_preselection_heuristic_enum.name}) is not implemented")
    # endregion

    def __set_first_implied_literals_preselection_heuristic(self, first_implied_literals_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum,
                                                            prop_z_depth_threshold: int, prop_z_number_of_variables_lower_bound: Union[int, None],
                                                            cra_rank: float) -> None:
        # NONE
        if first_implied_literals_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.NONE:
            self.__first_implied_literals_preselection_heuristic = NoneHeuristic(statistics=self.__statistics.preselection_heuristic_first_implied_literals_statistics)
            return

        # PROP_Z
        if first_implied_literals_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.PROP_Z:
            self.__first_implied_literals_preselection_heuristic = PropZHeuristic(depth_threshold=prop_z_depth_threshold,
                                                                                  number_of_variables_lower_bound=prop_z_number_of_variables_lower_bound,
                                                                                  statistics=self.__statistics.preselection_heuristic_first_implied_literals_statistics)
            return

        # CRA
        if first_implied_literals_preselection_heuristic_enum == ph_enum.PreselectionHeuristicEnum.CRA:
            self.__first_implied_literals_preselection_heuristic = ClauseReductionApproximationHeuristic(rank=cra_rank,
                                                                                                         total_number_of_variables=self.__cnf.real_number_of_variables,
                                                                                                         statistics=self.__statistics.preselection_heuristic_first_implied_literals_statistics)
            return

        raise c_exception.FunctionNotImplementedException("set_first_implied_literals_preselection_heuristic",
                                                          f"this type of preselection heuristic ({first_implied_literals_preselection_heuristic_enum.name}) is not implemented")

    # region Public method
    def create_circuit(self) -> Circuit:
        """
        Create the circuit
        :return: the created circuit
        """

        self.__statistics.compiler_statistics.create_circuit.start_stopwatch()  # timer (start - create_circuit)

        incidence_graph: IncidenceGraph = self.__cnf._incidence_graph
        incidence_graph_set: Set[IncidenceGraph] = {incidence_graph}

        # More components exist
        if not incidence_graph.is_connected():
            incidence_graph_set = incidence_graph.create_incidence_graphs_for_components()

        node_id_set: Set[int] = set()
        for incidence_graph in incidence_graph_set:
            # Renamable Horn CNF
            if bc_enum.BaseClassEnum.RENAMABLE_HORN_CNF in self.__base_class_enum_set:
                incidence_graph.initialize_renamable_horn_formula_recognition()

            # Solver
            solver = Solver(cnf=self.__cnf,
                            sat_solver_enum=self.__sat_solver_enum,
                            first_implied_literals_enum=il_enum.ImpliedLiteralsEnum.BACKBONE if self.__preprocessing else il_enum.ImpliedLiteralsEnum.IMPLICIT_BCP,
                            incidence_graph=incidence_graph,
                            propagate_sat_solver_enum=None if not self.__disable_sat else ss_enum.PropagateSatSolverEnum.MiniSAT,
                            statistics=self.__statistics.solver_statistics)

            component = Component(cnf=self.__cnf,
                                  solver=solver,
                                  circuit=self.__circuit,
                                  assignment_list=[],
                                  new_cut_set_threshold=self.__new_cut_set_threshold,
                                  new_cut_set_threshold_reduction=self.__new_cut_set_threshold_reduction,
                                  cut_set_try_cache=self.__cut_set_try_cache,
                                  incidence_graph=incidence_graph,
                                  decision_heuristic=self.__decision_heuristic,
                                  component_caching=self.__component_caching,
                                  component_caching_before_unit_propagation=self.__component_caching_before_unit_propagation,
                                  component_caching_after_unit_propagation=self.__component_caching_after_unit_propagation,
                                  eliminating_redundant_clauses_enum=self.__eliminating_redundant_clauses_enum,
                                  eliminating_redundant_clauses_threshold=self.__eliminating_redundant_clauses_threshold,
                                  hypergraph_partitioning=self.__hypergraph_partitioning,
                                  base_class_enum_set=self.__base_class_enum_set,
                                  base_class_threshold=self.__base_class_threshold,
                                  base_class_ratio_threshold=self.__base_class_ratio_threshold,
                                  implied_literals_enum=self.__implied_literals_enum,
                                  implied_literals_preselection_heuristic=self.__implied_literals_preselection_heuristic,
                                  first_implied_literals_enum=self.__first_implied_literals_enum,
                                  first_implied_literals_preselection_heuristic=self.__first_implied_literals_preselection_heuristic,
                                  statistics=self.__statistics,
                                  mapping_node_statistics=self.__mapping_node_statistics,
                                  node_statistics=self.__node_statistics,
                                  disable_sat=self.__disable_sat,
                                  cara_circuit=self.__cara_circuit,
                                  strong_determinism=self.__strong_determinism,
                                  strong_determinism_max=self.__strong_determinism_max)
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
        variable_in_circuit_set = self.__circuit.get_node(root_id)._variable_in_circuit_set
        variable_in_formula_set = self.__cnf._variable_set
        unused_variable_set = variable_in_formula_set.difference(variable_in_circuit_set)

        number_of_unused_variables = self.__cnf.number_of_variables - self.__cnf.real_number_of_variables
        sorted_list_temp = sorted(set(range(1, self.__cnf.number_of_variables + 1)).difference(variable_in_formula_set))
        unused_variable_set.update(set(sorted_list_temp[:number_of_unused_variables]))

        node_id_set = set()
        for var in unused_variable_set:
            child_id_set = self.__circuit.create_literal_leaf_set({var, -var})
            node_id = self.__circuit.create_or_node(child_id_set, decision_variable=var)
            node_id_set.add(node_id)

        if node_id_set:
            root_id = self.__circuit.create_and_node({root_id}.union(node_id_set))
            self.__circuit.set_root(root_id)

        # Smooth
        if self.__smooth:
            self.__statistics.compiler_statistics.smooth.start_stopwatch()  # timer (start - smooth)
            self.__circuit.smooth()
            self.__statistics.compiler_statistics.smooth.stop_stopwatch()   # timer (stop - smooth)

        # Statistics
        self.__statistics.set_compiled()
        self.__statistics.set_size(self.__circuit.size)
        self.__statistics.set_number_of_edges(self.__circuit.number_of_edges)
        self.__statistics.set_number_of_nodes(self.__circuit.number_of_nodes)
        self.__statistics.set_number_of_variables(self.__circuit.number_of_variables)
        node_type_dictionary_temp = self.__circuit.get_node_type_dictionary()
        self.__statistics.set_node_type_dictionary(node_type_dictionary_temp)

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
