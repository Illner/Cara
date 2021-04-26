# Import
from enum import IntEnum, unique


@unique
class LiteralCountHeuristicFunctionEnum(IntEnum):
    SUM = 1     # DLCS
    MAX = 2     # DLIS
    MIN = 3
    AVG = 4


literal_count_heuristic_function_enum_names = [lchf.name for lchf in LiteralCountHeuristicFunctionEnum]
literal_count_heuristic_function_enum_values = [lchf.value for lchf in LiteralCountHeuristicFunctionEnum]
