# Import
import os
from formula.cnf import Cnf
from other.sorted_list import SortedList
from tests.test_abstract import TestAbstract
from formula.pysat_horn_cnf import PySatHornCnf

# Import exception
import exception.cara_exception as c_exception


class HornCnfTest(TestAbstract):
    __DIRECTORY: str = os.path.join("formula", "horn_cnf")

    def __init__(self):
        super().__init__(HornCnfTest.__DIRECTORY, test_name="Horn CNF test")
        self._set_files(HornCnfTest.__DIRECTORY, "CNF_formulae")

    # region Static method
    @staticmethod
    def __horn_cnf_str(horn_cnf: PySatHornCnf) -> str:
        result = f"Number of variables: {horn_cnf.number_of_variables}, " \
                 f"number of clauses: {horn_cnf.number_of_clauses}, " \
                 f"formula length: {horn_cnf.formula_length}"

        return result
    # endregion

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""
        test_list = [("Satisfiability", self.__test_1),
                     ("Append", self.__test_2)]

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
        A test for satisfiability.
        Positive
        :return: the result of the test
        """

        result = ""

        for (file_name, file_path) in self._files:
            try:
                result = "\n".join((result, file_name))

                cnf = Cnf(file_path)
                cnf.get_incidence_graph().initialize_renamable_horn_formula_recognition()

                renaming_function = cnf.get_incidence_graph().is_renamable_horn_formula()
                if renaming_function is not None:
                    renaming_function = True if len(renaming_function) > 0 else False
                result = "\n".join((result, f"Renaming function: {renaming_function}"))

                horn_cnf = cnf.get_incidence_graph().convert_to_horn_cnf()
                result = "\n".join((result, self.__horn_cnf_str(horn_cnf), ""))

                assignment_list = [[], [1], [-2, -3]]
                for assignment in assignment_list:
                    model = horn_cnf.get_model(assignment)
                    result = "\n".join((result, f"Assignment: {assignment}", f"Model: {SortedList(model) if model is not None else 'UNSAT'}", ""))

            except (c_exception.CaraException, Exception) as err:
                result = "\n".join((result, str(err), ""))

        return result

    def __test_2(self) -> str:
        """
        A test for appending.
        Positive
        :return: the result of the test
        """

        result = ""
        horn_cnf = PySatHornCnf()

        clause_list = [[1, -6], [-1, 2], [-2, 3, -6], [-2, -3], [-4, 5]]
        for clause in clause_list:
            try:
                result = "\n".join((result, f"Appending the clause: {clause}"))
                horn_cnf.append(clause)
                result = "\n".join((result, self.__horn_cnf_str(horn_cnf)))

                model = horn_cnf.get_model([6])
                is_sat = False if model is None else True

                result = "\n".join((result, f"Is satisfiable: {str(is_sat)}", ""))
            except (c_exception.CaraException, Exception) as err:
                result = "\n".join((result, str(err), ""))

        return result
    # endregion
