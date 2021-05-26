# Import
from abc import ABC, abstractmethod
from other.sorted_list import SortedList
from typing import Set, Dict, List, Union, TypeVar
from circuit.node.node_abstract import NodeAbstract
from circuit.node.leaf.leaf_abstract import LeafAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum

TInnerNodeAbstract = TypeVar("TInnerNodeAbstract", bound="InnerNodeAbstract")


class InnerNodeAbstract(NodeAbstract, ABC):
    """
    Circuit inner node representation
    """

    """
    Protected Set<NodeAbstract> child_set
    Protected Set<Leaf> leaf_set
    Protected Set<InnerNodeAbstract> parent_set
    Private Dict<NodeTypeEnum.value, int> node_type_in_circuit_counter_dict

    Private bool decomposable                   # The node satisfies decomposability
    Private bool decomposable_in_circuit        # All nodes in the circuit satisfy decomposability
    Private bool deterministic                  # The node satisfies determinism
    Private bool deterministic_in_circuit       # All nodes in the circuit satisfy determinism
    Private bool smoothness                     # The node satisfies smoothness
    Private bool smoothness_in_circuit          # All nodes in the circuit satisfy smoothness
    """

    def __init__(self, id: int, node_type: nt_enum.NodeTypeEnum, child_set: Set[NodeAbstract],
                 decomposable: bool = True, deterministic: bool = True, smoothness: bool = True):
        self._child_set: Set[NodeAbstract] = child_set
        self._parent_set: Set[TInnerNodeAbstract] = set()
        self.__node_type_in_circuit_counter_dict: Union[Dict[nt_enum.NodeTypeEnum.value, int], None] = None

        variable_in_circuit_set_temp, literal_in_circuit_set_temp = self._union_variable_and_literal_in_circuit_set_over_all_children()

        self._leaf_set: Set[LeafAbstract] = set()
        node_in_circuit_set_temp = {self}
        for child in child_set:
            node_in_circuit_set_temp = node_in_circuit_set_temp.union(child._get_node_in_circuit_set(copy=False))
            self._leaf_set.update(self.__get_leaf_set(child))
            child._add_parent(self)  # add me as a parent

        self.__decomposable = decomposable
        self.__deterministic = deterministic
        self.__smoothness = smoothness

        self.__decomposable_in_circuit = None
        self.__deterministic_in_circuit = None
        self.__smoothness_in_circuit = None
        self._check_properties_decomposable_deterministic_smoothness_in_circuit()

        super().__init__(id=id,
                         node_type=node_type,
                         variable_in_circuit_set=variable_in_circuit_set_temp,
                         literal_in_circuit_set=literal_in_circuit_set_temp,
                         node_in_circuit_set=node_in_circuit_set_temp)

        # Set the node_type_in_circuit_counter_dict
        self._set_node_type_in_circuit_counter_dict()

    # region Static method
    @staticmethod
    def __get_leaf_set(node: NodeAbstract) -> Set[LeafAbstract]:
        """
        Return a set of leaves in the circuit where the node is the root
        :param node: a node (the root of the circuit)
        :return: the set that contains all leaves
        """

        # The node is an inner node
        if isinstance(node, InnerNodeAbstract):
            return node._leaf_set
        # The node is a leaf
        elif isinstance(node, LeafAbstract):
            return {node}
        # The instance of the child is not handled
        else:
            assert False

    @staticmethod
    def _union_variable_and_literal_in_circuit_set_over_set(child_set: Set[NodeAbstract]) -> (Set[int], Set[int]):
        """
        Return a tuple of two sets, where the first set contains all variables that appear in the child_set and
        the second set contains all literals that appear in the child_set
        :param child_set: the children set
        :return: (variable_set, literal_set)
        """

        union_variable_set = set()
        union_literal_set = set()
        for child in child_set:
            union_variable_set = union_variable_set.union(child._get_variable_in_circuit_set(copy=False))
            union_literal_set = union_literal_set.union(child._get_literal_in_circuit_set(copy=False))

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
        Called when something changes in the circuit and properties (nodes in the circuit, ...) need to be recomputed.
        :param call_parent_update: True for calling the update functions of parents recursively
        :param smooth: True if the function is called because of smoothness
        :return: None
        :raises TryingUpdateCircuitWithMappingNodesException: if it is a mapping node and smooth=False
        """

        # Mapping node
        if (self.node_type == nt_enum.NodeTypeEnum.MAPPING_NODE) and not smooth:
            raise c_exception.TryingUpdateCircuitWithMappingNodesException()

        variable_in_circuit_set_temp, literal_in_circuit_set_temp = self._union_variable_and_literal_in_circuit_set_over_all_children()
        self._set_variable_in_circuit_set(variable_in_circuit_set_temp)
        self._set_literal_in_circuit_set(literal_in_circuit_set_temp)

        self._leaf_set: Set[LeafAbstract] = set()
        node_in_circuit_set_temp = {self}
        for child in self._child_set:
            node_in_circuit_set_temp = node_in_circuit_set_temp.union(child._get_node_in_circuit_set(copy=False))
            self._leaf_set.update(self.__get_leaf_set(child))
        self._set_node_in_circuit_set(node_in_circuit_set_temp)

        self._set_node_type_in_circuit_counter_dict()

        self._update_properties()
        self._check_properties_decomposable_deterministic_smoothness_in_circuit()

        # Notice my parents
        if call_parent_update:
            for parent in self._parent_set:
                parent._update(smooth=smooth)

        # Clear caches
        self._clear_caches()

    def _check_properties_decomposable_deterministic_smoothness_in_circuit(self) -> None:
        """
        Set decomposable_in_circuit, deterministic_in_circuit and smoothness_in_circuit based on the children
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

    def _set_node_type_in_circuit_counter_dict(self) -> None:
        """
        Set the node_type_in_circuit_counter_dict
        :return: None
        """

        self.__node_type_in_circuit_counter_dict = dict()

        for node in self._get_node_in_circuit_set(copy=False):
            key = node.node_type.value

            # The node type does not exist in the dictionary
            if key not in self.__node_type_in_circuit_counter_dict:
                self.__node_type_in_circuit_counter_dict[key] = 1
            # The node type exists in the dictionary
            else:
                self.__node_type_in_circuit_counter_dict[key] += 1

    def _get_node_type_in_circuit_counter_dict(self, copy: bool):
        """
        :param copy: True if a copy is returned
        :return: the node type counter
        """

        # The node_type_in_circuit_counter_dict is not initialized
        if self.__node_type_in_circuit_counter_dict is None:
            self._set_node_type_in_circuit_counter_dict()

        if copy:
            return self.__node_type_in_circuit_counter_dict.copy()

        return self.__node_type_in_circuit_counter_dict

    def _union_variable_and_literal_in_circuit_set_over_all_children(self) -> (Set[int], Set[int]):
        """
        Return a tuple of two sets, where the first set contains all variables in the circuit and
        the second set contains all literals in the circuit
        :return: (variable_set, literal_set)
        """

        return self._union_variable_and_literal_in_circuit_set_over_set(self._child_set)

    def _add_parent(self, new_parent: TInnerNodeAbstract) -> None:
        """
        Add the parent (new_parent) to the set of parents (parent_set).
        If the parent already exists in the set, nothing happens.
        :param new_parent: a new parent
        :return: None
        :raises CycleWasDetectedException: if a cycle was detected (the new parent is already in the circuit)
        """

        # The new parent already exists in the circuit
        if self._exist_node_in_circuit_set(new_parent):
            raise c_exception.CycleWasDetectedException()

        self._parent_set.add(new_parent)

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

    def _add_child(self, new_child: NodeAbstract, smooth: bool = False, call_update: bool = True) -> None:
        """
        Add the child (new_child) to the set of children (child_set).
        If the child already exists in the set, nothing happens.
        :param new_child: a new child
        :param smooth: True if the function is called because of smoothness
        :param call_update: True for calling the update function after this modification.
        If the parameter is set to False, then the circuit may be inconsistent after this modification.
        :return: None
        """

        # The child already exists
        if new_child in self._child_set:
            return

        self._child_set.add(new_child)

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
        """

        # The child does not exist
        if child_to_delete not in self._child_set:
            raise c_exception.ChildDoesNotExistException(str(self), str(child_to_delete))

        self._child_set.remove(child_to_delete)

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

    def _get_parent_set(self, copy: bool) -> Set[NodeAbstract]:
        """
        :param copy: True if a copy is returned
        :return: the set of parents
        """

        if copy:
            return self._parent_set.copy()

        return self._parent_set

    def _get_leaf_set(self, copy: bool) -> Set[NodeAbstract]:
        """
        :param copy: True if a copy is returned
        :return: the set of leaves
        """

        if copy:
            return self._leaf_set.copy()

        return self._leaf_set
    # endregion

    # region Public method
    def get_number_of_occurrences_node_type_in_circuit_counter_dict(self, node_type: nt_enum.NodeTypeEnum) -> int:
        """
        Return the number of occurrences of node_type in the circuit
        :param node_type: the node type
        :return: the number of occurrences
        """

        value = node_type.value
        node_type_in_circuit_counter_dict_temp = self._get_node_type_in_circuit_counter_dict(copy=False)

        # The node type value exists as a key in the dictionary
        if value in node_type_in_circuit_counter_dict_temp:
            return node_type_in_circuit_counter_dict_temp[value]
        # The node type value does NOT exist as a key in the dictionary
        else:
            return 0

    def get_child_id_list(self) -> List[int]:
        """
        Return a list that contains children's ID
        :return: a children's ID list
        """

        child_id_list = []

        for child in self._child_set:
            child_id_list.append(child.id)

        return child_id_list
    # endregion

    # region Override method
    def get_node_size(self) -> int:
        """
        :return: the size of the inner node (= number of children)
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
        string_temp = " ".join((string_temp, "Children list (IDs):"))
        child_id_sorted_list_temp = SortedList()
        for child in self._child_set:
            child_id_sorted_list_temp.add(child.id)
        string_temp = " ".join((string_temp, str(child_id_sorted_list_temp)))

        # The parent set
        string_temp = " ".join((string_temp, "Parent list (IDs):"))
        parent_id_sorted_list_temp = SortedList()
        for parent in self._parent_set:
            parent_id_sorted_list_temp.add(parent.id)
        string_temp = " ".join((string_temp, str(parent_id_sorted_list_temp)))

        # The node type counter
        string_temp = " ".join((string_temp, "The node types in the circuit:"))
        for nt in nt_enum.NodeTypeEnum:
            string_temp = " ".join((string_temp,
                                    f"{nt.name}: {self.get_number_of_occurrences_node_type_in_circuit_counter_dict(nt)} "))

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
