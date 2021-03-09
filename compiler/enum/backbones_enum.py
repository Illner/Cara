# Import
from enum import IntEnum, unique


@unique
class BackbonesEnum(IntEnum):
    ITERATIVE_ALGORITHM = 3                 # Algorithm 3: Iterative algorithm (one test per variable)
    CHUNKING_ALGORITHM = 5                  # Algorithm 5: Chunking algorithm
    CORE_BASED_ALGORITHM_WITH_CHUNKING = 7  # Algorithm 7: Core-based Algorithm with Chunking


backbones_enum_names = [b.name for b in BackbonesEnum]
backbones_enum_values = [b.value for b in BackbonesEnum]
