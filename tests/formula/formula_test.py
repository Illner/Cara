# Import
import formula.cnf as cnf
from ..test_abstract import TestAbstract

# Import exception
import exception.test_exception as t_exception
import exception.formula_exception as f_exception


class FormulaTest(TestAbstract):
    __FOLDER = "formula"

    def __init__(self):
        super().__init__(FormulaTest.__FOLDER, "CNF_formulae")
        self.__original_result_path = self._create_path(FormulaTest.__FOLDER, self._original_result_file_name)
        self._test_name = "Formula test"

    # region Public method
    def test(self) -> (bool, str):
        # Check if the file with the original result exists
        if not self._exists_file(self.__original_result_path):
            raise t_exception.OriginalResultDoesNotExistException(self._test_name, self.__original_result_path)

        actual_result = self.__get_actual_result()
        with open(self.__original_result_path, "r") as original_result_file:
            original_result = original_result_file.read()

        return self._compare_results(actual_result, original_result)

    def save(self):
        original_result = self.__get_actual_result()

        with open(self.__original_result_path, "w") as original_result_file:
            original_result_file.write(original_result)
    # endregion

    # region Private method
    def __get_actual_result(self) -> str:
        actual_result = f"{self._test_name}\n"

        for (file_name, file_path) in self._files:
            try:
                c = cnf.Cnf(file_path)
                clause = c.get_clause(1)
                actual_result = "\n".join((actual_result, file_name, str(c), f"The second clause: {clause}", ""))
            except f_exception.FormulaException as err:
                actual_result = "\n".join((actual_result, file_name, str(err), ""))

        return actual_result
    # endregion
