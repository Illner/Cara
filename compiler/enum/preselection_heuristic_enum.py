# Import
from enum import IntEnum, unique


@unique
class PreselectionHeuristicEnum(IntEnum):
    NONE = 1
    PROP_Z = 2      # satz, kcnfs
    CRA = 3         # AUPC (Approximate Unit Propagation Count) - march


preselection_heuristic_enum_names = [ph.name for ph in PreselectionHeuristicEnum]
preselection_heuristic_enum_values = [ph.value for ph in PreselectionHeuristicEnum]
