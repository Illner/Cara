# Import enum
import compiler.enum.sat_solver_enum as ss_enum
from exception.cara_exception import CaraException


class CompilerException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class SatSolverIsNotSupportedException(CompilerException):
    """
    The SAT solver is not supported
    """

    def __init__(self, solver: ss_enum.SatSolverEnum):
        self.message = f"The SAT solver ({solver.name}) is not supported!"
        super().__init__(self.message)


class LiteralAlreadyExistsInAssignmentException(CompilerException):
    """
    The literal already exists in the assignment
    """

    def __init__(self, literal: int):
        self.message = f"The literal ({literal}) already exists in the assignment!"
        super().__init__(self.message)


class LiteralDoesNotExistInAssignmentException(CompilerException):
    """
    The literal does not exist in the assignment
    """

    def __init__(self, literal: int):
        self.message = f"The literal ({literal}) does not exist in the assignment!"
        super().__init__(self.message)


class OppositeLiteralAlreadyExistsInAssignmentException(CompilerException):
    """
    The opposite literal already exists in the assignment
    """

    def __init__(self, literal: int):
        self.message = f"The literal ({literal}) can't be added to the assignment because the opposite literal already is in the assignment!"
        super().__init__(self.message)


class InconsistentAssignmentException(CompilerException):
    """
    An inconsistent assignment has been detected
    """

    def __init__(self, message_extension: str = ""):
        self.message = "An inconsistent assignment has been detected!"
        if message_extension:
            self.message += f" ({message_extension})"
        super().__init__(self.message)


class TryingGetVariableFromEmptyCutSetException(CompilerException):
    """
    Trying to get a variable from the empty cut set
    """

    def __init__(self):
        self.message = "Trying to get a variable from the empty cut set!"
        super().__init__(self.message)
