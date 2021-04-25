# Import
from enum import IntEnum, unique


@unique
class DecisionHeuristicEnum(IntEnum):
    RANDOM = 1
    MOST_OCCURRENCES = 2
    JEROSLOW_WANG = 3
    CLAUSE_REDUCTION = 4    # OKsolver
    WEIGHTED_BINARIES = 5   # satz
    DLCS = 6                # Dynamic Largest Combined Sum
    DLIS = 7                # Dynamic Largest Individual Sum
    DLCS_DLIS = 8           # DLCS score with DLIS as a tie-breaker
    EUPC = 9                # Exact Unit Propagation Count


decision_heuristic_enum_names = [dh.name for dh in DecisionHeuristicEnum]
decision_heuristic_enum_values = [dh.value for dh in DecisionHeuristicEnum]
