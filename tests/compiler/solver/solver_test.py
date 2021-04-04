# Import
import os
from formula.cnf import Cnf
from compiler.solver import Solver
from other.sorted_list import SortedList
from tests.test_abstract import TestAbstract

# Import exception
import exception.cara_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum


class SolverTest(TestAbstract):
    __DIRECTORY: str = os.path.join("compiler", "solver")

    def __init__(self):
        super().__init__(SolverTest.__DIRECTORY, test_name="Solver test")
        self._set_files(SolverTest.__DIRECTORY, "CNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        for (file_name, file_path) in self._files:
            for sat_solver in ss_enum.sat_solver_enum_values:
                assumption_list = [[], [1]]
                for assumption in assumption_list:
                    try:
                        actual_result = "\n".join((actual_result, f"File: {file_name}, SAT solver: {ss_enum.SatSolverEnum._value2member_map_[sat_solver].name}, assumption: {assumption}"))

                        cnf = Cnf(file_path)
                        solver = Solver(cnf=cnf,
                                        clause_id_set=None,
                                        sat_solver_enum=sat_solver,
                                        first_implied_literals_enum=il_enum.FirstImpliedLiteralsEnum.IMPLICIT_BCP)

                        # Unit propagation
                        unit_propagation = solver.unit_propagation(assumption)
                        if unit_propagation is not None:
                            unit_propagation = SortedList(unit_propagation)

                        # Implicit unit propagation
                        implicit_unit_propagation = solver.iterative_implicit_unit_propagation(assumption, only_one_iteration=False)
                        if implicit_unit_propagation is not None:
                            implicit_unit_propagation = SortedList(implicit_unit_propagation)

                        # Satisfiability
                        is_sat = solver.is_satisfiable(assumption)

                        actual_result = "\n".join((actual_result,
                                                   f"Is satisfiable: {is_sat}",
                                                   f"Unit propagation: {unit_propagation}",
                                                   f"Implicit unit propagation: {implicit_unit_propagation}",
                                                   ""))
                    except (c_exception.CaraException, Exception) as err:
                        actual_result = "\n".join((actual_result, file_name, str(err), ""))

        return actual_result
    # endregion
