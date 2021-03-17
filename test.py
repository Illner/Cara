from pathlib import Path
import os
from datetime import timedelta
from experiment.experiment_abstract import ExperimentAbstract

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.component_caching.component_caching_enum as cc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum

dictionary_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\formula\cnf\CNF_formulae"
path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\SAT benchmarks\D4\qif\sum.32.cnf"
name = "sum.32.cnf"
p = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\temp"
timeout_experiment = timedelta(seconds=10)

a = ExperimentAbstract(directory_path=dictionary_path, experiment_name="name", timeout_experiment=None, log_directory_path=p, save_circuit=False)


result = a._experiment(name, path, smooth=False, ub_factor=0.1, new_cut_set_threshold=0.1, subsumed_threshold=1000,
                       sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
                       implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
                       component_caching_enum=cc_enum.ComponentCachingEnum.BASIC_CACHING_SCHEME,
                       hp_cache_enum=hpc_enum.HypergraphPartitioningCacheEnum.ISOMORFISM,
                       hp_software_enum=hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS,
                       hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                       hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                       hp_variable_simplification_enum=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL,
                       hp_limit_number_of_clauses_cache=(None, 200),
                       hp_limit_number_of_variables_cache=(None, 200))

print(result)
print(a.total_time)
