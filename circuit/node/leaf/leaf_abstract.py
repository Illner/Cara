# Import
from abc import ABC
from circuit.node.node_abstract import NodeAbstract
from other.sorted_list import SortedList

# Import exception
import exception.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class LeafAbstract(NodeAbstract, ABC):
    """
    Circuit leaf representation
    """

    """
    Private Set<InnerNodeAbstract> parent_set
    """

    def __init__(self, id: int, node_type: nt_enum.NodeTypeEnum,
                 variable_in_circuit_set: set[int], literal_in_circuit_set: set[int], size: int = 0):
        self.__parent_set: set[NodeAbstract] = set()
        super().__init__(id, node_type, variable_in_circuit_set, literal_in_circuit_set, {self}, size)

    # region Protected method
    def _add_parent(self, new_parent: NodeAbstract) -> None:
        """
        Add the parent (new_parent) to the set of parents (parent_set).
        If the parent already exists in the set, nothing happens.
        :param new_parent: the new parent
        """

        self.__parent_set.add(new_parent)

    def _remove_parent(self, parent_to_delete: NodeAbstract) -> None:
        """
        Remove the parent (parent_to_delete) from the set of parents (parent_set).
        If the parent does not exist in the set, raise an exception (ParentDoesNotExistException).
        :param parent_to_delete: the parent
        """

        # The parent does not exist in the set
        if parent_to_delete not in self.__parent_set:
            raise c_exception.ParentDoesNotExistException(str(self), str(parent_to_delete))

        self.__parent_set.remove(parent_to_delete)
    # endregion

    # region Override method
    def number_of_children(self):
        """
        Ballast method (NodeAbstract._update_size_based_on_children).
        Return a number of children.
        :return: 0 because lists don't have any children
        """

        return 0
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
