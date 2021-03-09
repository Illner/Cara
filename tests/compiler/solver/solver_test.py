# Import
import os
from formula.cnf import Cnf
from compiler.solver import Solver
from other.sorted_list import SortedList
from tests.test_abstract import TestAbstract

# Import exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum


class SolverTest(TestAbstract):
    __FOLDER: str = os.path.join("compiler", "solver")

    def __init__(self):
        super().__init__(SolverTest.__FOLDER, test_name="Solver test")
        self._set_files(SolverTest.__FOLDER, "CNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        for (file_name, file_path) in self._files:
            for sat_solver in ss_enum.sat_solver_enum_values:
                assumption_list = [[], [1]]
                for assumption in assumption_list:
                    try:
                        actual_result = "\n".join((actual_result, f"File: {file_name}, SAT solver: {ss_enum.SatSolverEnum(sat_solver).name}, assumption: {assumption}"))

                        cnf = Cnf(file_path)
                        solver = Solver(cnf=cnf,
                                        clause_id_set=None,
                                        sat_solver_enum=sat_solver)

                        # Unit propagation
                        unit_propagation = solver.unit_propagation(assumption)
                        if unit_propagation is not None:
                            unit_propagation = SortedList(unit_propagation)

                        # Implicit unit propagation
                        implicit_unit_propagation = solver.iterative_implicit_unit_propagation(assumption)
                        if implicit_unit_propagation is not None:
                            implicit_unit_propagation = SortedList(implicit_unit_propagation)

                        # Satisfiability
                        is_sat = solver.is_satisfiable(assumption)

                        actual_result = "\n".join((actual_result,
                                                   f"Is satisfiable: {is_sat}",
                                                   f"Unit propagation: {unit_propagation}",
                                                   f"Implicit unit propagation: {implicit_unit_propagation}",
                                                   ""))
                    except c_exception.CompilerException as err:
                        actual_result = "\n".join((actual_result, file_name, str(err), ""))

        return actual_result
    # endregion
