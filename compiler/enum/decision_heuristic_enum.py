# Import
from enum import IntEnum, unique


@unique
class DecisionHeuristicEnum(IntEnum):
    RANDOM = 1
    MOST_OCCURRENCES = 2
    JEROSLOW_WANG_ONE_SIDED = 3
    JEROSLOW_WANG_TWO_SIDED = 4
    CLAUSE_REDUCTION = 5            # OKsolver
    WEIGHTED_BINARIES = 6           # satz
    DLCS = 7                        # Dynamic Largest Combined Sum
    DLIS = 8                        # Dynamic Largest Individual Sum
    DLCS_DLIS = 9                   # DLCS score with DLIS as a tie-breaker
    EUPC = 10                       # Exact Unit Propagation Count


decision_heuristic_enum_names = [dh.name for dh in DecisionHeuristicEnum]
decision_heuristic_enum_values = [dh.value for dh in DecisionHeuristicEnum]
