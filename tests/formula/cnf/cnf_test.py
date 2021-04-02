# Import
import os
from formula.cnf import Cnf
from other.sorted_list import SortedList
from tests.test_abstract import TestAbstract

# Import exception
import exception.cara_exception as c_exception


class CnfTest(TestAbstract):
    __DIRECTORY: str = os.path.join("formula", "cnf")

    def __init__(self):
        super().__init__(CnfTest.__DIRECTORY, test_name="CNF test")
        self._set_files(CnfTest.__DIRECTORY, "CNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        for (file_name, file_path) in self._files:
            try:
                c = Cnf(file_path)
                clause = c.get_clause(1, copy=False)
                actual_result = "\n".join((actual_result, file_name, str(c), f"The second clause: ({SortedList(clause)})", ""))
            except (c_exception.CaraException, Exception) as err:
                actual_result = "\n".join((actual_result, file_name, str(err), ""))

        return actual_result
    # endregion
