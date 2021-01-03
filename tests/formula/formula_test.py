# Import
import formula.cnf as cnf
from tests.test_abstract import TestAbstract

# Import exception
import exception.formula_exception as f_exception


class FormulaTest(TestAbstract):
    __FOLDER: str = "formula"

    def __init__(self):
        super().__init__(FormulaTest.__FOLDER, FormulaTest._ORIGINAL_RESULT_FILE_NAME, test_name="Formula test")
        self._set_files(FormulaTest.__FOLDER, "CNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        for (file_name, file_path) in self._files:
            try:
                c = cnf.Cnf(file_path)
                clause = c.get_clause(1)
                actual_result = "\n".join((actual_result, file_name, str(c), f"The second clause: {clause}", ""))
            except f_exception.FormulaException as err:
                actual_result = "\n".join((actual_result, file_name, str(err), ""))

        return actual_result
    # endregion
