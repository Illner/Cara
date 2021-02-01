# Import
from typing import Union, TypeVar
from abc import ABC, abstractmethod
from other.sorted_list import SortedList

# Import exception
import exception.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum

# Type
TNodeAbstract = TypeVar("TNodeAbstract", bound="NodeAbstract")

# TODO Literal list


class NodeAbstract(ABC):
    """
    Circuit node representation
    """

    """
    Private int id
    Private NodeTypeEnum node_type
    Private int size                                # The number of edges in the circuit + the sizes of all leaves in the circuit
    Private Set<NodeAbstract> node_in_circuit_set   # The set which contains all nodes in the circuit
    Private Set<int> variable_in_circuit_set
    Private SortedList<int> variable_in_circuit_sorted_list
    Private Set<int> literal_in_circuit_set
    
    Private Dict<str, bool> satisfiable_cache                   # key = {0|1}+
    Private Dict<str, int> model_counting_cache                 # key = {0|1}+
    Private Dict<str, float> minimal_default_cardinality_cache  # key = {0|1}+
    """

    def __init__(self, id: int, node_type: nt_enum.NodeTypeEnum,
                 variable_in_circuit_set: set[int], literal_in_circuit_set: set[int],
                 node_in_circuit_set: set[TNodeAbstract], size: int = 0):
        self.__node_type: nt_enum.NodeTypeEnum = node_type
        self.__size: int = size
        self.__id = id

        self.__node_in_circuit_set: set[TNodeAbstract] = node_in_circuit_set
        self.__variable_in_circuit_set: set[int] = set()                        # initialization
        self.__variable_in_circuit_sorted_list: SortedList[int] = SortedList()  # initialization
        self.__literal_in_circuit_set: set[int] = set()                         # initialization

        self._set_variable_in_circuit_set(variable_in_circuit_set)
        self._set_literal_in_circuit_set(literal_in_circuit_set)

        # Cache
        self.__satisfiable_cache: dict[str, bool] = dict()                      # initialization
        self.__model_counting_cache: dict[str, int] = dict()                    # initialization
        self.__minimal_default_cardinality_cache: dict[str, float] = dict()     # initialization

    # region Abstract method
    @abstractmethod
    def is_satisfiable(self, assumption_set: set[int], exist_quantification_set: set[int], use_caches: bool = True) -> bool:
        pass

    @abstractmethod
    def model_counting(self, assumption_set: set[int], exist_quantification_set: set[int], use_caches: bool = True) -> int:
        pass

    @abstractmethod
    def minimum_default_cardinality(self, default_set: set[int], use_caches: bool = True) -> float:
        pass

    @abstractmethod
    def smooth(self, smooth_create_and_node_function) -> None:
        pass
    # endregion

    # region Protected method
    def _update_size(self, addend: int) -> None:
        """
        The addend will be added to the size. If the size after the update will be less than 0, raise an exception (SizeCannotBeLessThanZeroException).
        The addend is greater than 0 => addition
        The addend is less than 0 => subtraction
        """

        # The size after the update is negative
        if self.__size + addend < 0:
            raise c_exception.SizeCannotBeLessThanZeroException(str(self))

        self.__size += addend

    def _update_size_based_on_children(self, child_set: set[TNodeAbstract]) -> None:
        """
        The size will be changed to the sum of the sizes of all children (child_set) and the number of children
        :param child_set: the children set
        """

        self.__size = len(child_set)
        for child in child_set:
            self.__size += child.size

    def _add_variable_in_circuit_set(self, variable_set: set[int]) -> None:
        """
        Add the variables in the variable_set to the variable_in_circuit_set.
        If some variable already exists in the variable_in_circuit_set, nothing happens.
        :param variable_set: a set of variables which will be added to the variable_in_circuit_set
        """

        # Update variable_in_circuit_sorted_list
        for v in variable_set:
            if v not in self.__variable_in_circuit_set:
                self.__variable_in_circuit_sorted_list.add(v)

        # Update variable_in_circuit_set
        self.__variable_in_circuit_set.update(variable_set)

    def _remove_variable_in_circuit_set(self, variable_to_delete_set: set[int]) -> None:
        """
        Remove the variables in the variable_to_delete_set from the variable_in_circuit_set.
        If some variable does not exist in the variable_in_circuit_set, nothing happens.
        :param variable_to_delete_set: a set of variables which will be deleted from the variable_in_circuit_set
        """

        # Update variable_in_circuit_sorted_list
        for v in variable_to_delete_set:
            if v in self.__variable_in_circuit_set:
                self.__variable_in_circuit_sorted_list.remove(v)

        # Update variable_in_circuit_set
        self.__variable_in_circuit_set.difference_update(variable_to_delete_set)

    def _set_variable_in_circuit_set(self, new_variable_in_circuit_set: set[int]) -> None:
        """
        Setter - variable_in_circuit_set
        """

        self.__variable_in_circuit_set = new_variable_in_circuit_set
        self.__variable_in_circuit_sorted_list = SortedList(new_variable_in_circuit_set)

    def _get_variable_in_circuit_set(self, copy: bool = False) -> set[int]:
        """
        Getter - variable_in_circuit_set
        """

        if copy:
            return self.__variable_in_circuit_set.copy()

        return self.__variable_in_circuit_set

    def _exist_variable_in_circuit_set(self, variable: int) -> bool:
        """
        Check if the variable exists in the variable_in_circuit_set
        :param variable: the variable
        :return: True if the variable exists in the variable_in_circuit_set. Otherwise False is returned.
        """

        return variable in self.__variable_in_circuit_set

    def _add_literal_in_circuit_set(self, literal_set: set[int]) -> None:
        """
        Add the literals in the literal_set to the literal_in_circuit_set.
        If some literal already exists in the literal_in_circuit_set, nothing happens.
        :param literal_set: a set of literals which will be added to the literal_in_circuit_set
        """

        self.__literal_in_circuit_set.update(literal_set)

    def _remove_literal_in_circuit_set(self, literal_to_delete_set: set[int]) -> None:
        """
        Remove the literals in the literal_to_delete_set from the literal_in_circuit_set.
        If some literal does not exist in the literal_in_circuit_set, nothing happens.
        :param literal_to_delete_set: a set of literals which will be deleted from the literal_in_circuit_set
        """

        self.__literal_in_circuit_set.difference_update(literal_to_delete_set)

    def _set_literal_in_circuit_set(self, new_literal_in_circuit_set: set[int]) -> None:
        """
        Setter - literal_in_circuit_set
        """

        self.__literal_in_circuit_set = new_literal_in_circuit_set

    def _get_literal_in_circuit_set(self, copy: bool = False) -> set[int]:
        """
        Getter - literal_in_circuit_set
        """

        if copy:
            return self.__literal_in_circuit_set.copy()

        return self.__literal_in_circuit_set

    def _exist_literal_in_circuit_set(self, literal: int) -> bool:
        """
        Check if the literal exists in the literal_in_circuit_set
        :param literal: the literal
        :return: True if the literal exists in the literal_in_circuit_set. Otherwise False is returned.
        """

        return literal in self.__literal_in_circuit_set

    def _add_node_in_circuit_set(self, node_set: set[TNodeAbstract]) -> None:
        """
        Add the nodes in the node_set to the node_in_circuit_set.
        If some node already exists in the node_in_circuit_set, nothing happens.
        :param node_set: the set of nodes which will be added to the node_in_circuit_set
        """

        self.__node_in_circuit_set = self.__node_in_circuit_set.union(node_set)

    def _remove_node_in_circuit_set(self, node_to_delete_set: set[TNodeAbstract]) -> None:
        """
        Remove the nodes in the node_to_delete_set from the node_in_circuit_set.
        If some node does not exist in the node_in_circuit_set, nothing happens.
        :param node_to_delete_set: the set of nodes which will be deleted from the node_in_circuit_set
        """

        self.__node_in_circuit_set = self.__node_in_circuit_set.difference(node_to_delete_set)

    def _set_node_in_circuit_set(self, new_node_in_circuit_set: set[TNodeAbstract]) -> None:
        """
        Setter - variable_in_circuit_set
        """

        self.__node_in_circuit_set = new_node_in_circuit_set

    def _get_node_in_circuit_set(self, copy: bool = False) -> set[TNodeAbstract]:
        """
        Getter - node_in_circuit_set
        """

        if copy:
            return self.__node_in_circuit_set.copy()

        return self.__node_in_circuit_set

    def _exist_node_in_circuit_set(self, node: TNodeAbstract) -> bool:
        """
        Check if the node exists in the node_in_circuit_set
        :param node: the node
        :return: True if the node exists in the node_in_circuit_set. Otherwise False is returned.
        """

        return node in self.__node_in_circuit_set

    def _add_satisfiable_cache(self, key: str, satisfiable: bool) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        :param key: the key
        :param satisfiable: the value
        """

        self.__satisfiable_cache[key] = satisfiable

    def _get_satisfiable_cache(self, key: str) -> Union[bool, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        :param key: the key
        :return: The record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if key not in self.__satisfiable_cache:
            return None

        return self.__satisfiable_cache[key]

    def _clear_satisfiable_cache(self) -> None:
        """
        Clear the cache
        """

        self.__satisfiable_cache = dict()

    def _add_model_counting_cache(self, key: str, model_count: int) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        :param key: the key
        :param model_count: the value
        """

        self.__model_counting_cache[key] = model_count

    def _get_model_counting_cache(self, key: str) -> Union[int, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        :param key: the key
        :return: The record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if key not in self.__model_counting_cache:
            return None

        return self.__model_counting_cache[key]

    def _clear_model_counting_cache(self) -> None:
        """
        Clear the cache
        """

        self.__model_counting_cache = dict()

    def _add_minimal_default_cardinality_cache(self, key: str, minimal_default_cardinality: float) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        :param key: the key
        :param minimal_default_cardinality: the value
        """

        self.__minimal_default_cardinality_cache[key] = minimal_default_cardinality

    def _get_minimal_default_cardinality_cache(self, key: str) -> Union[float, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        :param key: the key
        :return: The record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if key not in self.__minimal_default_cardinality_cache:
            return None

        return self.__minimal_default_cardinality_cache[key]

    def _clear_minimal_default_cardinality_cache(self) -> None:
        """
        Clear the cache
        """

        self.__minimal_default_cardinality_cache = dict()

    def _clear_cache(self) -> None:
        """
        Clear all caches
        Cache: satisfiable_cache, model_counting_cache, minimal_default_cardinality_cache
        """

        self._clear_satisfiable_cache()
        self._clear_model_counting_cache()
        self._clear_minimal_default_cardinality_cache()

    def _generate_key_cache(self, assumption_set: set[int], exist_quantification_set: set[int]) -> str:
        """
        Generate a key for caching.
        Cache: satisfiable_cache, model_counting_cache
        :param assumption_set: the assumption set (can be empty)
        :param exist_quantification_set: the exist quantification set (can be empty)
        :return: the generated key based on the assumption_set, exist_quantification_set and variable_in_circuit_set
        """

        assumption_list_temp = []
        exist_quantification_list_temp = []

        it = self.__variable_in_circuit_sorted_list.irange()
        for v in it:
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

        assumption_str_temp = ''.join(assumption_list_temp)
        exist_quantification_str_temp = ''.join(exist_quantification_list_temp)
        str_temp = ''.join((assumption_str_temp, exist_quantification_str_temp))

        return str_temp

    def _generate_key_minimal_default_cardinality_cache(self, default_set: set[int]) -> str:
        """
        Generate a key for the minimal_default_cardinality_cache
        :param default_set: the default set (can be empty)
        :return: the generated key based on the default_set and variable_in_circuit_set
        """

        default_list_temp = []

        it = self.__variable_in_circuit_sorted_list.irange()
        for v in it:
            if v in default_set:
                default_list_temp.append("1")
            else:
                default_list_temp.append("-")

        str_temp = ''.join(default_list_temp)

        return str_temp
    # endregion

    # region Magic method
    def __str__(self):
        return str(self.__id)

    def __repr__(self):
        string_temp = " ".join((f"ID: {str(self.__id)}",
                                f"Node type: {self.__node_type.name}",
                                f"Size: {str(self.__size)}",
                                f"Variables in the circuit: {self.__variable_in_circuit_sorted_list}"))

        # Nodes in the circuit
        string_temp = " ".join((string_temp, "Nodes in the circuit:"))
        node_id_in_circuit_sorted_list_temp = SortedList()
        for node in self.__node_in_circuit_set:
            node_id_in_circuit_sorted_list_temp.add(node.id)
        string_temp = " ".join((string_temp, str(node_id_in_circuit_sorted_list_temp)))

        return string_temp
    # endregion

    # region Property
    @property
    def node_type(self):
        return self.__node_type

    @property
    def size(self):
        return self.__size

    @property
    def id(self):
        return self.__id

    @property
    def number_of_variables(self):
        return len(self.__variable_in_circuit_set)

    @property
    def number_of_nodes(self):
        return len(self.__node_in_circuit_set)
    # endregion
