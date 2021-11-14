# Import
from pulp import LpStatus

# Import exception
from exception.cara_exception import CaraException


class RenamableHornFormulaLpFormulationException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class SolutionDoesNotExistException(RenamableHornFormulaLpFormulationException):
    """
    A solution to the LP problem does not exist
    """

    def __init__(self, status: LpStatus):
        self.message = f"A solution to the LP problem does not exist ({status})!"
        super().__init__(self.message)


class CutSetIsNotDefinedException(RenamableHornFormulaLpFormulationException):
    """
    A cut set is not defined
    """

    def __init__(self):
        self.message = "A cut set is necessary for this objective function (RESPECT_DECOMPOSITION_HORN_FORMULA)!"
        super().__init__(self.message)