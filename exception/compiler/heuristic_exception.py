# Import
from typing import List, Dict

# Import exception
from exception.cara_exception import CaraException


class HeuristicException(CaraException):
    def __init__(self, message: str):
        super().__init__(message)


class ClauseIsNotBinaryException(HeuristicException):
    """
    The clause is not binary
    """

    def __init__(self, clause: List[int]):
        self.message = f"The clause ({clause}) is not binary!"
        super().__init__(self.message)


class PreselectedVariableSetIsEmptyException(HeuristicException):
    """
    The preselected variable set is empty
    """

    def __init__(self):
        self.message = "The preselected variable set is empty!"
        super().__init__(self.message)


class WeightDoesNotExistForSizeOfClauseException(HeuristicException):
    """
    Weight does not exist for this size of a clause
    """

    def __init__(self, clause_size: int):
        self.message = f"Weight does not exist for this size of a clause ({str(clause_size)})!"
        super().__init__(self.message)


class InvalidAdditionalScoreDictionaryException(HeuristicException):
    """
    The additional score dictionary is invalid
    """

    def __init__(self, variable: int, additional_score_dictionary: Dict[int, int]):
        self.message = f"The variable {variable} is not mentioned in the additional score dictionary ({additional_score_dictionary})!"
        super().__init__(self.message)


class AdditionalScoreIsNotSupportedException(HeuristicException):
    """
    Additional score is not supported
    """

    def __init__(self):
        self.message = f"Additional score is not supported by this decision heuristic!"
        super().__init__(self.message)


class DecisionHeuristicDoesNotSupportReturningMoreDecisionVariablesException(HeuristicException):
    """
    The decision heuristic does not support returning more decision variables
    """

    def __init__(self):
        self.message = "The decision variable does not support returning more decision variables!"
        super().__init__(self.message)
