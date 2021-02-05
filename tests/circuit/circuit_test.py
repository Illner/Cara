# Import
from circuit.circuit import Circuit
from tests.test_abstract import TestAbstract

# Import exception
import exception.circuit_exception as c_exception


class CircuitTest(TestAbstract):
    __FOLDER: str = "circuit"
    __ORIGINAL_RESULT_FILE_NAME: str = "original_result_circuit.txt"

    def __init__(self):
        super().__init__(CircuitTest.__FOLDER, CircuitTest.__ORIGINAL_RESULT_FILE_NAME, test_name="Circuit test")
        self._set_files(CircuitTest.__FOLDER, "NNF_formulae")

    # region Override method
    def _get_actual_result(self) -> str:
        actual_result = ""

        actual_result = "\n".join((actual_result, "Parsing", self.__test_1(), ""))  # Test 1

        return actual_result
    # endregion

    # region Private method
    def __test_1(self) -> str:
        """
        A test for parsing.
        Positive / negative
        """

        result = ""

        for (file_name, file_path) in self._files:
            try:
                c = Circuit(file_path)
                result = "\n".join((result, file_name, str(c), ""))
            except c_exception.CircuitException as err:
                result = "\n".join((result, file_name, str(err), ""))

        return result
    # endregion
