class HypergraphException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SomethingWrongException(HypergraphException):
    """
    Something wrong
    """

    def __init__(self, message_extension: str = ""):
        self.message = "Something wrong"
        if message_extension:
            self.message += f" ({message_extension})"
        super().__init__(self.message)


class FileIsMissingException(HypergraphException):
    """
    The file is missing
    """

    def __init__(self, file_path: str):
        self.message = f"The file ({file_path}) is missing!"
        super().__init__(self.message)


class SoftwareIsNotSupportedOnSystemException(HypergraphException):
    """
    The software is not supported on the system
    """

    def __init__(self, software_name: str):
        self.message = f"The software ({software_name}) is not supported on the system!"
        super().__init__(self.message)


class NodeDoesNotExistException(HypergraphException):
    """
    The node does not exist in the hypergraph
    """

    def __init__(self, node_id: int):
        self.message = f"The node ({str(node_id)}) does not exist in the hypergraph!"
        super().__init__(self.message)


class HyperedgeDoesNotExistException(HypergraphException):
    """
    The hyperedge does not exist in the hypergraph
    """

    def __init__(self, hyperedge_id: int):
        self.message = f"The hyperedge ({hyperedge_id}) does not exist in the hypergraph!"
        super().__init__(self.message)


class InvalidUBfactorException(HypergraphException):
    """
    Invalid UBfactor
    """

    def __init__(self, ub_factor: float):
        self.message = f"The UBfactor ({ub_factor}) has to be a real number between 0.01 (1%) and 0.49 (49%)!"
        super().__init__(self.message)
