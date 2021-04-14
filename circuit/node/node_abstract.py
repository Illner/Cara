# Import
from abc import ABC, abstractmethod
from other.sorted_list import SortedList
from typing import Set, Dict, Union, TypeVar

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
    Private Set<NodeAbstract> node_in_circuit_set                   # a set that contains all nodes in the circuit
    Private Set<int> variable_in_circuit_set
    Private SortedList<int> variable_in_circuit_sorted_list
    Private Set<int> literal_in_circuit_set

    Private Dict<str, bool> satisfiable_cache                   
    Private Dict<str, int> model_counting_cache
    Private Dict<str, float> minimal_default_cardinality_cache
    """

    def __init__(self, id: int, node_type: nt_enum.NodeTypeEnum,
                 variable_in_circuit_set: Set[int], literal_in_circuit_set: Set[int],
                 node_in_circuit_set: Set[TNodeAbstract]):
        self.__id = id
        self.__node_type: nt_enum.NodeTypeEnum = node_type

        self.__node_in_circuit_set: Set[TNodeAbstract] = node_in_circuit_set
        self.__variable_in_circuit_set: Set[int] = set()
        self.__variable_in_circuit_sorted_list: SortedList[int] = SortedList()
        self.__literal_in_circuit_set: Set[int] = set()

        self._set_variable_in_circuit_set(variable_in_circuit_set)
        self._set_literal_in_circuit_set(literal_in_circuit_set)

        # Cache
        self.__satisfiable_cache: Dict[str, bool] = dict()
        self.__model_counting_cache: Dict[str, int] = dict()
        self.__minimal_default_cardinality_cache: Dict[str, float] = dict()

    # region Abstract method
    @abstractmethod
    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True) -> bool:
        pass

    @abstractmethod
    def model_counting(self, assumption_set: Set[int], use_cache: bool = True) -> int:
        pass

    @abstractmethod
    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_cache: bool = True) -> float:
        pass

    @abstractmethod
    def get_node_size(self) -> int:
        pass
    # endregion

    # region Protected method
    def _add_variable_in_circuit_set(self, variable_set: Set[int]) -> None:
        """
        Add variables to the variable_in_circuit_set.
        If some variable already exists in the variable_in_circuit_set, nothing happens.
        :param variable_set: a set of variables that will be added to the variable_in_circuit_set
        :return: None
        """

        # Update variable_in_circuit_sorted_list
        for v in variable_set:
            if v not in self.__variable_in_circuit_set:
                self.__variable_in_circuit_sorted_list.add(v)

        # Update variable_in_circuit_set
        self.__variable_in_circuit_set.update(variable_set)

    def _remove_variable_in_circuit_set(self, variable_to_delete_set: Set[int]) -> None:
        """
        Remove variables from the variable_in_circuit_set.
        If some variable does not exist in the variable_in_circuit_set, nothing happens.
        :param variable_to_delete_set: a set of variables that will be deleted from the variable_in_circuit_set
        :return: None
        """

        # Update variable_in_circuit_sorted_list
        for v in variable_to_delete_set:
            if v in self.__variable_in_circuit_set:
                self.__variable_in_circuit_sorted_list.remove(v)

        # Update variable_in_circuit_set
        self.__variable_in_circuit_set.difference_update(variable_to_delete_set)

    def _set_variable_in_circuit_set(self, new_variable_in_circuit_set: Set[int]) -> None:
        """
        Setter - variable_in_circuit_set
        :return: None
        """

        self.__variable_in_circuit_set = new_variable_in_circuit_set
        self.__variable_in_circuit_sorted_list = SortedList(new_variable_in_circuit_set)

    def _get_variable_in_circuit_set(self, copy: bool) -> Set[int]:
        """
        :param copy: True if a copy is returned
        :return: a set of variables in the circuit
        """

        if copy:
            return self.__variable_in_circuit_set.copy()

        return self.__variable_in_circuit_set

    def _exist_variable_in_circuit_set(self, variable: int) -> bool:
        """
        Check if the variable exists in the variable_in_circuit_set
        :param variable: the variable
        :return: True if the variable exists in the variable_in_circuit_set. Otherwise, False is returned.
        """

        return variable in self.__variable_in_circuit_set

    def _add_literal_in_circuit_set(self, literal_set: Set[int]) -> None:
        """
        Add literals to the literal_in_circuit_set.
        If some literal already exists in the literal_in_circuit_set, nothing happens.
        :param literal_set: a set of literals that will be added to the literal_in_circuit_set
        :return: None
        """

        self.__literal_in_circuit_set.update(literal_set)

    def _remove_literal_in_circuit_set(self, literal_to_delete_set: Set[int]) -> None:
        """
        Remove literals from the literal_in_circuit_set.
        If some literal does not exist in the literal_in_circuit_set, nothing happens.
        :param literal_to_delete_set: a set of literals that will be deleted from the literal_in_circuit_set
        :return: None
        """

        self.__literal_in_circuit_set.difference_update(literal_to_delete_set)

    def _set_literal_in_circuit_set(self, new_literal_in_circuit_set: Set[int]) -> None:
        """
        Setter - literal_in_circuit_set
        :return: None
        """

        self.__literal_in_circuit_set = new_literal_in_circuit_set

    def _get_literal_in_circuit_set(self, copy: bool) -> Set[int]:
        """
        :param copy: True if a copy is returned
        :return: a set of literals in the circuit
        """

        if copy:
            return self.__literal_in_circuit_set.copy()

        return self.__literal_in_circuit_set

    def _exist_literal_in_circuit_set(self, literal: int) -> bool:
        """
        Check if the literal exists in the literal_in_circuit_set
        :param literal: the literal
        :return: True if the literal exists in the literal_in_circuit_set. Otherwise, False is returned.
        """

        return literal in self.__literal_in_circuit_set

    def _add_node_in_circuit_set(self, node_set: Set[TNodeAbstract]) -> None:
        """
        Add nodes to the node_in_circuit_set.
        If some node already exists in the node_in_circuit_set, nothing happens.
        :param node_set: a set of nodes that will be added to the node_in_circuit_set
        :return: None
        """

        self.__node_in_circuit_set = self.__node_in_circuit_set.union(node_set)

    def _remove_node_in_circuit_set(self, node_to_delete_set: Set[TNodeAbstract]) -> None:
        """
        Remove nodes from the node_in_circuit_set.
        If some node does not exist in the node_in_circuit_set, nothing happens.
        :param node_to_delete_set: a set of nodes that will be deleted from the node_in_circuit_set
        :return: None
        """

        self.__node_in_circuit_set = self.__node_in_circuit_set.difference(node_to_delete_set)

    def _set_node_in_circuit_set(self, new_node_in_circuit_set: Set[TNodeAbstract]) -> None:
        """
        Setter - variable_in_circuit_set
        :return: None
        """

        self.__node_in_circuit_set = new_node_in_circuit_set

    def _get_node_in_circuit_set(self, copy: bool) -> Set[TNodeAbstract]:
        """
        :param copy: True if a copy is returned
        :return: a set of nodes in the circuit
        """

        if copy:
            return self.__node_in_circuit_set.copy()

        return self.__node_in_circuit_set

    def _exist_node_in_circuit_set(self, node: TNodeAbstract) -> bool:
        """
        Check if the node exists in the node_in_circuit_set
        :param node: the node
        :return: True if the node exists in the node_in_circuit_set. Otherwise, False is returned.
        """

        return node in self.__node_in_circuit_set

    def _add_satisfiable_cache(self, key: str, satisfiable: bool) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        :param key: the key
        :param satisfiable: the value
        :return: None
        """

        self.__satisfiable_cache[key] = satisfiable

    def _get_satisfiable_cache(self, key: str) -> Union[bool, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        :param key: the key
        :return: the record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if key not in self.__satisfiable_cache:
            return None

        return self.__satisfiable_cache[key]

    def _clear_satisfiable_cache(self) -> None:
        """
        Clear the cache
        :return: None
        """

        self.__satisfiable_cache = dict()

    def _add_model_counting_cache(self, key: str, model_count: int) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        :param key: the key
        :param model_count: the value
        :return: None
        """

        self.__model_counting_cache[key] = model_count

    def _get_model_counting_cache(self, key: str) -> Union[int, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        :param key: the key
        :return: the record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if key not in self.__model_counting_cache:
            return None

        return self.__model_counting_cache[key]

    def _clear_model_counting_cache(self) -> None:
        """
        Clear the cache
        :return: None
        """

        self.__model_counting_cache = dict()

    def _add_minimal_default_cardinality_cache(self, key: str, minimal_default_cardinality: float) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        :param key: the key
        :param minimal_default_cardinality: the value
        :return: None
        """

        self.__minimal_default_cardinality_cache[key] = minimal_default_cardinality

    def _get_minimal_default_cardinality_cache(self, key: str) -> Union[float, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        :param key: the key
        :return: the record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if key not in self.__minimal_default_cardinality_cache:
            return None

        return self.__minimal_default_cardinality_cache[key]

    def _clear_minimal_default_cardinality_cache(self) -> None:
        """
        Clear the cache
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

    def _generate_key_cache(self, assumption_set: Set[int], exist_quantification_set: Set[int]) -> str:
        """
        Generate a key for caching
        Cache: satisfiable_cache, model_counting_cache, minimal_default_cardinality_cache
        :param assumption_set: an assumption set / observation set (can be empty)
        :param exist_quantification_set: an exist quantification set / default set (can be empty)
        :return: the generated key based on the assumption_set, exist_quantification_set and variable_in_circuit_set
        """

        assumption_list_temp = []
        exist_quantification_list_temp = []

        variable_iterator = self.__variable_in_circuit_sorted_list.irange()
        for v in variable_iterator:
            # The assumption list
            if v in assumption_set:
                assumption_list_temp.append("1")
            elif -v in assumption_set:
                assumption_list_temp.append("0")
            else:
                assumption_list_temp.append("-")

            # The exist quantification list
            if v in exist_quantification_set:
                exist_quantification_list_temp.append("1")
            elif -v in exist_quantification_set:
                exist_quantification_list_temp.append("0")
            else:
                exist_quantification_list_temp.append("-")

        key_string = ''.join((''.join(assumption_list_temp), ''.join(exist_quantification_list_temp)))

        return key_string

    def _create_restricted_assumption_set(self, assumption_set: Set[int]) -> Set[int]:
        """
        :param assumption_set: an assumption set
        :return: the restricted assumption set
        """

        return set(filter(lambda l: self._exist_variable_in_circuit_set(abs(l)), assumption_set))

    def _create_restricted_exist_quantification_set(self, exist_quantification_set: Set[int]) -> Set[int]:
        """
        :param exist_quantification_set: an exist quantification set
        :return: the restricted exist quantification set
        """

        return exist_quantification_set.intersection(self._get_variable_in_circuit_set(copy=False))
    # endregion

    # region Magic method
    def __str__(self):
        return str(self.__id)

    def __repr__(self):
        literal_in_circuit_sorted_list_temp = SortedList(self.__literal_in_circuit_set)

        string_temp = " ".join((f"ID: {str(self.__id)}",
                                f"Node type: {self.__node_type.name}",
                                f"Variables in the circuit: {self.__variable_in_circuit_sorted_list}",
                                f"Literals in the circuit: {literal_in_circuit_sorted_list_temp}"))

        # The nodes in the circuit
        string_temp = " ".join((string_temp, "Nodes in the circuit:"))
        node_id_in_circuit_sorted_list_temp = SortedList()
        for node in self.__node_in_circuit_set:
            node_id_in_circuit_sorted_list_temp.add(node.id)
        string_temp = " ".join((string_temp, str(node_id_in_circuit_sorted_list_temp)))

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
        return len(self.__variable_in_circuit_set)

    @property
    def number_of_nodes(self) -> int:
        return len(self.__node_in_circuit_set)
    # endregion
