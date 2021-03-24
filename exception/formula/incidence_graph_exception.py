# Import
from exception.cara_exception import CaraException


class IncidenceGraphException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class ClauseIdDoesNotExistException(IncidenceGraphException):
    """
    The clause's id doesn't exist in the incidence graph
    """

    def __init__(self, clause_id: int):
        self.message = f"The clause's id ({clause_id}) doesn't exist in the incidence graph!"
        super().__init__(self.message)


class ClauseIdAlreadyExistsException(IncidenceGraphException):
    """
    The clause's id already exists in the incidence graph
    """

    def __init__(self, clause_id: int):
        self.message = f"The clause's id ({clause_id}) already exists in the incidence graph!"
        super().__init__(self.message)


class ClauseHasBeenRemovedException(IncidenceGraphException):
    """
    The clause has been already removed from the incidence graph
    """

    def __init__(self, clause_id: int):
        self.message = f"The clause ({clause_id}) has been already removed from the incidence graph!"
        super().__init__(self.message)


class VariableDoesNotExistException(IncidenceGraphException):
    """
    The variable does not exist in the incidence graph
    """

    def __init__(self, variable: int):
        self.message = f"The variable ({variable}) doesn't exist in the incidence graph!"
        super().__init__(self.message)


class VariableAlreadyExistsException(IncidenceGraphException):
    """
    The variable already exists in the incidence graph
    """

    def __init__(self, variable: int):
        self.message = f"The variable ({variable}) already exists in the incidence graph!"
        super().__init__(self.message)


class VariableHasBeenRemovedException(IncidenceGraphException):
    """
    The variable has been already removed from the incidence graph
    """

    def __init__(self, variable: int):
        self.message = f"The variable ({variable}) has been already removed from the incidence graph!"
        super().__init__(self.message)


class TryingRestoreLiteralHasNotBeenRemovedException(IncidenceGraphException):
    """
    Trying to restore the variable node that has not been removed
    """

    def __init__(self, literal: int):
        self.message = f"Trying to restore the variable node (|{literal}|) that has not been removed!"
        super().__init__(self.message)


class TryingRestoreLiteralIsNotLastOneRemovedException(IncidenceGraphException):
    """
    Trying to restore the variable node that is not the last one that was removed
    """

    def __init__(self, literal: int, last_literal: int):
        self.message = f"Trying to restore the variable node (|{literal}|) that is not the last one (|{last_literal}|) that was removed!"
        super().__init__(self.message)


class TryingRemoveEdgeDoesNotExistException(IncidenceGraphException):
    """
    Trying to remove the edge that does not exist
    """

    def __init__(self, variable: int, clause_id: int):
        self.message = f"Trying to remove the edge ({variable} - {clause_id}) that does not exist in the incidence graph!"
        super().__init__(self.message)
