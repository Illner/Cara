# Import exception
from exception.cara_exception import CaraException


class HypergraphPartitioningException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class SomethingWrongException(HypergraphPartitioningException):
    """
    Something wrong
    """

    def __init__(self, message_extension: str = ""):
        self.message = "Something wrong"
        if message_extension:
            self.message += f" ({message_extension})"
        super().__init__(self.message)


class FileIsMissingException(HypergraphPartitioningException):
    """
    The file is missing
    """

    def __init__(self, file_path: str):
        self.message = f"The file ({file_path}) is missing!"
        super().__init__(self.message)


class SoftwareIsNotSupportedOnSystemException(HypergraphPartitioningException):
    """
    The software is not supported on the system
    """

    def __init__(self, software_name: str):
        self.message = f"The software ({software_name}) is not supported on the system!"
        super().__init__(self.message)


class NodeDoesNotExistException(HypergraphPartitioningException):
    """
    The node does not exist in the hypergraph
    """

    def __init__(self, node_id: int):
        self.message = f"The node ({str(node_id)}) does not exist in the hypergraph!"
        super().__init__(self.message)


class HyperedgeDoesNotExistException(HypergraphPartitioningException):
    """
    The hyperedge does not exist in the hypergraph
    """

    def __init__(self, hyperedge_id: int):
        self.message = f"The hyperedge ({hyperedge_id}) does not exist in the hypergraph!"
        super().__init__(self.message)


class InvalidUBfactorException(HypergraphPartitioningException):
    """
    Invalid UB factor
    """

    def __init__(self, ub_factor: float):
        self.message = f"The UB factor ({ub_factor}) has to be a real number between 0.01 (1%) and 0.49 (49%)!"
        super().__init__(self.message)


class InvalidLimitCacheException(HypergraphPartitioningException):
    """
    Invalid limits for caching
    """

    def __init__(self, lower_bound: int, upper_bound: int, type_of_limit: str):
        self.message = f"Invalid lower bound ({lower_bound}) and upper bound ({upper_bound}) for {type_of_limit}!"
        super().__init__(self.message)
