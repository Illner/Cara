# Import
import os
from formula.cnf import Cnf
from compiler.compiler import Compiler
from tests.test_abstract import TestAbstract

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.component_caching.component_caching_enum as cc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


class CompilerTest(TestAbstract):
    __FOLDER: str = os.path.join("compiler", "compiler")

    def __init__(self):
        super().__init__(CompilerTest.__FOLDER, test_name="Compiler test")
        self._set_files(CompilerTest.__FOLDER, "CNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        for (file_name, file_path) in self._files:
            count = 0
            print()
            print(f"File ({file_name}): ", end="")

            for implied_literals_enum in il_enum.implied_literals_enum_values:
                for hp_cache_enum in hpc_enum.hpc_enum_values:
                    for hp_variable_simplification_enum in hpvs_enum.hpvs_enum_values:
                        for subsumed_threshold in [100, None]:
                            for new_cut_set_threshold in [0, 0.5, 1]:
                                try:
                                    count += 1

                                    actual_result = "\n".join((actual_result,
                                                               f"File: {file_name}, "
                                                               f"implied literals: {il_enum.ImpliedLiteralsEnum(implied_literals_enum).name}, "
                                                               f"cache: {hpc_enum.HypergraphPartitioningCacheEnum(hp_cache_enum).name}, "
                                                               f"variable simplification: {hpvs_enum.HypergraphPartitioningVariableSimplificationEnum(hp_variable_simplification_enum).name}, "
                                                               f"subsumed threshold: {subsumed_threshold}, "
                                                               f"new cut set threshold: {new_cut_set_threshold}"))

                                    cnf = Cnf(file_path)
                                    compiler = Compiler(cnf=cnf,
                                                        smooth=True,
                                                        ub_factor=0.1,
                                                        subsumed_threshold=subsumed_threshold,
                                                        new_cut_set_threshold=new_cut_set_threshold,
                                                        sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
                                                        implied_literals_enum=implied_literals_enum,
                                                        component_caching_enum=cc_enum.ComponentCachingEnum.STANDARD_CACHING_SCHEME,
                                                        hp_cache_enum=hp_cache_enum,
                                                        hp_software_enum=hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS,
                                                        hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                                                        hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                                                        hp_variable_simplification_enum=hp_variable_simplification_enum,
                                                        hp_limit_number_of_clauses_cache=(None, 100),
                                                        hp_limit_number_of_variables_cache=(None, 100))
                                    circuit = compiler.create_circuit()
                                    number_of_models = circuit.model_counting(set(), set())
                                    real_number_of_models = int(cnf.comments)

                                    if number_of_models == real_number_of_models:
                                        actual_result = "\n".join((actual_result, f"Correct", ""))
                                        print("|", end="" if count % 10 != 0 else " ")
                                    else:
                                        actual_result = "\n".join((actual_result, f"Incorrect: {number_of_models} vs {real_number_of_models}", ""))
                                        print("X", end="" if count % 10 != 0 else " ")

                                except Exception as err:
                                    print("E", end="" if count % 10 != 0 else " ")
                                    actual_result = "\n".join((actual_result, str(err), ""))

        print()
        return actual_result
    # endregion
