# Import exception
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


class PLineIsNotMentionedException(FormulaException):
    """
    P line is not mentioned at all or is mentioned after the clauses
    """

    def __init__(self):
        self.message = "P line is not mentioned at all or is mentioned after the clauses!"
        super().__init__(self.message)


class FormulaIsNot2CnfException(FormulaException):
    """
    The formula is not 2-CNF
    """

    def __init__(self, message_extension: str = ""):
        self.message = "The formula is not 2-CNF!"
        if message_extension:
            self.message += f" ({message_extension})"
        super().__init__(self.message)


class FormulaIsNotHornException(FormulaException):
    """
    The formula is not Horn
    """

    def __init__(self, message_extension: str = ""):
        self.message = "The formula is not Horn!"
        if message_extension:
            self.message += f" ({message_extension})"
        super().__init__(self.message)
