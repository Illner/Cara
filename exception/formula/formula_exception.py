# Import
from exception.cara_exception import CaraException


class FormulaException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidDimacsCnfFormatException(FormulaException):
    """
    Invalid DIMACS CNF format
    """

    def __init__(self, message_extension: str = "no detailed information was given"):
        self.message = f"DIMACS CNF format is invalid in the file! ({message_extension})"
        super().__init__(self.message)


class ClauseDoesNotExistException(FormulaException):
    """
    The clause doesn't exist in the formula
    """

    def __init__(self, id_clause: int):
        self.message = f"The clause with id ({id_clause}) doesn't exist in the formula!"
        super().__init__(self.message)


class VariableDoesNotExistException(FormulaException):
    """
    The variable does not exist
    """

    def __init__(self, variable: int):
        self.message = f"The variable ({variable}) was not defined on p line but is used in a clause!"
        super().__init__(self.message)


class PLineIsNotMentionedException(FormulaException):
    """
    P line is not mentioned at all or is mentioned after the clauses
    """

    def __init__(self):
        self.message = "P line is not mentioned at all or is mentioned after the clauses!"
        super().__init__(self.message)
