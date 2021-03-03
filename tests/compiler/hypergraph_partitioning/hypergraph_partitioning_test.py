# Import
import os
from formula.cnf import Cnf
from compiler.solver import Solver
from other.sorted_list import SortedList
from tests.test_abstract import TestAbstract
from compiler.hypergraph_partitioning import HypergraphPartitioning

# Import exception
import exception.formula.formula_exception as f_exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


class HypergraphPartitioningTest(TestAbstract):
    __FOLDER: str = os.path.join("compiler", "hypergraph_partitioning")

    def __init__(self):
        super().__init__(HypergraphPartitioningTest.__FOLDER, test_name="Hypergraph partitioning test")
        self._set_files(HypergraphPartitioningTest.__FOLDER, "CNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        for (file_name, file_path) in self._files:
            try:
                cnf = Cnf(file_path)
                solver = Solver(cnf, None, ss_enum.SatSolverEnum.MiniSAT)

                for cache_enum in hpc_enum.hpc_enum_values:
                    for variable_simplification_enum in hpvs_enum.hpvs_enum_values:
                        try:
                            actual_result = "\n".join((actual_result,
                                                       f"File: {file_name}, "
                                                       f"cache: {hpc_enum.HypergraphPartitioningCacheEnum(cache_enum).name}, "
                                                       f"variable simplification: {hpvs_enum.HypergraphPartitioningVariableSimplificationEnum(variable_simplification_enum).name}"))

                            hypergraph_partitioning = HypergraphPartitioning(cnf,
                                                                             cache_enum=cache_enum,
                                                                             variable_simplification_enum=variable_simplification_enum,
                                                                             ub_factor=0.10,
                                                                             software_enum=hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS,
                                                                             node_weight_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                                                                             hyperedge_weight_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                                                                             limit_number_of_clauses_cache=(None, None),
                                                                             limit_number_of_variables_cache=(None, None))

                            number_of_repetition = 1 if cache_enum == hpc_enum.HypergraphPartitioningCacheEnum.NONE else 2
                            for _ in range(number_of_repetition):
                                cut_set = hypergraph_partitioning.get_cut_set(cnf.get_incidence_graph(), solver, [])
                                cut_set = SortedList(cut_set)

                                # Deterministic
                                if len(cut_set) > 5:
                                    cut_set = "> 5"

                                actual_result = "\n".join((actual_result, f"Cut set: {cut_set}"))
                        except c_exception.CompilerException as err:
                            actual_result = "\n".join((actual_result, str(err), ""))
            except (f_exception.FormulaException, c_exception.CompilerException) as err:
                actual_result = "\n".join((actual_result, file_name, str(err), ""))

        return actual_result
    # endregion
