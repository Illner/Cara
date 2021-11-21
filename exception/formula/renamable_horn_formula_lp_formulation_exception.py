# Import
from pulp import LpStatus

# Import exception
from exception.cara_exception import CaraException

# Import enum
import formula.enum.lp_formulation_type_enum as lpft_enum


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

    def __init__(self, lp_formulation_type: lpft_enum.LpFormulationTypeEnum):
        self.message = f"A cut set is necessary for this LP formulation type ({lp_formulation_type.name})!"
        super().__init__(self.message)
