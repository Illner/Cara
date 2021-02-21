# Import enum
import compiler.sat_solver_enum as ss_enum


class CompilerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SatSolverIsNotSupportedException(CompilerException):
    """
    The SAT solver is not supported
    """

    def __init__(self, solver: ss_enum.SatSolverEnum):
        self.message = f"The SAT solver ({solver.name}) is not supported!"
        super().__init__(self.message)
