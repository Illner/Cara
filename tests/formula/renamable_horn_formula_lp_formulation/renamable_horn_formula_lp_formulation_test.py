# Import
import os
from formula.cnf import Cnf
from tests.test_abstract import TestAbstract
from formula.renamable_horn_formula_lp_formulation import RenamableHornFormulaLpFormulation

# Import exception
import exception.cara_exception as c_exception

# Import enum
import formula.enum.lp_formulation_type_enum as lpft_enum


class RenamableHornFormulaLpFormulationTest(TestAbstract):
    __DIRECTORY: str = os.path.join("formula", "renamable_horn_formula_lp_formulation")

    def __init__(self):
        super().__init__(RenamableHornFormulaLpFormulationTest.__DIRECTORY, test_name="Renamable Horn formula - LP formulation test")
        self._set_files(RenamableHornFormulaLpFormulationTest.__DIRECTORY, "CNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""
        test_list = [("LP formulation", self.__test_1),
                     ("Weighted LP formulation", self.__test_2)]

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

                for lp_formulation_type in [lpft_enum.LpFormulationTypeEnum.HORN_FORMULA,
                                            lpft_enum.LpFormulationTypeEnum.LENGTH_WEIGHTED_HORN_FORMULA,
                                            lpft_enum.LpFormulationTypeEnum.SQUARED_LENGTH_WEIGHTED_HORN_FORMULA,
                                            lpft_enum.LpFormulationTypeEnum.INVERSE_LENGTH_WEIGHTED_HORN_FORMULA,
                                            lpft_enum.LpFormulationTypeEnum.SQUARED_INVERSE_LENGTH_WEIGHTED_HORN_FORMULA,
                                            lpft_enum.LpFormulationTypeEnum.NUMBER_OF_EDGES,
                                            lpft_enum.LpFormulationTypeEnum.NUMBER_OF_VERTICES,
                                            lpft_enum.LpFormulationTypeEnum.VERTEX_COVER]:
                    for is_exact in [True, False]:
                        try:
                            result = "\n".join((result, f"LP formulation type: {lpft_enum.LpFormulationTypeEnum._value2member_map_[lp_formulation_type].name}, "
                                                        f"is exact: {is_exact}"))

                            renamable_horn_formula_lp_formulation = RenamableHornFormulaLpFormulation(incidence_graph=incidence_graph,
                                                                                                      number_of_threads=0,
                                                                                                      is_exact=is_exact,
                                                                                                      lp_formulation_type=lp_formulation_type)
                            result = "\n".join((result, str(renamable_horn_formula_lp_formulation)))

                            _ = renamable_horn_formula_lp_formulation.solve()

                        except (c_exception.CaraException, Exception) as err:
                            result = "\n".join((result, str(err), ""))

            except (c_exception.CaraException, Exception) as err:
                result = "\n".join((result, str(err), ""))

        return result

    def __test_2(self) -> str:
        """
        A test for weighted LP formulation.
        Positive
        :return: the result of the test
        """

        result = ""

        for (file_name, file_path) in self._files:
            try:
                result = "\n".join((result, file_name))

                cnf = Cnf(file_path)
                incidence_graph = cnf.get_incidence_graph(copy=False)

                for lp_formulation_type in [lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_HORN_FORMULA,
                                            lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_NUMBER_OF_EDGES,
                                            lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_NUMBER_OF_VERTICES,
                                            lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_VERTEX_COVER]:
                    for cut_set in [set(), {2}, {1, 2}]:
                        try:
                            result = "\n".join((result, f"LP formulation type: {lpft_enum.LpFormulationTypeEnum._value2member_map_[lp_formulation_type].name}, "
                                                        f"cut set: {sorted(cut_set)}"))

                            renamable_horn_formula_lp_formulation = RenamableHornFormulaLpFormulation(incidence_graph=incidence_graph,
                                                                                                      number_of_threads=0,
                                                                                                      is_exact=False,
                                                                                                      lp_formulation_type=lp_formulation_type,
                                                                                                      cut_set=cut_set,
                                                                                                      weight_for_variables_not_in_cut_set=2)
                            result = "\n".join((result, str(renamable_horn_formula_lp_formulation)))

                            _ = renamable_horn_formula_lp_formulation.solve()

                        except (c_exception.CaraException, Exception) as err:
                            result = "\n".join((result, str(err), ""))

            except (c_exception.CaraException, Exception) as err:
                result = "\n".join((result, str(err), ""))

        return result
    # endregion
