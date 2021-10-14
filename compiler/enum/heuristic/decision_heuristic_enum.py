# Import
from enum import IntEnum, unique


@unique
class DecisionHeuristicEnum(IntEnum):
    RANDOM = 1
    JEROSLOW_WANG_ONE_SIDED = 2
    JEROSLOW_WANG_TWO_SIDED = 3
    CLAUSE_REDUCTION = 4            # OKsolver
    WEIGHTED_BINARIES = 5           # satz
    BACKBONE_SEARCH = 6
    DLCS = 7                        # Dynamic Largest Combined Sum
    DLIS = 8                        # Dynamic Largest Individual Sum
    DLCS_DLIS = 9                   # DLCS score with DLIS as a tie-breaker
    EUPC = 10                       # Exact Unit Propagation Count
    VSIDS = 11
    VSADS = 12
    RENAMABLE_HORN = 13


decision_heuristic_enum_names = [dh.name for dh in DecisionHeuristicEnum]
decision_heuristic_enum_values = [dh.value for dh in DecisionHeuristicEnum]
