# Import
from typing import Union, List

# Import exception
from exception.cara_exception import CaraException

# Import enum
import compiler.enum.sat_solver_enum as ss_enum


class CompilerException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class SatSolverIsNotSupportedException(CompilerException):
    """
    The SAT solver is not supported
    """

    def __init__(self, solver: Union[ss_enum.SatSolverEnum, ss_enum.PropagateSatSolverEnum]):
        self.message = f"The SAT solver ({solver.name}) is not supported!"
        super().__init__(self.message)


class TryingGetVariableFromEmptyCutSetException(CompilerException):
    """
    Trying to get a variable from the empty cut set
    """

    def __init__(self):
        self.message = "Trying to get a variable from the empty cut set!"
        super().__init__(self.message)


class ClauseIsNotBinaryException(CompilerException):
    """
    The clause is not binary
    """

    def __init__(self, clause: List[int]):
        self.message = f"The clause ({clause}) is not binary!"
        super().__init__(self.message)
