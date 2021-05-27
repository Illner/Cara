# Import
from typing import Set, Union, Dict
from circuit.node.node_abstract import NodeAbstract
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class AndInnerNode(InnerNodeAbstract):
    """
    Circuit AND inner node representation
    """

    def __init__(self, child_set: Set[NodeAbstract], id: int = 0):
        decomposable_temp = self.__is_decomposable_set(child_set)

        super().__init__(id=id,
                         node_type=nt_enum.NodeTypeEnum.AND_NODE,
                         child_set=child_set,
                         decomposable=decomposable_temp)

    # region Private method
    @staticmethod
    def __is_decomposable_set(child_set: Set[NodeAbstract]) -> bool:
        """
        Check if the node is decomposable
        :param child_set: children set
        :return: True if the node is decomposable. Otherwise, False is returned.
        """

        # The node has no children or only one child
        if not len(child_set) or len(child_set) == 1:
            return True

        child_list = list(child_set)

        for i in range(0, len(child_list) - 1):
            for j in range(i+1, len(child_list)):
                intersection_temp = child_list[i]._get_variable_in_circuit_set(copy=False).intersection(child_list[j]._get_variable_in_circuit_set(copy=False))

                if len(intersection_temp):
                    return False

        return True
    # endregion

    # region Protected method
    def _is_decomposable(self) -> bool:
        """
        Check if the node is decomposable
        :return: True if the node is decomposable. Otherwise, False is returned.
        """

        return self.__is_decomposable_set(self._child_set)
    # endregion

    # region Override method
    def _update_properties(self) -> None:
        self._set_decomposable(self._is_decomposable())

    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> bool:
        # The circuit is not decomposable
        if not self.decomposable_in_circuit:
            raise c_exception.CircuitIsNotDecomposableException("Satisfiability is not supported if the circuit is not decomposable.")

        restricted_assumption_set_temp = self._create_restricted_assumption_set(assumption_set=assumption_set,
                                                                                mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary)
        restricted_exist_quantification_set_temp = self._create_restricted_exist_quantification_set(exist_quantification_set=exist_quantification_set,
                                                                                                    variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)

        # Cache
        key = ""    # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_assumption_set_temp, restricted_exist_quantification_set_temp)
            value = self._get_satisfiable_cache(key)
            if value is not None:
                return value

        result = True
        for child in self._child_set:
            result_temp = child.is_satisfiable(assumption_set=restricted_assumption_set_temp,
                                               exist_quantification_set=restricted_exist_quantification_set_temp,
                                               use_cache=use_cache,
                                               mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary,
                                               variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)
            # The child is not satisfied => this node is not satisfied
            if not result_temp:
                result = False
                break

        # Cache
        if use_cache:
            self._add_satisfiable_cache(key, result)

        return result

    def model_counting(self, assumption_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> int:
        # The circuit is not decomposable
        if not self.decomposable_in_circuit:
            raise c_exception.CircuitIsNotDecomposableException("Model counting is not supported if the circuit is not decomposable.")

        # The circuit is not deterministic
        if not self.deterministic_in_circuit:
            raise c_exception.CircuitIsNotDeterministicException("Model counting is not supported if the circuit is not deterministic.")

        # The circuit is not smooth
        if not self.smoothness_in_circuit:
            raise c_exception.CircuitIsNotSmoothException("Model counting is not supported if the circuit is not smooth.")

        restricted_assumption_set_temp = self._create_restricted_assumption_set(assumption_set=assumption_set,
                                                                                mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary)

        # Cache
        key = ""    # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_assumption_set_temp, set())
            value = self._get_model_counting_cache(key)
            if value is not None:
                return value

        number_of_models = 1
        for child in self._child_set:
            number_of_models *= child.model_counting(assumption_set=restricted_assumption_set_temp,
                                                     use_cache=use_cache,
                                                     mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary,
                                                     variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)

        # Cache
        if use_cache:
            self._add_model_counting_cache(key, number_of_models)

        return number_of_models

    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_cache: bool = True,
                                    mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                                    variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> float:
        # The circuit is not decomposable
        if not self.decomposable_in_circuit:
            raise c_exception.CircuitIsNotDecomposableException("Minimum default-cardinality is not supported if the circuit is not decomposable.")

        restricted_observation_set_temp = self._create_restricted_assumption_set(assumption_set=observation_set,
                                                                                 mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary)
        restricted_default_set_temp = self._create_restricted_exist_quantification_set(exist_quantification_set=default_set,
                                                                                       variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)

        # Cache
        key = ""    # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_observation_set_temp, restricted_default_set_temp)
            value = self._get_minimal_default_cardinality_cache(key)
            if value is not None:
                return value

        default_cardinality = 0
        for child in self._child_set:
            default_cardinality += child.minimum_default_cardinality(observation_set=restricted_observation_set_temp,
                                                                     default_set=restricted_default_set_temp,
                                                                     use_cache=use_cache,
                                                                     mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary,
                                                                     variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)

        # Cache
        if use_cache:
            self._add_minimal_default_cardinality_cache(key, default_cardinality)

        return default_cardinality
    # endregion
