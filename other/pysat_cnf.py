# Import
from pysat.formula import CNF
from typing import Set, List, Iterator, Union


class PySatCNF(CNF):
    """
    PySAT CNF
    """

    """
    Private Set<int> variable_set
    """

    def __init__(self):
        super().__init__()

        self.__variable_set: Set[int] = set()

    def append(self, clause: Union[Iterator[int], Set[int], List[int]]) -> None:
        self.__variable_set.update(map(lambda lit: abs(lit), clause))

        super().append(clause)

    def __str__(self):
        result = " ".join(('p cnf', str(len(self.__variable_set)), str(len(self.clauses))))

        for clause in self.clauses:
            result = "\n".join((result, " ".join((" ".join(str(lit) for lit in clause), "0"))))

        return result
