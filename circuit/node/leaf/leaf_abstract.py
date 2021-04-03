# Import
from abc import ABC
from typing import Set
from other.sorted_list import SortedList
from circuit.node.node_abstract import NodeAbstract

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
        self.__parent_set: Set[NodeAbstract] = set()
        self.__size: int = size
        super().__init__(id=id,
                         node_type=node_type,
                         variable_in_circuit_set=variable_in_circuit_set,
                         literal_in_circuit_set=literal_in_circuit_set,
                         node_in_circuit_set={self})

    # region Protected method
    def _add_parent(self, new_parent: NodeAbstract) -> None:
        """
        Add the parent (new_parent) to the set of parents (parent_set).
        If the parent already exists in the set, nothing happens.
        :param new_parent: a new parent
        :return: None
        """

        self.__parent_set.add(new_parent)

    def _remove_parent(self, parent_to_delete: NodeAbstract) -> None:
        """
        Remove the parent (parent_to_delete) from the set of parents (parent_set)
        :param parent_to_delete: the parent
        :return: None
        :raises ParentDoesNotExistException: if the parent does not exist in the set
        """

        # The parent does not exist in the set
        if parent_to_delete not in self.__parent_set:
            raise c_exception.ParentDoesNotExistException(str(self), str(parent_to_delete))

        self.__parent_set.remove(parent_to_delete)

    def _set_size(self, new_size: int) -> None:
        """
        Setter - the size
        :return: None
        """

        self.__size = new_size

    def _get_parent_set(self, copy: bool) -> Set[NodeAbstract]:
        """
        :param copy: True if a copy is returned
        :return: the parent set
        """

        if copy:
            return self.__parent_set.copy()

        return self.__parent_set
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

        # Parents
        string_temp = " ".join((string_temp, "Parent list (IDs):"))
        parent_id_sorted_list_temp = SortedList()
        for parent in self.__parent_set:
            parent_id_sorted_list_temp.add(parent.id)
        string_temp = " ".join((string_temp, str(parent_id_sorted_list_temp)))

        return string_temp
    # endregion
