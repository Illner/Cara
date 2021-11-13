# Import
import os
from formula.cnf import Cnf
from tests.test_abstract import TestAbstract
from formula.renamable_horn_formula_lp_formulation import RenamableHornFormulaLpFormulation

# Import exception
import exception.cara_exception as c_exception

# Import enum
import formula.enum.lp_formulation_objective_function_enum as lpfof_enum


class RenamableHornFormulaLpFormulationTest(TestAbstract):
    __DIRECTORY: str = os.path.join("formula", "renamable_horn_formula_lp_formulation")

    def __init__(self):
        super().__init__(RenamableHornFormulaLpFormulationTest.__DIRECTORY, test_name="Renamable Horn formula - LP formulation test")
        self._set_files(RenamableHornFormulaLpFormulationTest.__DIRECTORY, "CNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""
        test_list = [("LP formulation", self.__test_1)]

        for test_name, test in test_list:
            try:
                actual_result = "\n".join((actual_result, test_name, test(), ""))
            except Exception as err:
                actual_result = "\n".join((actual_result, test_name, str(err), ""))

        return actual_result
    # endregion

    # region Private method
    def __test_1(self) -> str:
        """
        A test for LP formulation.
        Positive
        :return: the result of the test
        """

        result = ""

        for (file_name, file_path) in self._files:
            try:
                result = "\n".join((result, file_name))

                cnf = Cnf(file_path)
                incidence_graph = cnf.get_incidence_graph(copy=False)

                for objective_function in lpfof_enum.lp_formulation_objective_function_enum_values:
                    for is_exact in [True, False]:
                        try:
                            result = "\n".join((result, f"Objective function: {lpfof_enum.LpFormulationObjectiveFunctionEnum._value2member_map_[objective_function].name}, "
                                                        f"is exact: {is_exact}"))

                            renamable_horn_formula_lp_formulation = RenamableHornFormulaLpFormulation(incidence_graph=incidence_graph,
                                                                                                      number_of_threads=0,
                                                                                                      is_exact=is_exact,
                                                                                                      objective_function=objective_function)
                            result = "\n".join((result, str(renamable_horn_formula_lp_formulation)))

                            _ = renamable_horn_formula_lp_formulation.solve()

                        except (c_exception.CaraException, Exception) as err:
                            result = "\n".join((result, str(err), ""))

            except (c_exception.CaraException, Exception) as err:
                result = "\n".join((result, str(err), ""))

        return result
    # endregion
