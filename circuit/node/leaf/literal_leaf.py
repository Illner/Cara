# Import
import math
from typing import Set, Union, Dict, Tuple
from circuit.node.leaf.leaf_abstract import LeafAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class LiteralLeaf(LeafAbstract):
    """
    Circuit literal leaf representation
    """

    """
    Private int literal
    Private int variable
    Private bool is_positive
    """

    def __init__(self, literal: int, id: int = 0):
        self.__literal: int = literal
        self.__variable: int = abs(literal)
        self.__is_positive = True if literal > 0 else False
        super().__init__(id=id,
                         node_type=nt_enum.NodeTypeEnum.LITERAL,
                         variable_in_circuit_set={self.__variable},
                         literal_in_circuit_set={self.__literal})

    # region Override method
    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> bool:
        variable, literal = self.__variable, self.__literal

        # Mapping is used
        if mapping_id_variable_id_dictionary is not None:
            variable = mapping_id_variable_id_dictionary[self.__variable]
            literal = variable if self.__is_positive else -variable

        # The assumption set
        if literal in assumption_set:
            return True
        if -literal in assumption_set:
            return False

        # The exist quantification set
        if variable in exist_quantification_set:
            return True

        return True

    def model_counting(self, assumption_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> int:
        literal = self.__literal

        # Mapping is used
        if mapping_id_variable_id_dictionary is not None:
            variable = mapping_id_variable_id_dictionary[self.__variable]
            literal = variable if self.__is_positive else -variable

        # The assumption set
        if literal in assumption_set:
            return 1
        if -literal in assumption_set:
            return 0

        return 1

    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_cache: bool = True,
                                    mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                                    variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> float:
        variable, literal = self.__variable, self.__literal

        # Mapping is used
        if mapping_id_variable_id_dictionary is not None:
            variable = mapping_id_variable_id_dictionary[self.__variable]
            literal = variable if self.__is_positive else -variable

        # The default set
        if variable in default_set:
            if self.__is_positive:
                return 0

            # Negative literal
            return 1

        # The observation set
        if literal in observation_set:
            return 0    # True

        if -literal in observation_set:
            return math.inf  # False

        return 0

    def copy_circuit(self, mapping_dictionary: Dict[int, int], circuit,
                     copied_node_dictionary: Union[Dict[int, int], None] = None, size: int = 0) -> Tuple[int, int]:
        # The variable is not included in the mapping function
        if self.__variable not in mapping_dictionary:
            raise c_exception.MappingIsIncompleteException(mapping_dictionary=mapping_dictionary,
                                                           variable_or_literal_in_circuit={self.__literal})

        mapped_variable = mapping_dictionary[self.__variable]
        new_node_id = circuit.create_literal_leaf(literal=mapped_variable if self.__is_positive else -mapped_variable,
                                                  use_unique_node_cache=True)

        return new_node_id, size
    # endregion

    # endregion Magic method
    def __repr__(self):
        string_temp = super().__repr__()

        string_temp = " ".join((string_temp, f"Literal: {self.__literal}"))

        return string_temp
    # endregion

    # region Property
    @property
    def literal(self) -> int:
        return self.__literal

    @property
    def variable(self) -> int:
        return self.__variable

    @property
    def is_positive(self) -> bool:
        return self.__is_positive
    # endregion
