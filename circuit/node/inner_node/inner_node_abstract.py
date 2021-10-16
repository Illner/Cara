# Import
from abc import ABC, abstractmethod
from other.sorted_list import SortedList
from typing import Set, Dict, Union, TypeVar
from circuit.node.node_abstract import NodeAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum

# Type
TInnerNodeAbstract = TypeVar("TInnerNodeAbstract", bound="InnerNodeAbstract")


class InnerNodeAbstract(NodeAbstract, ABC):
    """
    Circuit inner node representation
    """

    """
    Protected Set<int> child_id_set
    Protected Set<int> parent_id_set
    Protected Set<NodeAbstract> child_set
    Protected Set<InnerNodeAbstract> parent_set
    Private Dict<int, int> mapping_id_variable_id_dictionary

    Private bool decomposable                   # The node satisfies decomposability
    Private bool decomposable_in_circuit        # All nodes in the circuit satisfy decomposability
    Private bool deterministic                  # The node satisfies determinism
    Private bool deterministic_in_circuit       # All nodes in the circuit satisfy determinism
    Private bool smoothness                     # The node satisfies smoothness
    Private bool smoothness_in_circuit          # All nodes in the circuit satisfy smoothness
    """

    def __init__(self, id: int, node_type: nt_enum.NodeTypeEnum, child_set: Set[NodeAbstract],
                 decomposable: bool = True, deterministic: bool = True, smoothness: bool = True,
                 mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None):
        self._child_id_set: Set[int] = set()
        self._parent_id_set: Set[int] = set()
        self._child_set: Set[NodeAbstract] = child_set
        self._parent_set: Set[TInnerNodeAbstract] = set()
        self.__mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = mapping_id_variable_id_dictionary

        variable_in_circuit_set_temp, literal_in_circuit_set_temp = self._union_variable_and_literal_in_circuit_set_over_all_children()

        self.__decomposable = decomposable
        self.__deterministic = deterministic
        self.__smoothness = smoothness

        # Initialization
        self.__decomposable_in_circuit = None
        self.__deterministic_in_circuit = None
        self.__smoothness_in_circuit = None
        self._check_properties_decomposable_deterministic_smoothness_in_circuit()

        super().__init__(id=id,
                         node_type=node_type,
                         variable_in_circuit_set=variable_in_circuit_set_temp,
                         literal_in_circuit_set=literal_in_circuit_set_temp)

        for child in child_set:
            child._add_parent(self)     # add me as a parent
            self._child_id_set.add(child.id)

    # region Static method
    @staticmethod
    def _union_variable_and_literal_in_circuit_set_over_set(child_set: Set[NodeAbstract]) -> (Set[int], Set[int]):
        """
        Return a tuple of two sets, where the first set contains all variables that appear in the child_set and
        the second set contains all literals that appear in the child_set
        :param child_set: children set
        :return: (variable_set, literal_set)
        """

        union_variable_set = set()
        union_literal_set = set()

        for child in child_set:
            union_variable_set = union_variable_set.union(child._variable_in_circuit_set)
            union_literal_set = union_literal_set.union(child._literal_in_circuit_set)

        return union_variable_set, union_literal_set
    # endregion

    # region Abstract method
    @abstractmethod
    def _update_properties(self) -> None:
        pass
    # endregion

    # region Protected method
    def _update(self, call_parent_update: bool = True, smooth: bool = False) -> None:
        """
        Update the properties of the circuit.
        Called when something changes in the circuit and properties (variable in circuit set, ...) need to be recomputed.
        :param call_parent_update: True for calling the update functions of parents recursively
        :param smooth: True if the function is called because of smoothness
        :return: None
        :raises TryingUpdateCircuitWithMappingNodesException: if this is a mapping node and smooth=False
        """

        # Mapping node
        if (self.node_type == nt_enum.NodeTypeEnum.MAPPING_NODE) and not smooth:
            raise c_exception.TryingUpdateCircuitWithMappingNodesException()

        variable_in_circuit_set_temp, literal_in_circuit_set_temp = self._union_variable_and_literal_in_circuit_set_over_all_children()
        self._set_variable_in_circuit_set(variable_in_circuit_set_temp)
        self._set_literal_in_circuit_set(literal_in_circuit_set_temp)

        self._update_properties()
        self._check_properties_decomposable_deterministic_smoothness_in_circuit()

        # Notice my parents
        if call_parent_update:
            for parent in self._parent_set:
                parent._update(call_parent_update=call_parent_update,   # always True
                               smooth=smooth)

        # Clear caches
        self._clear_caches()

    def _check_properties_decomposable_deterministic_smoothness_in_circuit(self) -> None:
        """
        Set decomposable_in_circuit, deterministic_in_circuit and smoothness_in_circuit based on the children set
        :return: None
        """

        # Check decomposable_in_circuit
        self.__decomposable_in_circuit = self.__decomposable
        for child in self._child_set:
            if isinstance(child, InnerNodeAbstract) and not child.decomposable_in_circuit:
                self.__decomposable_in_circuit = False

            if not self.__decomposable_in_circuit:
                break

        # Check deterministic_in_circuit
        self.__deterministic_in_circuit = self.__deterministic
        for child in self._child_set:
            if isinstance(child, InnerNodeAbstract) and not child.deterministic_in_circuit:
                self.__deterministic_in_circuit = False

            if not self.__deterministic_in_circuit:
                break

        # Check smoothness_in_circuit
        self.__smoothness_in_circuit = self.__smoothness
        for child in self._child_set:
            if isinstance(child, InnerNodeAbstract) and not child.smoothness_in_circuit:
                self.__smoothness_in_circuit = False

            if not self.__smoothness_in_circuit:
                break

    def _set_decomposable(self, new_decomposable_value: bool) -> None:
        """
        Set the decomposable property.
        In case the decomposable property is False, change the decomposable_in_circuit property to False as well.
        :param new_decomposable_value: a new value of the decomposable property
        :return: None
        """

        self.__decomposable = new_decomposable_value

        # Update the decomposable_in_circuit property
        if not new_decomposable_value:
            self.__decomposable_in_circuit = False

    def _set_deterministic(self, new_deterministic_value: bool) -> None:
        """
        Set the deterministic property.
        In case the deterministic property is False, change the deterministic_in_circuit property to False as well.
        :param new_deterministic_value: a new value of the deterministic property
        :return: None
        """

        self.__deterministic = new_deterministic_value

        # Update the deterministic_in_circuit property
        if not new_deterministic_value:
            self.__deterministic_in_circuit = False

    def _set_smoothness(self, new_smoothness_value: bool) -> None:
        """
        Set the smoothness property.
        In case the smoothness property is False, change the smoothness_in_circuit property to False as well.
        :param new_smoothness_value: a new value of the smoothness property
        :return: None
        """

        self.__smoothness = new_smoothness_value

        # Update the smoothness_in_circuit property
        if not new_smoothness_value:
            self.__smoothness_in_circuit = False

    def _union_variable_and_literal_in_circuit_set_over_all_children(self) -> (Set[int], Set[int]):
        """
        Return a tuple of two sets, where the first set contains all variables in the circuit and
        the second set contains all literals in the circuit
        :return: (variable_set, literal_set)
        """

        variable_in_circuit_set_temp, literal_in_circuit_set_temp = InnerNodeAbstract._union_variable_and_literal_in_circuit_set_over_set(self._child_set)

        # Mapping is used
        if self.__mapping_id_variable_id_dictionary is not None:
            variable_in_circuit_set_temp = NodeAbstract.use_mapping_on_variable_set(variable_set=variable_in_circuit_set_temp,
                                                                                    mapping_dictionary=self.__mapping_id_variable_id_dictionary)
            literal_in_circuit_set_temp = NodeAbstract.use_mapping_on_literal_set(literal_set=literal_in_circuit_set_temp,
                                                                                  mapping_dictionary=self.__mapping_id_variable_id_dictionary)

        return variable_in_circuit_set_temp, literal_in_circuit_set_temp

    def _add_parent(self, new_parent: TInnerNodeAbstract) -> None:
        """
        Add the parent (new_parent) to the set of parents (parent_set).
        If the parent already exists in the set, nothing happens.
        :param new_parent: a new parent
        :return: None
        """

        self._parent_set.add(new_parent)
        self._parent_id_set.add(new_parent.id)

    def _remove_parent(self, parent_to_delete: TInnerNodeAbstract) -> None:
        """
        Remove the parent (parent_to_delete) from the set of parents (parent_set).
        :param parent_to_delete: a parent
        :return: None
        :raises ParentDoesNotExistException: if the parent does not exist in the set
        """

        # The parent does not exist in the set
        if parent_to_delete not in self._parent_set:
            raise c_exception.ParentDoesNotExistException(str(self), str(parent_to_delete))

        self._parent_set.remove(parent_to_delete)
        self._parent_id_set.remove(parent_to_delete.id)

    def _get_parent_set(self, copy: bool) -> Set[TInnerNodeAbstract]:
        """
        :param copy: True if a copy is returned
        :return: the set of parents
        """

        if copy:
            return self._parent_set.copy()

        return self._parent_set

    def _get_parent_id_set(self, copy: bool) -> Set[int]:
        """
        :param copy: True if a copy is returned
        :return: the set of parents' id
        """

        if copy:
            return self._parent_id_set.copy()

        return self._parent_id_set

    def _add_child(self, new_child: NodeAbstract, smooth: bool = False, call_update: bool = True) -> None:
        """
        Add the child (new_child) to the set of children (child_set).
        If the child already exists in the set, nothing happens.
        :param new_child: a new child
        :param smooth: True if the function is called because of smoothness
        :param call_update: True for calling the update function after this modification.
        If the parameter is set to False, then the circuit may be inconsistent after this modification.
        :return: None
        :raises TryingUpdateCircuitWithMappingNodesException: if this is a mapping node
        """

        # Mapping node
        if self.node_type == nt_enum.NodeTypeEnum.MAPPING_NODE:
            raise c_exception.TryingUpdateCircuitWithMappingNodesException()

        # The child already exists
        if new_child in self._child_set:
            return

        self._child_set.add(new_child)
        self._child_id_set.add(new_child.id)

        if call_update:
            self._update(smooth=smooth)

    def _remove_child(self, child_to_delete: NodeAbstract, smooth: bool = False, call_update: bool = True) -> None:
        """
        Remove the child (child_to_delete) from the set of children (child_set)
        :param child_to_delete: a child
        :param smooth: True if the function is called because of smoothness
        :param call_update: True for calling the update function after this modification.
        If the parameter is set to False, then the circuit may be inconsistent after this modification.
        :return: None
        :raises ChildDoesNotExistException: if the child does not exist in the set
        :raises TryingUpdateCircuitWithMappingNodesException: if this is a mapping node
        """

        # The child does not exist
        if child_to_delete not in self._child_set:
            raise c_exception.ChildDoesNotExistException(str(self), str(child_to_delete))

        # Mapping node
        if self.node_type == nt_enum.NodeTypeEnum.MAPPING_NODE:
            raise c_exception.TryingUpdateCircuitWithMappingNodesException()

        self._child_set.remove(child_to_delete)
        self._child_id_set.remove(child_to_delete.id)

        if call_update:
            self._update(smooth=smooth)

    def _get_child_set(self, copy: bool) -> Set[NodeAbstract]:
        """
        :param copy: True if a copy is returned
        :return: the set of children
        """

        if copy:
            return self._child_set.copy()

        return self._child_set

    def _get_child_id_set(self, copy: bool) -> Set[int]:
        """
        :param copy: True if a copy is returned
        :return: the set of children's id
        """

        if copy:
            return self._child_id_set.copy()

        return self._child_id_set
    # endregion

    # region Override method
    def get_node_size(self) -> int:
        """
        :return: the size of the inner node (= number of children)
        """

        return len(self._child_set)

    def get_number_of_children(self) -> int:
        """
        :return: the number of children
        """

        return len(self._child_set)
    # endregion

    # region Magic method
    def __repr__(self):
        string_temp = super().__repr__()

        string_temp = " ".join((string_temp,
                                f"Decomposable: {self.__decomposable}",
                                f"Decomposable_in_circuit: {self.__decomposable_in_circuit}",
                                f"Deterministic: {self.__deterministic}",
                                f"Deterministic_in_circuit: {self.__deterministic_in_circuit}",
                                f"Smoothness: {self.__smoothness}",
                                f"Smoothness_in_circuit: {self.__smoothness_in_circuit}"))

        # The children set
        child_id_sorted_list_temp = SortedList(self._child_id_set)
        string_temp = " ".join((string_temp, "Children list (IDs):", str(child_id_sorted_list_temp)))

        # The parent set
        parent_id_sorted_list_temp = SortedList(self._parent_id_set)
        string_temp = " ".join((string_temp, "Parent list (IDs):", str(parent_id_sorted_list_temp)))

        return string_temp
    # endregion

    # region Property
    @property
    def decomposable(self) -> bool:
        return self.__decomposable

    @property
    def decomposable_in_circuit(self) -> bool:
        return self.__decomposable_in_circuit

    @property
    def deterministic(self) -> bool:
        return self.__deterministic

    @property
    def deterministic_in_circuit(self) -> bool:
        return self.__deterministic_in_circuit

    @property
    def smoothness(self) -> bool:
        return self.__smoothness

    @property
    def smoothness_in_circuit(self) -> bool:
        return self.__smoothness_in_circuit
    # endregion
