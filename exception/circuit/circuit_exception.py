# Import enum
from typing import Set
import circuit.node.node_type_enum as nt_enum


class CircuitException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SizeCannotBeLessThanZeroException(CircuitException):
    """
    The size of the circuit cannot be less than 0
    """

    def __init__(self, node: str):
        self.message = f"The size of the circuit ({node}) cannot be less than 0!"
        super().__init__(self.message)


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


class NumberOfNodeTypeOccurrencesCannotBeLessThanZeroException(CircuitException):
    """
    The number of node type occurrences cannot be less than 0
    """

    def __init__(self, node_type: nt_enum.NodeTypeEnum, node: str):
        self.message = f"The number of node type ({node_type.value}) occurrences cannot be less than 0! Node: ({node})"
        super().__init__(self.message)


class TryingRemoveNodeTypeDoesNotHaveOccurrenceException(CircuitException):
    """
    Trying to remove an occurrence of the node type which does not have any occurrence in the circuit
    """

    def __init__(self, node_type: nt_enum.NodeTypeEnum, node: str):
        self.message = f"Trying to remove an occurrence of the node type ({node_type.value}) which does not have any occurrence in the circuit! Node: ({node})"
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
    Can be used for an observation set and default set as well (assumption_and_exist_set = False).
    """

    def __init__(self, variable_union_set: Set[int], assumption_and_exist_set: bool = True):
        assumption_set_name_temp = "assumption set" if assumption_and_exist_set else "observation set"
        exist_quantification_set_name_temp = "existential quantification set" if assumption_and_exist_set else "default set"

        self.message = f"The {assumption_set_name_temp} and {exist_quantification_set_name_temp} are not disjoint ({variable_union_set})!"
        super().__init__(self.message)


class AssumptionSetContainsComplementLiteralsException(CircuitException):
    """
    The assumption set contains complement literals.
    Can be used for an observation set as well (assumption_set = False).
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
