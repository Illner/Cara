# Import
from pysat.formula import CNF
from typing import Set, List, Union


class PySatCnf(CNF):
    """
    PySAT CNF
    """

    """
    Private int formula_length
    Private Set<int> variable_set
    
    Private bool is_2_cnf
    Private bool is_horn_formula
    """

    def __init__(self):
        super().__init__()

        self.__formula_length: int = 0
        self.__variable_set: Set[int] = set()

        self.__is_2_cnf: bool = True
        self.__is_horn_formula: bool = True

    def append(self, clause: Union[Set[int], List[int]]) -> None:
        self.__formula_length += len(clause)

        number_of_positive_literals = 0
        for lit in clause:
            self.__variable_set.add(abs(lit))

            if lit > 0:
                number_of_positive_literals += 1

        # Check Horn formula
        if number_of_positive_literals > 1:
            self.__is_horn_formula = False

        # Check 2-CNF
        if len(clause) > 2:
            self.__is_2_cnf = False

        super().append(clause)

    def __str__(self):
        result = " ".join(('p cnf', str(self.number_of_variables), str(self.number_of_clauses)))

        for clause in self.clauses:
            result = "\n".join((result, " ".join((" ".join(str(lit) for lit in clause), "0"))))

        return result

    # region Public
    def get_variable_set(self, copy: bool = False):
        """
        :param copy: True if a copy is returned
        :return: a set of variables
        """

        if copy:
            return self.__variable_set.copy()

        return self.__variable_set
    # endregion

    # region Property
    @property
    def number_of_variables(self):
        return len(self.__variable_set)

    @property
    def number_of_clauses(self):
        return len(self.clauses)

    @property
    def formula_length(self):
        return self.__formula_length

    @property
    def is_2_cnf(self):
        return self.__is_2_cnf

    @property
    def is_horn_formula(self):
        return self.__is_horn_formula
    # endregion
