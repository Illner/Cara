class InvalidDimacsCnfFormatException(Exception):
    """
    Invalid DIMACS CNF format
    """

    def __init__(self, message_extension: str = "no detailed information was given"):
        self.message = f"DIMACS CNF format is invalid in the file! ({message_extension})"

        super().__init__(self.message)

    def __str__(self):
        return self.message


class ClauseDoesNotExistException(Exception):
    """
    A clause doesn't exist in the formula
    """

    def __init__(self, id_clause: int):
        self.message = f"The clause with id ({id_clause}) doesn't exist in the formula!"

        super().__init__(self.message)

    def __str__(self):
        return self.message
