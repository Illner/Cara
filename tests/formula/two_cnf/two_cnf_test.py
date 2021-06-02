# Import
import os
from formula.cnf import Cnf
from formula.pysat_2_cnf import PySat2Cnf
from tests.test_abstract import TestAbstract

# Import exception
import exception.cara_exception as c_exception


class TwoCnfTest(TestAbstract):
    __DIRECTORY: str = os.path.join("formula", "two_cnf")

    def __init__(self):
        super().__init__(TwoCnfTest.__DIRECTORY, test_name="2-CNF test")
        self._set_files(TwoCnfTest.__DIRECTORY, "CNF_formulae")

    # region Static method
    @staticmethod
    def __two_cnf_str(two_cnf: PySat2Cnf) -> str:
        result = f"Number of variables: {two_cnf.number_of_variables}, " \
                 f"number of clauses: {two_cnf.number_of_clauses}, " \
                 f"formula length: {two_cnf.formula_length}"

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
                two_cnf = cnf.get_incidence_graph().convert_to_2_cnf()

                result = "\n".join((result, TwoCnfTest.__two_cnf_str(two_cnf), ""))

                assignment_list = [[], [1], [-2, -3]]
                for assignment in assignment_list:
                    model = two_cnf.get_model(assignment)
                    is_sat = False if model is None else True

                    result = "\n".join((result, f"Assignment: {assignment}", f"Is satisfiable: {str(is_sat)}", ""))

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
        two_cnf = PySat2Cnf()

        clause_list = [[1, 2], [1, 3], [1, 4], [1, -4], [5, 6]]
        for clause in clause_list:
            try:
                result = "\n".join((result, f"Appending the clause: {clause}"))
                two_cnf.append(clause)
                result = "\n".join((result, TwoCnfTest.__two_cnf_str(two_cnf)))

                model = two_cnf.get_model([-1])
                is_sat = False if model is None else True

                result = "\n".join((result, f"Is satisfiable: {str(is_sat)}", ""))
            except (c_exception.CaraException, Exception) as err:
                result = "\n".join((result, str(err), ""))

        return result
    # endregion
