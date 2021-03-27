# Import
from pysat.formula import CNF
from typing import Set, List, Union


class PySatCnf(CNF):
    """
    PySAT CNF
    """

    """
    Private bool is_2_cnf
    Private int formula_length
    Protected Set<int> variable_set
    """

    def __init__(self):
        super().__init__()

        self.__is_2_cnf: bool = True
        self.__formula_length: int = 0
        self._variable_set: Set[int] = set()

    def append(self, clause: Union[Set[int], List[int]]) -> None:
        self._variable_set.update(map(lambda l: abs(l), clause))
        self.__formula_length += len(clause)

        # Check 2-CNF
        if len(clause) > 2:
            self.__is_2_cnf = False

        super().append(clause)

    def __str__(self):
        result = " ".join(('p cnf', str(self.number_of_variables), str(self.number_of_clauses)))

        for clause in self.clauses:
            result = "\n".join((result, " ".join((" ".join(str(lit) for lit in clause), "0"))))

        return result

    # region Property
    @property
    def number_of_variables(self):
        return len(self._variable_set)

    @property
    def number_of_clauses(self):
        return len(self.clauses)

    @property
    def formula_length(self):
        return self.__formula_length

    @property
    def is_2_cnf(self):
        return self.__is_2_cnf
    # endregion
