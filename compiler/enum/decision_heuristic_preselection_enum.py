# Import
from enum import IntEnum, unique


@unique
class DecisionHeuristicPreselectionEnum(IntEnum):
    NONE = 1
    PROP_Z = 2      # satz, kcnfs
    CRA = 3         # march


decision_heuristic_preselection_enum_names = [dhp.name for dhp in DecisionHeuristicPreselectionEnum]
decision_heuristic_preselection_enum_values = [dhp.value for dhp in DecisionHeuristicPreselectionEnum]
