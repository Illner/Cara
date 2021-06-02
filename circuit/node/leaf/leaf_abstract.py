# Import
from abc import ABC
from typing import Set, List
from other.sorted_list import SortedList
from circuit.node.node_abstract import NodeAbstract
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class LeafAbstract(NodeAbstract, ABC):
    """
    Circuit leaf representation
    """

    """
    Private int size                            # the size of the leaf
    Private Set<InnerNodeAbstract> parent_set
    """

    def __init__(self, id: int, node_type: nt_enum.NodeTypeEnum,
                 variable_in_circuit_set: Set[int], literal_in_circuit_set: Set[int], size: int = 0):
        self.__parent_set: Set[InnerNodeAbstract] = set()
        self.__size: int = size

        super().__init__(id=id,
                         node_type=node_type,
                         variable_in_circuit_set=variable_in_circuit_set,
                         literal_in_circuit_set=literal_in_circuit_set)

    # region Protected method
    def _add_parent(self, new_parent: InnerNodeAbstract) -> None:
        """
        Add the parent (new_parent) to the set of parents (parent_set).
        If the parent already exists in the set, nothing happens.
        :param new_parent: a new parent
        :return: None
        """

        self.__parent_set.add(new_parent)

    def _remove_parent(self, parent_to_delete: InnerNodeAbstract) -> None:
        """
        Remove the parent (parent_to_delete) from the set of parents (parent_set)
        :param parent_to_delete: a parent
        :return: None
        :raises ParentDoesNotExistException: if the parent does not exist in the set
        """

        # The parent does not exist in the set
        if parent_to_delete not in self.__parent_set:
            raise c_exception.ParentDoesNotExistException(str(self), str(parent_to_delete))

        self.__parent_set.remove(parent_to_delete)

    def _get_parent_set(self, copy: bool) -> Set[InnerNodeAbstract]:
        """
        :param copy: True if a copy is returned
        :return: the parent set
        """

        if copy:
            return self.__parent_set.copy()

        return self.__parent_set

    def _set_size(self, new_size: int) -> None:
        """
        Setter - size
        :return: None
        """

        self.__size = new_size
    # endregion

    # region Public method
    def get_parent_id_list(self) -> List[int]:
        """
        Return a list that contains parent's ID
        :return: a parent's ID list
        """

        parent_id_list = []

        for parent in self._get_parent_set(copy=False):
            parent_id_list.append(parent.id)

        return parent_id_list
    # endregion

    # region Override method
    def get_node_size(self) -> int:
        """
        :return: the size of the leaf
        """

        return self.__size
    # endregion

    # region Magic method
    def __repr__(self):
        string_temp = super().__repr__()

        # The parent set
        parent_id_sorted_list_temp = SortedList(self.get_parent_id_list())
        string_temp = " ".join((string_temp, "Parent list (IDs):", str(parent_id_sorted_list_temp)))

        return string_temp
    # endregion
