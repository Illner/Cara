# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\formula\cnf\CNF_formulae\large_cnf_valid.cnf"
path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\cnf_formulae\mixdup.cnf"

from compiler.hypergraph_partitioning.hypergraph_partitioning import HypergraphPartitioning
from formula.cnf import Cnf
from compiler.solver import Solver

import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum

cnf = Cnf(path)
hp = HypergraphPartitioning(cnf=cnf,
                            ub_factor=0.1,
                            subsumption_threshold=None,
                            cache_enum=hpc_enum.HypergraphPartitioningCacheEnum.ISOMORFISM_VARIANCE,
                            variable_simplification_enum=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL,
                            node_weight_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                            hyperedge_weight_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                            software_enum=hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS,
                            limit_number_of_clauses_cache=(None, None),
                            limit_number_of_variables_cache=(None, None))

solver = Solver(cnf=cnf,
                sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
                first_implied_literals_enum=il_enum.FirstImpliedLiteralsEnum.IMPLICIT_BCP)

print(cnf.get_incidence_graph())

x = hp.get_cut_set(incidence_graph=cnf.get_incidence_graph(),
                   solver=solver,
                   assignment=[])

print(x)
