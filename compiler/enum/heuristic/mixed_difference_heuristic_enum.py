# Import
from enum import IntEnum, unique


@unique
class MixedDifferenceHeuristicEnum(IntEnum):
    OK_SOLVER = 1
    POSIT_SATZ = 2


mixed_difference_heuristic_enum_names = [mdh.name for mdh in MixedDifferenceHeuristicEnum]
mixed_difference_heuristic_enum_values = [mdh.value for mdh in MixedDifferenceHeuristicEnum]
