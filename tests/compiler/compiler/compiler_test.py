# Import
import os
from formula.cnf import Cnf
import other.environment as env
from compiler.compiler import Compiler
from tests.test_abstract import TestAbstract

# Import exception
import exception.cara_exception as c_exception

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
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


class CompilerTest(TestAbstract):
    __DIRECTORY: str = os.path.join("compiler", "compiler")

    def __init__(self, limit: int):
        super().__init__(CompilerTest.__DIRECTORY, test_name="Compiler test")
        self._set_files(CompilerTest.__DIRECTORY, "CNF_formulae")

        self.__limit: int = limit

    # region Override method
    def _get_actual_result(self) -> str:
        for (file_name, file_path) in self._files:
            print()
            print(f"File ({file_name}): ")

            if file_name == "ais6.cnf":
                self.__test(file_path)

        print()
        return ""
    # endregion

    # region Private method
    def __test(self, file_path: str):
        count = 0

        hp_software_enum = hps_enum.HypergraphPartitioningSoftwareEnum.PATOH
        if env.is_windows():
            hp_software_enum = hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS

        for implied_literals_preselection_heuristic_enum in ph_enum.preselection_heuristic_enum_values:
            for first_implied_literals_preselection_heuristic_enum in ph_enum.preselection_heuristic_enum_values:
                for new_cut_set_threshold in [0, 0.5, 1]:
                    for subsumed_threshold in [100, None]:
                        for eliminating_redundant_clauses_enum in erc_enum.eliminating_redundant_clauses_enum_values:
                            for eliminating_redundant_clauses_threshold in [100, None]:
                                for hp_cache_enum in hpc_enum.hpc_enum_values:
                                    for decision_heuristic_vsids_d4_version in [True, False]:
                                        for decision_heuristic_weight_for_satisfied_clauses in [True, False]:
                                            for decision_heuristic_ignore_binary_clauses in [True, False]:
                                                for component_caching_enum in [cc_enum.ComponentCachingEnum.CARA_CACHING_SCHEME, cc_enum.ComponentCachingEnum.BASIC_CACHING_SCHEME]:
                                                    for component_caching_before_unit_propagation in [True, False]:
                                                        for component_caching_after_unit_propagation in [True, False]:
                                                            for smooth in [True, False]:
                                                                for disable_sat in [True, False]:
                                                                    for decision_heuristic_enum in dh_enum.decision_heuristic_enum_values:
                                                                        for first_implied_literals_enum in il_enum.implied_literals_enum_values:
                                                                            for implied_literals_enum in il_enum.implied_literals_enum_values:
                                                                                for hp_variable_simplification_enum in hpvs_enum.hpvs_enum_values:
                                                                                    try:
                                                                                        count += 1

                                                                                        cnf = Cnf(file_path)
                                                                                        compiler = Compiler(cnf=cnf,
                                                                                                            smooth=smooth,
                                                                                                            statistics=False,
                                                                                                            preprocessing=False,
                                                                                                            imbalance_factor=0.1,
                                                                                                            subsumption_threshold=subsumed_threshold,
                                                                                                            new_cut_set_threshold=new_cut_set_threshold,
                                                                                                            decision_heuristic_enum=decision_heuristic_enum,
                                                                                                            sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
                                                                                                            base_class_enum_set=set(),
                                                                                                            implied_literals_enum=implied_literals_enum,
                                                                                                            implied_literals_preselection_heuristic_enum=implied_literals_preselection_heuristic_enum,
                                                                                                            first_implied_literals_enum=first_implied_literals_enum,
                                                                                                            first_implied_literals_preselection_heuristic_enum=first_implied_literals_preselection_heuristic_enum,
                                                                                                            component_caching_enum=component_caching_enum,
                                                                                                            component_caching_before_unit_propagation=component_caching_before_unit_propagation,
                                                                                                            component_caching_after_unit_propagation=component_caching_after_unit_propagation,
                                                                                                            eliminating_redundant_clauses_enum=eliminating_redundant_clauses_enum,
                                                                                                            eliminating_redundant_clauses_threshold=eliminating_redundant_clauses_threshold,
                                                                                                            hp_cache_enum=hp_cache_enum,
                                                                                                            hp_software_enum=hp_software_enum,
                                                                                                            hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                                                                                                            hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                                                                                                            hp_variable_simplification_enum=hp_variable_simplification_enum,
                                                                                                            hp_limit_number_of_clauses_cache=(None, 500),
                                                                                                            hp_limit_number_of_variables_cache=(None, 500),
                                                                                                            decision_heuristic_vsids_d4_version=decision_heuristic_vsids_d4_version,
                                                                                                            decision_heuristic_weight_for_satisfied_clauses=decision_heuristic_weight_for_satisfied_clauses,
                                                                                                            decision_heuristic_ignore_binary_clauses=decision_heuristic_ignore_binary_clauses,
                                                                                                            disable_sat=disable_sat)
                                                                                        circuit = compiler.create_circuit()
                                                                                        number_of_models = circuit.model_counting(set())
                                                                                        real_number_of_models = int(cnf.comments)

                                                                                        if number_of_models == real_number_of_models:
                                                                                            result_temp = "|"
                                                                                        else:
                                                                                            result_temp = "X"

                                                                                        print(result_temp, end="\n" if count % 100 == 0 else ("" if count % 10 != 0 else " "), flush=True)

                                                                                        if count % 1000 == 0:
                                                                                            print()

                                                                                    except c_exception.InvalidConfigurationException:
                                                                                        count -= 1
                                                                                    except (c_exception.CaraException, Exception) as err:
                                                                                        print(f"\nError - {str(err)}", end="\n", flush=True)

                                                                                    if count >= self.__limit:
                                                                                        return
    # endregion
