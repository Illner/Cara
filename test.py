# Import
import time
from formula.cnf import Cnf
from circuit.circuit import Circuit
from compiler.compiler import Compiler

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum

# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\formula\cnf\CNF_formulae\no_comments_valid.cnf"
# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\SAT benchmarks\D4\Handmade\LatinSquare\qg2-08.cnf"
# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\formula\cnf\CNF_formulae\large_cnf_valid.cnf"

path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\compiler\compiler\CNF_formulae\D1119_M20.cnf"

start_time = time.time()

cnf = Cnf(path)

compiler = Compiler(cnf, smooth=False, ub_factor=0.1, new_cut_set_threshold=0.1, subsumed_threshold=1000,
                    sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
                    implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
                    hp_cache_enum=hpc_enum.HypergraphPartitioningCacheEnum.NONE,
                    hp_software_enum=hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS,
                    hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                    hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                    hp_variable_simplification_enum=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL,
                    hp_limit_number_of_clauses_cache=(None, 300),
                    hp_limit_number_of_variables_cache=(None, 300))

circuit = compiler.create_circuit()

end_time = time.time()


print("Time: ", end_time-start_time)
# print(circuit)
print("Number of models: ", circuit.model_counting(set(), set()))
