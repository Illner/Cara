# Import
from abc import ABC, abstractmethod
from typing import Dict, Union, Set, List, Tuple
from formula.incidence_graph import IncidenceGraph

# TODO Cleaning strategy
# TODO Heap activity


class ComponentCachingAbstract(ABC):
    """
    Component caching
    """

    """
    Private int id_counter
    Private Dict<str, int> hash_key_cache                   # key: hash, value: a key
    Private Dict<int, int> key_node_cache                   # key: a key, value: an identifier of a node
    Private Dict<int, Dict<int, int>> key_mapping_cache     # key: a key, value: a variable mapping
    Private Set<str> multi_occurrence_cache
    
    Protected str delimiter
    Protected str end_delimiter
    Protected str end_delimiter_2
    """

    def __init__(self):
        self.__id_counter: int = 0
        self.__hash_key_cache: Dict[str, int] = dict()
        self.__key_node_cache: Dict[int, int] = dict()
        self.__key_mapping_cache: Dict[int, Dict[int, int]] = dict()
        self.__multi_occurrence_cache: Set[str] = set()

        self._delimiter = ","
        self._end_delimiter = f"{self._delimiter}0{self._delimiter}"
        self._end_delimiter_2 = f"{self._delimiter}00{self._delimiter}"

    # region Abstract method
    @abstractmethod
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Tuple[Union[str, None], Union[Tuple[Dict[int, int], Dict[int, int]], None]]:
        """
        Generate a key for caching.
        (None, None) is returned if the formula represented by the incidence graph is not cacheable.
        (generated_key, None) is returned if the variable mapping is not supported by the caching scheme.
        :param incidence_graph: an incidence graph
        :return: the generated key based on the incidence graph and both mappings between variables (variable_id -> mapping_id, mapping_id -> variable_id)
        """

        pass
    # endregion

    # region Public method
    def add(self, hash_key: Union[str, None], node_id: int, mapping: Union[Dict[int, int], None] = None) -> None:
        """
        Add a new record to the cache.
        If the key is None, nothing happens.
        If the record already exists in the cache, the value of the record (node_id and mapping) will be updated.
        :param hash_key: the hash
        :param node_id: the value
        :param mapping: the variable mapping (optional)
        :return: None
        """

        # Invalid key
        if hash_key is None:
            return

        # The key already exists in the cache
        if self.exist(hash_key):
            id_key = self.__hash_key_cache[hash_key]
        else:
            id_key = self.__get_new_id()

        self.__hash_key_cache[hash_key] = id_key
        self.__key_node_cache[id_key] = node_id

        if id_key in self.__key_mapping_cache:
            del self.__key_mapping_cache[id_key]

        if mapping is not None:
            self.__key_mapping_cache[id_key] = mapping

    def get(self, hash_key: Union[str, None]) -> Tuple[Union[int, None], Union[Dict[int, int], None]]:
        """
        Return the value of the record (node_id and mapping) with the key from the cache.
        If the record does not exist in the cache, (None, None) is returned.
        :param hash_key: the hash
        :return: the record's value (node_id and mapping) if the record exists. Otherwise, (None, None) is returned.
        """

        # The record does not exist
        if not self.exist(hash_key):
            return None, None

        id_key = self.__hash_key_cache[hash_key]
        node_id = self.__key_node_cache[id_key]

        mapping = None
        if id_key in self.__key_mapping_cache:
            mapping = self.__key_mapping_cache[id_key]

        return node_id, mapping

    def exist(self, hash_key: Union[str, None]) -> bool:
        """
        Check if a record with the key exists in the cache
        :param hash_key: the hash
        :return: True if the key exists in the cache. Otherwise, False is returned.
        """

        if (hash_key is None) or (hash_key not in self.__hash_key_cache):
            return False

        return True
    # endregion

    # region Private method
    def __get_new_id(self) -> int:
        """
        Return a new ID.
        The ID counter will be incremented.
        :return: a new ID
        """

        id_temp = self.__id_counter
        self.__id_counter += 1

        return id_temp
    # endregion

    # region Protected method
    def _add_multi_occurrence_cache(self, key: str) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, nothing happens.
        :param key: the key
        :return: None
        """

        self.__multi_occurrence_cache.add(key)

    def _exist_multi_occurrence_cache(self, key: str) -> bool:
        """
        :return: True if the key exists in the cache. Otherwise, False is returned.
        """

        return key in self.__multi_occurrence_cache

    def _clear_multi_occurrence_cache(self) -> None:
        """
        Clear the cache
        :return: None
        """

        self.__multi_occurrence_cache = set()

    def _generate_key_multi_occurrence_cache(self, clause_list: List[int]) -> str:
        """
        Generate a key for caching
        Cache: multi_occurrence_cache
        :param clause_list: a clause (should be sorted)
        :return: the generated key
        """

        clause_key_string = self._delimiter.join([str(lit) for lit in clause_list])

        return clause_key_string
    # endregion
