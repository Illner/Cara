# Import
from typing import Set, Dict

# Import exception
from exception.cara_exception import CaraException


class CircuitException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class ParentDoesNotExistException(CircuitException):
    """
    The node does not have the parent in its set of parents
    """

    def __init__(self, node: str, parent: str):
        self.message = f"The node ({node}) does not have the parent ({parent}) in its set of parents!"
        super().__init__(self.message)


class ChildDoesNotExistException(CircuitException):
    """
    The node does not have the child in its list of children
    """

    def __init__(self, node: str, child: str):
        self.message = f"The node ({node}) does not have the child ({child}) in its list of children!"
        super().__init__(self.message)


class CircuitIsNotDecomposableException(CircuitException):
    """
    The circuit is not decomposable
    """

    def __init__(self, message_extension: str = ""):
        self.message = f"The circuit is not decomposable! {message_extension}"
        super().__init__(self.message)


class CircuitIsNotDeterministicException(CircuitException):
    """
    The circuit is not deterministic
    """

    def __init__(self, message_extension: str = ""):
        self.message = f"The circuit is not deterministic! {message_extension}"
        super().__init__(self.message)


class CircuitIsNotSmoothException(CircuitException):
    """
    The circuit is not smooth
    """

    def __init__(self, message_extension: str = ""):
        self.message = f"The circuit is not smooth! {message_extension}"
        super().__init__(self.message)


class CycleWasDetectedException(CircuitException):
    """
    A cycle was detected
    """

    def __init__(self):
        self.message = "A cycle was detected!"
        super().__init__(self.message)


class InvalidDimacsNnfFormatException(CircuitException):
    """
    Invalid DIMACS NNF format
    """

    def __init__(self, message_extension: str = "no detailed information is given"):
        self.message = f"DIMACS NNF format is invalid in the file! ({message_extension})"
        super().__init__(self.message)


class NLineIsNotMentionedException(CircuitException):
    """
    N line is not mentioned at all or is mentioned after the nodes
    """

    def __init__(self):
        self.message = "NNF line is not mentioned at all or is mentioned after the nodes!"
        super().__init__(self.message)


class NodeWithSameIDAlreadyExistsInCircuitException(CircuitException):
    """
    A node with the same ID already exists in the circuit
    """

    def __init__(self, node_to_add: str):
        self.message = f"The node ({node_to_add}) cannot be added to the circuit because a node with the same ID already exists there!"
        super().__init__(self.message)


class NodeWithIDDoesNotExistInCircuitException(CircuitException):
    """
    The node with the ID does not exist in the circuit
    """

    def __init__(self, node: str, message_extension: str = "no detailed information is given"):
        self.message = f"The node ({node}) does not exist in the circuit! ({message_extension})"
        super().__init__(self.message)


class SomethingWrongException(CircuitException):
    """
    Something wrong
    """

    def __init__(self, message_extension: str = ""):
        self.message = "Something wrong"
        if message_extension:
            self.message += f" ({message_extension})"
        super().__init__(self.message)


class VariableDoesNotExistInCircuitException(CircuitException):
    """
    The variable does not exist in the circuit
    """

    def __init__(self, variable: int, root_node: str):
        self.message = f"The variable ({str(variable)}) does not occur in the circuit ({root_node})!"
        super().__init__(self.message)


class RootOfCircuitIsNotSetException(CircuitException):
    """
    The root of the circuit is not set
    """

    def __init__(self):
        self.message = "The root of the circuit is not set!"
        super().__init__(self.message)


class AssumptionSetAndExistentialQuantificationSetAreNotDisjointException(CircuitException):
    """
    The assumption set and existential quantification set are not disjoint.
    It can be used for an observation set and default set as well (assumption_and_exist_set = False).
    """

    def __init__(self, variable_union_set: Set[int], assumption_and_exist_set: bool = True):
        assumption_set_name_temp = "assumption set" if assumption_and_exist_set else "observation set"
        exist_quantification_set_name_temp = "existential quantification set" if assumption_and_exist_set else "default set"

        self.message = f"The {assumption_set_name_temp} and {exist_quantification_set_name_temp} are not disjoint ({variable_union_set})!"
        super().__init__(self.message)


class AssumptionSetContainsComplementLiteralsException(CircuitException):
    """
    The assumption set contains complement literals.
    It can be used for an observation set as well (assumption_set = False).
    """

    def __init__(self, complement_literals_set: Set[int], assumption_set: bool = True):
        assumption_set_name_temp = "assumption set" if assumption_set else "observation set"

        self.message = f"The {assumption_set_name_temp} contains complement literals ({complement_literals_set})!"
        super().__init__(self.message)


class SetContainsLiteralsButOnlyVariablesAreAllowedException(CircuitException):
    """
    The set contains literals, but only variables are allowed
    """

    def __init__(self, set_name: str, variable_set: Set[int]):
        self.message = f"The set ({set_name}) contains literals, but only variables are allowed ({variable_set}!)"
        super().__init__(self.message)


class OperationIsNotSupportedException(CircuitException):
    """
    The operation is not supported
    """

    def __init__(self, operation_name: str):
        self.message = f"The operation ({operation_name}) is not supported for this type of circuit!"
        super().__init__(self.message)


class TryingUpdateCircuitWithMappingNodesException(CircuitException):
    """
    Trying to update the circuit that contains mapping nodes
    """

    def __init__(self):
        self.message = "Trying to update the circuit that contains mapping nodes!"
        super().__init__(self.message)


class MappingIsIncompleteException(CircuitException):
    """
    The mapping is incomplete
    """

    def __init__(self, mapping_dictionary: Dict[int, int], variable_or_literal_in_circuit: Set[int]):
        self.message = f"The mapping ({mapping_dictionary}) is incomplete in the sub-circuit ({variable_or_literal_in_circuit})!"
        super().__init__(self.message)
