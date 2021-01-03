# Import
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
        pass
    # endregion
