import os
import pickle
import other.environment as env
from compiler.compiler import Compiler

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.enum.component_caching_enum as cc_enum
import compiler.enum.heuristic.decision_heuristic_enum as dh_enum
import formula.enum.eliminating_redundant_clauses_enum as erc_enum
import compiler.enum.heuristic.preselection_heuristic_enum as ph_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_patoh_sugparam_enum as hpps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


# folder_path = r"C:\Users\illner\Desktop\RH"
#
# files = [(file, file_path) for file in os.listdir(folder_path) if (os.path.isfile(file_path := os.path.join(folder_path, file)))]
# files = sorted(files)
#
# temp_dict = {}
#
# for i, (file_name, file_path) in enumerate(files):
#     print(f"{i + 1}/{len(files)}")
#
#     length = 0
#
#     with open(file_path, "r") as file:
#         for line in file.readlines():
#             temp = line.split(" ")
#
#             if line.startswith("p cnf"):
#
#                 number_of_variables = int(temp[2])
#                 number_of_clauses = int(temp[3])
#             else:
#                 length += (len(temp) - 1)
#
#     compiler = Compiler(cnf=file_path,
#                         statistics=False,
#                         smooth=False,
#                         preprocessing=False,
#                         imbalance_factor=0.1,
#                         subsumption_threshold=500,
#                         new_cut_set_threshold=0.1,
#                         decision_heuristic_enum=dh_enum.DecisionHeuristicEnum.JEROSLOW_WANG_TWO_SIDED,
#                         sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
#                         base_class_enum_set=set(),
#                         implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
#                         implied_literals_preselection_heuristic_enum=ph_enum.PreselectionHeuristicEnum.NONE,
#                         first_implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
#                         first_implied_literals_preselection_heuristic_enum=ph_enum.PreselectionHeuristicEnum.NONE,
#                         component_caching_enum=cc_enum.ComponentCachingEnum.BASIC_CACHING_SCHEME,
#                         component_caching_before_unit_propagation=False,
#                         component_caching_after_unit_propagation=True,
#                         eliminating_redundant_clauses_enum=erc_enum.EliminatingRedundantClausesEnum.NONE,
#                         eliminating_redundant_clauses_threshold=None,
#                         hp_cache_enum=hpc_enum.HypergraphPartitioningCacheEnum.NONE,
#                         hp_software_enum=hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS if env.is_windows() else hps_enum.HypergraphPartitioningSoftwareEnum.PATOH,
#                         hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
#                         hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
#                         hp_variable_simplification_enum=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL,
#                         hp_patoh_sugparam_enum=hpps_enum.PatohSugparamEnum.QUALITY,
#                         decision_heuristic_vsids_d4_version=True,
#                         decision_heuristic_vsads_p_constant_factor=1,
#                         decision_heuristic_vsads_q_constant_factor=1)
#
#     compiler.create_circuit()
#
#     size = compiler.circuit.size
#
#     temp_dict[file_name] = (number_of_variables, number_of_clauses, size, length)
#     print(f"\t{file_name} \n\t\tSize: {size} \n\t\tRatio: {number_of_clauses / number_of_variables} \n\t\tLength: {length}")
#
#     if i%25 == 0:
#         with open(r"C:\Users\illner\Desktop\temp_dictionary.pkl", "wb") as file:
#             pickle.dump(temp_dict, file, pickle.HIGHEST_PROTOCOL)
#
# print(temp_dict)
#
# with open(r"C:\Users\illner\Desktop\temp_dictionary.pkl", "wb") as file:
#     pickle.dump(temp_dict, file, pickle.HIGHEST_PROTOCOL)

from visualization.plot import scatter

dict_path = r"C:\Users\illner\Desktop\temp_dictionary.pkl"

data = None
data_x = []
data_y = []

with (open(dict_path, "rb")) as file:
    data = pickle.load(file)

print(len(data))

for file_name in data:
    number_of_variables, number_of_clauses, size, length = data[file_name]

    data_x.append(number_of_clauses / number_of_variables)
    data_y.append(size/length)

scatter(data_x, data_y, "")
