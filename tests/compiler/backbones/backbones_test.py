# Import
import os
from formula.cnf import Cnf
from compiler.solver import Solver
from tests.test_abstract import TestAbstract

# Import exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.backbones_enum as b_enum
import compiler.enum.sat_solver_enum as ss_enum


class BackbonesTest(TestAbstract):
    __FOLDER: str = os.path.join("compiler", "backbones")

    def __init__(self):
        super().__init__(BackbonesTest.__FOLDER, test_name="Backbones test")
        self._set_files(BackbonesTest.__FOLDER, "CNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        for (file_name, file_path) in self._files:
            for sat_solver_enum in ss_enum.sat_solver_enum_values:
                for backbones_enum in b_enum.backbones_enum_values:
                    try:
                        actual_result = "\n".join((actual_result,
                                                   f"File: {file_name}, "
                                                   f"SAT solver: {ss_enum.SatSolverEnum(sat_solver_enum).name}, "
                                                   f"backbones: {b_enum.BackbonesEnum(backbones_enum).name}"))

                        cnf = Cnf(file_path)
                        solver = Solver(cnf=cnf,
                                        clause_id_set=None,
                                        backbones_chunk_size=0.5,
                                        sat_solver_enum=sat_solver_enum,
                                        backbones_enum=backbones_enum)

                        number_of_backbone_literals = solver.get_backbones([])
                        real_number_of_backbone_literals = int(cnf.comments)

                        number_of_backbone_literals = 0 if number_of_backbone_literals is None else len(number_of_backbone_literals)

                        if number_of_backbone_literals == real_number_of_backbone_literals:
                            actual_result = "\n".join((actual_result, f"Correct", ""))
                        else:
                            actual_result = "\n".join((actual_result, f"Incorrect: {number_of_backbone_literals} vs {real_number_of_backbone_literals}", ""))
                    except c_exception.CompilerException as err:
                        actual_result = "\n".join((actual_result, str(err), ""))

        return actual_result
    # endregion
