# Import
from abc import ABC, abstractmethod
from typing import Dict, Union, Set, List
from formula.incidence_graph import IncidenceGraph

# TODO Cleaning strategy
# TODO Heap activity


class ComponentCachingAbstract(ABC):
    """
    Component caching
    """

    """
    Private Dict<str, int> cache                # key: hash, value: an identifier of a node
    Private Set<str> multi_occurrence_cache
    
    Protected str delimiter
    Protected str end_delimiter
    Protected str end_delimiter_2
    """

    def __init__(self):
        self.__cache: Dict[str, int] = dict()
        self.__multi_occurrence_cache: Set[str] = set()

        self._delimiter = ","
        self._end_delimiter = f"{self._delimiter}0{self._delimiter}"
        self._end_delimiter_2 = f"{self._delimiter}00{self._delimiter}"

    # region Abstract method
    @abstractmethod
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Union[str, None]:
        """
        Generate a key for caching.
        None is returned if the formula represented by the incidence graph is not cacheable.
        :param incidence_graph: an incidence graph
        :return: the generated key based on the incidence graph
        """

        pass
    # endregion

    # region Public method
    def add(self, key: Union[str, None], node_id: int) -> None:
        """
        Add a new record to the cache.
        If the key is None, nothing happens.
        If the record already exists in the cache, the value of the record will be updated.
        :param key: the key
        :param node_id: the value
        :return: None
        """

        # Invalid key
        if key is None:
            return

        self.__cache[key] = node_id

    def get(self, key: Union[str, None]) -> Union[int, None]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, None is returned.
        :param key: the key
        :return: the record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if not self.exist(key):
            return None

        return self.__cache[key]

    def exist(self, key: Union[str, None]) -> bool:
        """
        Check if a record with the key exists in the cache
        :param key: the key
        :return: True if the key exists in the cache. Otherwise, False is returned.
        """

        if (key is None) or (key not in self.__cache):
            return False

        return True
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
