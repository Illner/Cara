# Import
from enum import IntEnum, unique


@unique
class DecisionHeuristicEnum(IntEnum):
    RANDOM = 1
    MOST_OCCURRENCES = 2
    JEROSLOW_WANG = 3
    CLAUSE_REDUCTION = 4    # OKsolver
    WEIGHTED_BINARIES = 5   # satz


decision_heuristic_enum_names = [dh.name for dh in DecisionHeuristicEnum]
decision_heuristic_enum_values = [dh.value for dh in DecisionHeuristicEnum]
