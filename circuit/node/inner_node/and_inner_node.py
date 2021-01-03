# Import
from circuit.node.node_abstract import NodeAbstract
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract

# Import exception
import exception.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class AndInnerNode(InnerNodeAbstract):
    """
    Circuit AND inner node representation
    """

    def __init__(self, child_set: set[NodeAbstract], id: int = 0):
        decomposable_temp = self.__is_decomposable_set(child_set)

        super().__init__(id, nt_enum.NodeTypeEnum.AND_NODE, child_set, decomposable=decomposable_temp)

    # region Private method
    @staticmethod
    def __is_decomposable_set(child_set: set[NodeAbstract]) -> bool:
        """
        Check if the node is decomposable
        :param child_set: the children set
        :return: True if the node is decomposable. Otherwise False is returned.
        """

        # The node has no children or one child
        if not len(child_set) or len(child_set) == 1:
            return True

        child_list = list(child_set)

        for i in range(0, len(child_list) - 1):
            for j in range(i+1, len(child_list)):
                intersection_temp = child_list[i]._get_variable_in_circuit_set().intersection(child_list[j]._get_variable_in_circuit_set())

                if len(intersection_temp):
                    return False

        return True
    # endregion

    # region Protected method
    def _is_decomposable(self) -> bool:
        """
        Check if the node is decomposable
        :return: True if the node is decomposable. Otherwise False is returned.
        """

        return self.__is_decomposable_set(self._child_set)
    # endregion

    # region Override method
    def _update_properties(self) -> None:
        self._set_decomposable(self._is_decomposable())

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

        result = True
        for child in self._child_set:
            result_temp = child.is_satisfiable(assumption_restriction_set_temp, exist_quantification_restriction_set_temp)
            # The child is not satisfied => this node is not satisfied
            if not result_temp:
                result = False
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

        number_of_models = 1
        for child in self._child_set:
            number_of_models *= child.model_counting(assumption_restriction_set_temp, exist_quantification_restriction_set_temp)

        # Cache
        if use_caches:
            self._add_model_counting_cache(key, number_of_models)

        return number_of_models

    def smooth(self, variable_need_to_be_added_set: set[int]) -> None:
        for child in self._child_set:
            child.smooth(variable_need_to_be_added_set)

        # Update the circuit properties etc.
        self._update()
    # endregion
