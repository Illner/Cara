# Import enum
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


class CycleWasDetectedException(CircuitException):
    """
    A cycle was detected
    """

    def __init__(self):
        self.message = "A cycle was detected!"
        super().__init__(self.message)
