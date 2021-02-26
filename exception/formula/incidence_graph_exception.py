class IncidenceGraphException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ClauseIdDoesNotExistException(IncidenceGraphException):
    """
    The clause's id doesn't exist in the incidence graph
    """

    def __init__(self, clause_id: int):
        self.message = f"The clause's id ({clause_id}) doesn't exist in the incidence graph!"
        super().__init__(self.message)


class VariableDoesNotExistException(IncidenceGraphException):
    """
    The variable does not exist in the incidence graph
    """

    def __init__(self, variable: int):
        self.message = f"The variable ({variable}) doesn't exist in the incidence graph!"
        super().__init__(self.message)


class VariableHasBeenRemovedException(IncidenceGraphException):
    """
    The variable has been already removed from the incidence graph
    """

    def __init__(self, variable: int):
        self.message = f"The variable ({variable}) has been already removed from the incidence graph!"
        super().__init__(self.message)
