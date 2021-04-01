# Import
from enum import IntEnum, unique


@unique
class NodeTypeEnum(IntEnum):
    AND_NODE = 1            # Inner node
    OR_NODE = 2             # Inner node
    CONSTANT = 3            # Leaf
    LITERAL = 4             # Leaf
    TWO_CNF = 5             # Leaf
    RENAMABLE_HORN_CNF = 6  # Leaf


node_type_enum_names = [nt.name for nt in NodeTypeEnum]
node_type_enum_values = [nt.value for nt in NodeTypeEnum]
