# Import
from abc import ABC, abstractmethod
from other.sorted_list import SortedList
from typing import Set, Dict, Union, TypeVar

# Import exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum

# Type
TNodeAbstract = TypeVar("TNodeAbstract", bound="NodeAbstract")


class NodeAbstract(ABC):
    """
    Circuit node representation
    """

    """
    Private int id
    Private NodeTypeEnum node_type
    Protected Set<int> literal_in_circuit_set
    Protected Set<int> variable_in_circuit_set
    Private SortedList<int> variable_in_circuit_sorted_list

    Private Dict<str, bool> satisfiable_cache                   
    Private Dict<str, int> model_counting_cache
    Private Dict<str, float> minimal_default_cardinality_cache
    """

    def __init__(self, id: int, node_type: nt_enum.NodeTypeEnum,
                 variable_in_circuit_set: Set[int], literal_in_circuit_set: Set[int]):
        self.__id = id
        self.__node_type: nt_enum.NodeTypeEnum = node_type

        # Initialization
        self._literal_in_circuit_set: Set[int] = set()
        self._variable_in_circuit_set: Set[int] = set()
        self.__variable_in_circuit_sorted_list: SortedList[int] = SortedList()

        self._set_variable_in_circuit_set(variable_in_circuit_set)
        self._set_literal_in_circuit_set(literal_in_circuit_set)

        # Cache
        self.__satisfiable_cache: Dict[str, bool] = dict()
        self.__model_counting_cache: Dict[str, int] = dict()
        self.__minimal_default_cardinality_cache: Dict[str, float] = dict()

    # region Abstract method
    @abstractmethod
    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> bool:
        pass

    @abstractmethod
    def model_counting(self, assumption_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> int:
        pass

    @abstractmethod
    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_cache: bool = True,
                                    mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                                    variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> float:
        pass

    @abstractmethod
    def get_node_size(self) -> int:
        pass
    # endregion

    # region Static method
    @staticmethod
    def use_mapping_on_literal_set(literal_set: Set[int], mapping_dictionary: Dict[int, int]) -> Set[int]:
        """
        :param literal_set: a literal set
        :param mapping_dictionary: a variable mapping dictionary
        :return: a literal set after applying the mapping function
        :raises MappingIsIncompleteException: if some literal does not exist in the mapping
        """

        try:
            result = set(map(lambda l: mapping_dictionary[abs(l)] if l > 0 else -mapping_dictionary[abs(l)], literal_set))
        except KeyError:
            raise c_exception.MappingIsIncompleteException(mapping_dictionary=mapping_dictionary,
                                                           variable_or_literal_in_circuit=literal_set)

        return result

    @staticmethod
    def use_mapping_on_variable_set(variable_set: Set[int], mapping_dictionary: Dict[int, int]) -> Set[int]:
        """
        :param variable_set: a variable set
        :param mapping_dictionary: a variable mapping dictionary
        :return: a variable set after applying the mapping function
        :raises MappingIsIncompleteException: if some variable does not exist in the mapping
        """

        try:
            result = set(map(lambda v: mapping_dictionary[v], variable_set))
        except KeyError:
            raise c_exception.MappingIsIncompleteException(mapping_dictionary=mapping_dictionary,
                                                           variable_or_literal_in_circuit=variable_set)

        return result

    @staticmethod
    def _generate_key_cache(assumption_set: Set[int], exist_quantification_set: Set[int]) -> str:
        """
        Generate a key for caching
        Cache: satisfiable_cache, model_counting_cache, minimal_default_cardinality_cache
        :param assumption_set: an assumption set / observation set
        :param exist_quantification_set: an exist quantification set / default set
        :return: the generated key based on the assumption_set and exist_quantification_set
        """

        assumption_list_temp = sorted(map(str, assumption_set))
        exist_quantification_list_temp = sorted(map(str, exist_quantification_set))

        key_string = ',0,'.join((','.join(assumption_list_temp), ','.join(exist_quantification_list_temp)))

        return key_string
    # endregion

    # region Protected method
    def _add_variable_in_circuit_set(self, variable_set: Set[int]) -> None:
        """
        Add variables to the variable_in_circuit_set.
        If some variable already exists in the variable_in_circuit_set, nothing happens.
        :param variable_set: a set of variables that will be added to the variable_in_circuit_set
        :return: None
        """

        for v in variable_set:
            if v not in self._variable_in_circuit_set:
                self._variable_in_circuit_set.add(v)
                self.__variable_in_circuit_sorted_list.add(v)

    def _remove_variable_in_circuit_set(self, variable_to_delete_set: Set[int]) -> None:
        """
        Remove variables from the variable_in_circuit_set.
        If some variable does not exist in the variable_in_circuit_set, nothing happens.
        :param variable_to_delete_set: a set of variables that will be deleted from the variable_in_circuit_set
        :return: None
        """

        for v in variable_to_delete_set:
            if v in self._variable_in_circuit_set:
                self._variable_in_circuit_set.remove(v)
                self.__variable_in_circuit_sorted_list.remove(v)

    def _set_variable_in_circuit_set(self, new_variable_in_circuit_set: Set[int]) -> None:
        """
        Setter - variable_in_circuit_set
        :return: None
        """

        self._variable_in_circuit_set = new_variable_in_circuit_set
        self.__variable_in_circuit_sorted_list = SortedList(new_variable_in_circuit_set)

    def _get_variable_in_circuit_set(self, copy: bool) -> Set[int]:
        """
        :param copy: True if a copy is returned
        :return: a set of variables in the circuit
        """

        if copy:
            return self._variable_in_circuit_set.copy()

        return self._variable_in_circuit_set

    def _exist_variable_in_circuit_set(self, variable: int) -> bool:
        """
        Check if the variable exists in the variable_in_circuit_set
        :param variable: a variable
        :return: True if the variable exists in the variable_in_circuit_set. Otherwise, False is returned.
        """

        return variable in self._variable_in_circuit_set

    def _add_literal_in_circuit_set(self, literal_set: Set[int]) -> None:
        """
        Add literals to the literal_in_circuit_set.
        If some literal already exists in the literal_in_circuit_set, nothing happens.
        :param literal_set: a set of literals that will be added to the literal_in_circuit_set
        :return: None
        """

        self._literal_in_circuit_set.update(literal_set)

    def _remove_literal_in_circuit_set(self, literal_to_delete_set: Set[int]) -> None:
        """
        Remove literals from the literal_in_circuit_set.
        If some literal does not exist in the literal_in_circuit_set, nothing happens.
        :param literal_to_delete_set: a set of literals that will be deleted from the literal_in_circuit_set
        :return: None
        """

        self._literal_in_circuit_set.difference_update(literal_to_delete_set)

    def _set_literal_in_circuit_set(self, new_literal_in_circuit_set: Set[int]) -> None:
        """
        Setter - literal_in_circuit_set
        :return: None
        """

        self._literal_in_circuit_set = new_literal_in_circuit_set

    def _get_literal_in_circuit_set(self, copy: bool) -> Set[int]:
        """
        :param copy: True if a copy is returned
        :return: a set of literals in the circuit
        """

        if copy:
            return self._literal_in_circuit_set.copy()

        return self._literal_in_circuit_set

    def _exist_literal_in_circuit_set(self, literal: int) -> bool:
        """
        Check if the literal exists in the literal_in_circuit_set
        :param literal: a literal
        :return: True if the literal exists in the literal_in_circuit_set. Otherwise, False is returned.
        """

        return literal in self._literal_in_circuit_set

    # region Cache
    def _add_satisfiable_cache(self, key: Union[str, None], satisfiable: bool) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        Cache: satisfiable_cache
        :param key: the key
        :param satisfiable: the value
        :return: None
        """

        # Invalid key
        if key is None:
            return

        self.__satisfiable_cache[key] = satisfiable

    def _get_satisfiable_cache(self, key: Union[str, None]) -> Union[bool, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        Cache: satisfiable_cache
        :param key: the key
        :return: the record's value if the record exists. Otherwise, None is returned.
        """

        if (key is None) or (key not in self.__satisfiable_cache):
            return None

        return self.__satisfiable_cache[key]

    def _clear_satisfiable_cache(self) -> None:
        """
        Clear the cache
        Cache: satisfiable_cache
        :return: None
        """

        self.__satisfiable_cache = dict()

    def _add_model_counting_cache(self, key: Union[str, None], model_count: int) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        Cache: model_counting_cache
        :param key: the key
        :param model_count: the value
        :return: None
        """

        # Invalid key
        if key is None:
            return

        self.__model_counting_cache[key] = model_count

    def _get_model_counting_cache(self, key: Union[str, None]) -> Union[int, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        Cache: model_counting_cache
        :param key: the key
        :return: the record's value if the record exists. Otherwise, None is returned.
        """

        if (key is None) or (key not in self.__model_counting_cache):
            return None

        return self.__model_counting_cache[key]

    def _clear_model_counting_cache(self) -> None:
        """
        Clear the cache
        Cache: model_counting_cache
        :return: None
        """

        self.__model_counting_cache = dict()

    def _add_minimal_default_cardinality_cache(self, key: Union[str, None], minimal_default_cardinality: float) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        Cache: minimal_default_cardinality_cache
        :param key: the key
        :param minimal_default_cardinality: the value
        :return: None
        """

        # Invalid key
        if key is None:
            return

        self.__minimal_default_cardinality_cache[key] = minimal_default_cardinality

    def _get_minimal_default_cardinality_cache(self, key: Union[str, None]) -> Union[float, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        Cache: minimal_default_cardinality_cache
        :param key: the key
        :return: the record's value if the record exists. Otherwise, None is returned.
        """

        if (key is None) or (key not in self.__minimal_default_cardinality_cache):
            return None

        return self.__minimal_default_cardinality_cache[key]

    def _clear_minimal_default_cardinality_cache(self) -> None:
        """
        Clear the cache
        Cache: minimal_default_cardinality_cache
        :return: None
        """

        self.__minimal_default_cardinality_cache = dict()

    def _clear_caches(self) -> None:
        """
        Clear all caches
        Cache: satisfiable_cache, model_counting_cache, minimal_default_cardinality_cache
        :return: None
        """

        self._clear_satisfiable_cache()
        self._clear_model_counting_cache()
        self._clear_minimal_default_cardinality_cache()
    # endregion

    def _create_restricted_assumption_set(self, assumption_set: Set[int], variable_id_mapping_id_dictionary: Union[Dict[int, int], None]) -> Set[int]:
        """
        :param assumption_set: an assumption set
        :param variable_id_mapping_id_dictionary: a variable mapping dictionary (None = no mapping)
        :return: the restricted assumption set
        :raises MappingIsIncompleteException: if the mapping is incomplete in the circuit
        """

        # Mapping is used
        if variable_id_mapping_id_dictionary is not None:
            try:
                result = set(filter(lambda l: self._exist_variable_in_circuit_set(variable_id_mapping_id_dictionary[abs(l)]), assumption_set))
            except KeyError:
                raise c_exception.MappingIsIncompleteException(mapping_dictionary=variable_id_mapping_id_dictionary,
                                                               variable_or_literal_in_circuit=self._variable_in_circuit_set)
        else:
            result = set(filter(lambda l: self._exist_variable_in_circuit_set(abs(l)), assumption_set))

        return result

    def _create_restricted_exist_quantification_set(self, exist_quantification_set: Set[int], mapping_id_variable_id_dictionary: Union[Dict[int, int], None]) -> Set[int]:
        """
        :param exist_quantification_set: an exist quantification set
        :param mapping_id_variable_id_dictionary: a variable mapping dictionary (None = no mapping)
        :return: the restricted exist quantification set
        :raises MappingIsIncompleteException: if the mapping is incomplete in the circuit
        """

        # Mapping is used
        if mapping_id_variable_id_dictionary is not None:
            try:
                result = exist_quantification_set.intersection(map(lambda v: mapping_id_variable_id_dictionary[v], self._variable_in_circuit_set))
            except KeyError:
                raise c_exception.MappingIsIncompleteException(mapping_dictionary=mapping_id_variable_id_dictionary,
                                                               variable_or_literal_in_circuit=self._variable_in_circuit_set)
        else:
            result = exist_quantification_set.intersection(self._variable_in_circuit_set)

        return result
    # endregion

    # region Magic method
    def __str__(self):
        return str(self.__id)

    def __repr__(self):
        literal_in_circuit_sorted_list_temp = SortedList(self._literal_in_circuit_set)

        string_temp = " ".join((f"ID: {str(self.__id)}",
                                f"Node type: {self.__node_type.name}",
                                f"Variables in the circuit: {str(self.__variable_in_circuit_sorted_list)}",
                                f"Literals in the circuit: {str(literal_in_circuit_sorted_list_temp)}"))

        return string_temp
    # endregion

    # region Property
    @property
    def node_type(self) -> nt_enum.NodeTypeEnum:
        return self.__node_type

    @property
    def id(self) -> int:
        return self.__id

    @property
    def number_of_variables(self) -> int:
        return len(self._variable_in_circuit_set)
    # endregion
