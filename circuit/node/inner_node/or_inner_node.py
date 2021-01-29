# Import
import warnings
from typing import Union
from circuit.node.node_abstract import NodeAbstract
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract

# Import
import exception.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class OrInnerNode(InnerNodeAbstract):
    """
    Circuit OR inner node representation
    """

    """
    private int decision_variable
    """

    def __init__(self, child_set: set[NodeAbstract], id: int = 0,
                 decision_variable: Union[int, None] = None):
        if decision_variable is None:
            deterministic_temp = self.__is_deterministic_set(child_set)
        else:
            deterministic_temp = True

        smooth_temp = self.__is_smooth_set(child_set)

        super().__init__(id, nt_enum.NodeTypeEnum.OR_NODE, child_set, deterministic=deterministic_temp, smoothness=smooth_temp)

        # Check if the decision variable does not exist in the circuit
        if (decision_variable is not None) and (not self._exist_variable_in_circuit_set(decision_variable)):
            raise c_exception.VariableDoesNotExistInCircuitException(decision_variable, str(self))
        self.__decision_variable = decision_variable

    # region Static method
    @staticmethod
    def __is_deterministic_set(child_set: set[NodeAbstract]) -> bool:
        """
        Check if the node is deterministic
        :param child_set: the children set
        :return: True if the node is deterministic. Otherwise False is returned.
        """

        # The node has no children or one child
        if not len(child_set) or len(child_set) == 1:
            return True

        warnings.warn("Warning: __is_deterministic_set is not implemented. Deterministic was set to True!")
        return True

    @staticmethod
    def __is_smooth_set(child_set: set[NodeAbstract]) -> bool:
        """
        Check if the node is smooth
        :param child_set: the children set
        :return: True if the node is smooth. Otherwise False is returned.
        """

        # The node has no children or one child
        if not len(child_set) or len(child_set) == 1:
            return True

        union_variable_set_temp = set()
        for child in child_set:
            union_variable_set_temp = union_variable_set_temp.union(child._get_variable_in_circuit_set())

        for child in child_set:
            if len(union_variable_set_temp) != len(child._get_variable_in_circuit_set()):
                return False

        return True
    # endregion

    # region Protected method
    def _is_smooth(self) -> bool:
        """
        Check if the node is smooth
        :return: True if the node is smooth. Otherwise False is returned.
        """

        return self.__is_smooth_set(self._child_set)

    def _is_deterministic(self) -> bool:
        """
        Check if the node is deterministic
        :return: True if the node is deterministic. Otherwise False is returned.
        """

        return self.__is_deterministic_set(self._child_set)
    # endregion

    # region Override method
    def _update_properties(self) -> None:
        self._set_deterministic(self._is_deterministic())
        self._set_smoothness(self._is_smooth())

    def is_satisfiable(self, assumption_set: set[int], exist_quantification_set: set[int], use_caches: bool = True) -> bool:
        # The circuit is not decomposable
        if not self.decomposable_in_circuit:
            raise c_exception.CircuitIsNotDecomposableException("Satisfiability is not supported if the circuit is not decomposable.")

        assumption_restriction_set_temp = set(filter(lambda l: self._exist_variable_in_circuit_set(abs(l)), assumption_set))
        exist_quantification_restriction_set_temp = exist_quantification_set.intersection(self._get_variable_in_circuit_set())

        # Cache
        key = ""    # initialization
        if use_caches:
            key = self._generate_key_cache(assumption_restriction_set_temp, exist_quantification_restriction_set_temp)
            value = self._get_satisfiable_cache(key)
            if value is not None:
                return value

        result = False
        for child in self._child_set:
            result_temp = child.is_satisfiable(assumption_restriction_set_temp, exist_quantification_restriction_set_temp)
            # The child is satisfied => this node is satisfied
            if result_temp:
                result = True
                break

        # Cache
        if use_caches:
            self._add_satisfiable_cache(key, result)

        return result

    def model_counting(self, assumption_set: set[int], exist_quantification_set: set[int], use_caches: bool = True) -> int:
        # The circuit is not decomposable
        if not self.decomposable_in_circuit:
            raise c_exception.CircuitIsNotDecomposableException("Model counting is not supported if the circuit is not decomposable.")

        # The circuit is not deterministic
        if not self.deterministic_in_circuit:
            raise c_exception.CircuitIsNotDeterministicException("Model counting is not supported if the circuit is not deterministic.")

        # The circuit is not smooth
        if not self.smoothness_in_circuit:
            for child in self._child_set:
                child.smooth(set())

        assumption_restriction_set_temp = assumption_set.intersection(self._get_variable_in_circuit_set())
        exist_quantification_restriction_set_temp = exist_quantification_set.intersection(self._get_variable_in_circuit_set())

        # Cache
        key = ""    # initialization
        if use_caches:
            key = self._generate_key_cache(assumption_restriction_set_temp, exist_quantification_restriction_set_temp)
            value = self._get_model_counting_cache(key)
            if value is not None:
                return value

        number_of_models = 0
        for child in self._child_set:
            number_of_models += child.model_counting(assumption_restriction_set_temp, exist_quantification_restriction_set_temp)

        # Cache
        if use_caches:
            self._add_model_counting_cache(key, number_of_models)

        return number_of_models

    def smooth(self, variable_need_to_be_added_set: set[int]) -> None:
        # The circuit is smooth, and no variable needs to be added.
        if not len(variable_need_to_be_added_set) and self.smoothness_in_circuit:
            return

        union_variable_set = variable_need_to_be_added_set.union(self._get_variable_in_circuit_set())
        for child in self._child_set:
            child.smooth(union_variable_set.difference(child._get_variable_in_circuit_set()))

        # Update the circuit properties etc.
        self._update()
    # endregion

    # region Property
    @property
    def decision_variable(self):
        return self.__decision_variable
    # endregion
