# Import
import math
from typing import Set, Union, Dict
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
        super().__init__(id=id,
                         node_type=nt_enum.NodeTypeEnum.CONSTANT,
                         variable_in_circuit_set=set(),
                         literal_in_circuit_set=set())

    # region Override method
    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> bool:
        if self.__constant:
            return True
        else:
            return False

    def model_counting(self, assumption_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> int:
        if self.__constant:
            return 1
        else:
            return 0

    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_cache: bool = True,
                                    mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                                    variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> float:
        if self.__constant:
            return 0
        else:
            return math.inf
    # endregion

    # region Magic method
    def __repr__(self):
        string_temp = super().__repr__()

        string_temp = " ".join((string_temp, f"Constant: {self.__constant}"))

        return string_temp
    # endregion

    # region Property
    @property
    def constant(self) -> bool:
        return self.__constant
    # endregion
