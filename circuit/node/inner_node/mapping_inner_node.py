# Import
from typing import Set, Dict, Union, Tuple
from circuit.node.node_abstract import NodeAbstract
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract

# Import
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class MappingInnerNode(InnerNodeAbstract):
    """
    Mapping inner node
    """

    """
    Private Dict<int, int> mapping_id_variable_id_dictionary
    Private Dict<int, int> variable_id_mapping_id_dictionary
    """

    def __init__(self, child: NodeAbstract, variable_id_mapping_id_dictionary: Dict[int, int],
                 mapping_id_variable_id_dictionary: Dict[int, int], id: int = 0):
        self.__mapping_id_variable_id_dictionary: Dict[int, int] = mapping_id_variable_id_dictionary
        self.__variable_id_mapping_id_dictionary: Dict[int, int] = variable_id_mapping_id_dictionary

        # Check if the mapping is complete
        variable_in_mapping_set = set(mapping_id_variable_id_dictionary.keys())
        variable_in_circuit_set = child._get_variable_in_circuit_set(copy=False)

        if not variable_in_circuit_set.issubset(variable_in_mapping_set):
            raise c_exception.MappingIsIncompleteException(mapping_dictionary=mapping_id_variable_id_dictionary,
                                                           variable_or_literal_in_circuit=variable_in_circuit_set)

        super().__init__(id=id,
                         node_type=nt_enum.NodeTypeEnum.MAPPING_NODE,
                         child_set={child},
                         mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary)

    # region Override method
    def _update_properties(self) -> None:
        pass    # no properties

    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> bool:
        # The circuit is not decomposable
        if not self.decomposable_in_circuit:
            raise c_exception.CircuitIsNotDecomposableException("Satisfiability is not supported if the circuit is not decomposable.")

        restricted_assumption_set_temp = self._create_restricted_assumption_set(assumption_set=assumption_set,
                                                                                variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)
        restricted_exist_quantification_set_temp = self._create_restricted_exist_quantification_set(exist_quantification_set=exist_quantification_set,
                                                                                                    mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary)

        # Cache
        key = ""    # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_assumption_set_temp, restricted_exist_quantification_set_temp)
            value = self._get_satisfiable_cache(key)
            if value is not None:
                return value

        # Mapping is used
        if variable_id_mapping_id_dictionary is not None:
            mapping_dictionary_temp = self.__compute_composed_mapping_dictionary(variable_id_mapping_id_dictionary)
            mapping_id_variable_id_dictionary_temp, variable_id_mapping_id_dictionary_temp = mapping_dictionary_temp
        else:
            mapping_id_variable_id_dictionary_temp = self.__mapping_id_variable_id_dictionary
            variable_id_mapping_id_dictionary_temp = self.__variable_id_mapping_id_dictionary

        child = self.__get_child()
        result = child.is_satisfiable(assumption_set=restricted_assumption_set_temp,
                                      exist_quantification_set=restricted_exist_quantification_set_temp,
                                      use_cache=use_cache,
                                      mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary_temp,
                                      variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary_temp)

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
                                                                                variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)

        # Cache
        key = ""  # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_assumption_set_temp, set())
            value = self._get_model_counting_cache(key)
            if value is not None:
                return value

        # Mapping is used
        if variable_id_mapping_id_dictionary is not None:
            mapping_dictionary_temp = self.__compute_composed_mapping_dictionary(variable_id_mapping_id_dictionary)
            mapping_id_variable_id_dictionary_temp, variable_id_mapping_id_dictionary_temp = mapping_dictionary_temp
        else:
            mapping_id_variable_id_dictionary_temp = self.__mapping_id_variable_id_dictionary
            variable_id_mapping_id_dictionary_temp = self.__variable_id_mapping_id_dictionary

        child = self.__get_child()
        number_of_models = child.model_counting(assumption_set=restricted_assumption_set_temp,
                                                use_cache=use_cache,
                                                mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary_temp,
                                                variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary_temp)

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
                                                                                 variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)
        restricted_default_set_temp = self._create_restricted_exist_quantification_set(exist_quantification_set=default_set,
                                                                                       mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary)

        # Cache
        key = ""    # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_observation_set_temp, restricted_default_set_temp)
            value = self._get_minimal_default_cardinality_cache(key)
            if value is not None:
                return value

        # Mapping is used
        if variable_id_mapping_id_dictionary is not None:
            mapping_dictionary_temp = self.__compute_composed_mapping_dictionary(variable_id_mapping_id_dictionary)
            mapping_id_variable_id_dictionary_temp, variable_id_mapping_id_dictionary_temp = mapping_dictionary_temp
        else:
            mapping_id_variable_id_dictionary_temp = self.__mapping_id_variable_id_dictionary
            variable_id_mapping_id_dictionary_temp = self.__variable_id_mapping_id_dictionary

        child = self.__get_child()
        default_cardinality = child.minimum_default_cardinality(observation_set=restricted_observation_set_temp,
                                                                default_set=restricted_default_set_temp,
                                                                use_cache=use_cache,
                                                                mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary_temp,
                                                                variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary_temp)

        # Cache
        if use_cache:
            self._add_minimal_default_cardinality_cache(key, default_cardinality)

        return default_cardinality

    def str_mapping(self) -> str:
        result = ""
        variable_sorted_list = sorted(self.__variable_id_mapping_id_dictionary.keys())

        for variable_id in variable_sorted_list:
            mapping_id = self.__variable_id_mapping_id_dictionary[variable_id]

            # mapping_id is an implied variable
            if not self.__get_child()._exist_variable_in_circuit_set(mapping_id):
                continue

            result = " ".join((result, str(variable_id), str(mapping_id)))

        return result
    # endregion

    # region Private method
    def __compute_composed_mapping_dictionary(self, variable_id_mapping_id_dictionary: Dict[int, int]) -> Tuple[Dict[int, int], Dict[int, int]]:
        composed_mapping_id_variable_id_dictionary: Dict[int, int] = dict()
        composed_variable_id_mapping_id_dictionary: Dict[int, int] = dict()

        for variable_id in variable_id_mapping_id_dictionary:
            mapping_id = variable_id_mapping_id_dictionary[variable_id]

            if mapping_id in self.__variable_id_mapping_id_dictionary:
                mapping_id = self.__variable_id_mapping_id_dictionary[mapping_id]

                composed_mapping_id_variable_id_dictionary[mapping_id] = variable_id
                composed_variable_id_mapping_id_dictionary[variable_id] = mapping_id

        return composed_mapping_id_variable_id_dictionary, composed_variable_id_mapping_id_dictionary

    def __get_child(self) -> NodeAbstract:
        return list(self._child_set)[0]
    # endregion

    # endregion Magic method
    def __repr__(self):
        string_temp = super().__repr__()

        string_temp = " ".join((string_temp, f"Mapping: {self.__variable_id_mapping_id_dictionary}"))

        return string_temp
    # endregion
