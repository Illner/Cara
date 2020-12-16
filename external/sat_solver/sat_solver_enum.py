# Import
from enum import IntEnum, unique


@unique
class SatSolverEnum(IntEnum):
    MiniSAT = 1
    Glucose = 2
    Lingeling = 3
    CaDiCal = 4


sat_solver_enum_names = [ss.name for ss in SatSolverEnum]
sat_solver_enum_values = [ss.value for ss in SatSolverEnum]
