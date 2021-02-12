# Import
import math
from typing import Set
from circuit.node.leaf.leaf_abstract import LeafAbstract

# Import enum
import circuit.node.node_type_enum as nt_enum


class ConstantLeaf(LeafAbstract):
    """
    Circuit constant (True, False) leaf representation
    """

    """
    Private bool constant
    """

    def __init__(self, constant: bool, id: int = 0):
        self.__constant: bool = constant
        super().__init__(id, nt_enum.NodeTypeEnum.CONSTANT, set(), set())

    # region Override method
    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_caches: bool = True) -> bool:
        if self.constant:
            return True
        else:
            return False

    def model_counting(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_caches: bool = True) -> int:
        if self.constant:
            return 1
        else:
            return 0

    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_caches: bool = True) -> float:
        if self.constant:
            return 0
        else:
            return math.inf
    # endregion

    # region Magic method
    def __repr__(self):
        string_temp = super().__repr__()

        string_temp = " ".join((string_temp, f"Constant: {self.constant}"))

        return string_temp
    # endregion

    # region Property
    @property
    def constant(self):
        return self.__constant
    # endregion
