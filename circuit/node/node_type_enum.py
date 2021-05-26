# Import
from enum import IntEnum, unique


@unique
class NodeTypeEnum(IntEnum):
    AND_NODE = 1            # Inner node
    OR_NODE = 2             # Inner node
    MAPPING_NODE = 3        # Inner node
    CONSTANT = 4            # Leaf
    LITERAL = 5             # Leaf
    TWO_CNF = 6             # Leaf
    RENAMABLE_HORN_CNF = 7  # Leaf


node_type_enum_names = [nt.name for nt in NodeTypeEnum]
node_type_enum_values = [nt.value for nt in NodeTypeEnum]
