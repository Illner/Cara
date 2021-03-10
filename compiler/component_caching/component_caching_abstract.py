# Import
from typing import Dict, Union
from abc import ABC, abstractmethod
from formula.incidence_graph import IncidenceGraph

# TODO Cleaning strategy
# TODO Heap activity
# TODO Subsumed clauses


class ComponentCachingAbstract(ABC):
    """
    Component caching
    """

    """
    Private Dict<str, int> cache
    """

    def __init__(self):
        self.__cache: Dict[str, int] = dict()

    # region Abstract method
    @abstractmethod
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Union[str, None]:
        """
        Generate a key for caching.
        None is returned if the formula represented by the incidence graph is not cacheable.
        :param incidence_graph: the incidence graph
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
        :return: The record's value if the record exists. Otherwise, None is returned.
        """

        # The record does not exist
        if not self.exist(key):
            return None

        return self.__cache[key]

    def exist(self, key: Union[int, None]) -> bool:
        """
        Check if a record with the key exists in the cache
        :param key: the key
        :return: True if the key exists in the cache. Otherwise, False is returned.
        """

        if (key is None) or (key not in self.__cache):
            return False

        return True
    # endregion