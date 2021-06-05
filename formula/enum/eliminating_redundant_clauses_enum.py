# Import
from enum import IntEnum, unique


@unique
class EliminatingRedundantClausesEnum(IntEnum):
    NONE = 1
    SUBSUMPTION = 2
    # UP_REDUNDANCY = 3


eliminating_redundant_clauses_enum_names = [erc.name for erc in EliminatingRedundantClausesEnum]
eliminating_redundant_clauses_enum_values = [erc.value for erc in EliminatingRedundantClausesEnum]
