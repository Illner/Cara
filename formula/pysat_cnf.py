# Import
import itertools
from pysat.formula import CNF
from pysat.solvers import Minisat22
from typing import Set, List, Union
from other.sorted_list import SortedList


class PySatCnf(CNF):
    """
    PySAT CNF
    """

    """
    Private int formula_length
    Private Set<int> literal_set
    Private Set<int> variable_set
    
    Private bool is_2_cnf
    Private bool is_horn_formula
    """

    def __init__(self):
        super().__init__()

        self.__formula_length: int = 0
        self.__literal_set: Set[int] = set()
        self.__variable_set: Set[int] = set()

        self.__is_2_cnf: bool = True
        self.__is_horn_formula: bool = True

    # region Public method
    def append(self, clause: Union[Set[int], List[int]]) -> None:
        self.__formula_length += len(clause)

        number_of_positive_literals = 0
        for lit in clause:
            self.__literal_set.add(lit)
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

    def get_number_of_models(self, assignment_list: List[int]) -> int:
        """
        Return the number of models.
        Time complexity is exponential!!!
        :param assignment_list: a partial assignment
        :return: the number of models
        """

        variable_set = self.get_variable_set(copy=True)
        for lit in assignment_list:
            var = abs(lit)
            if var in variable_set:
                variable_set.remove(var)

        variable_list = list(variable_set)
        mask_iterator = itertools.product([0, 1], repeat=len(variable_list))

        solver = Minisat22(bootstrap_with=self.clauses)
        for lit in assignment_list:
            solver.add_clause([lit])

        number_of_models = 0
        # Iterate over all possible assignments
        for mask in mask_iterator:
            assignment_temp = []

            # Create an assignment
            for i, sign in enumerate(mask):
                var = variable_list[i]
                if sign:
                    assignment_temp.append(var)
                else:
                    assignment_temp.append(-var)

            is_sat = solver.solve(assumptions=assignment_temp)

            # A new model has been found
            if is_sat:
                number_of_models += 1

        solver.delete()

        return number_of_models

    def str_renaming_function(self, renaming_function: Set[int]) -> str:
        result = " ".join(('p cnf', str(self.number_of_variables), str(self.number_of_clauses)))

        for clause in self.clauses:
            clause_temp = [-lit if abs(lit) in renaming_function else lit for lit in clause]
            result = "\n".join((result, " ".join((" ".join(map(str, clause_temp)), "0"))))

        return result
    # endregion

    # region Magic method
    def __str__(self):
        return self.str_renaming_function(renaming_function=set())

    def __repr__(self):
        clause_sorted_list = SortedList()
        for clause in self.clauses:
            clause_sorted_list.add(SortedList(clause))

        return " ".join(map(lambda c: c.str_delimiter(end_delimiter="0"), clause_sorted_list))
    # endregion

    # region Public method
    def get_variable_set(self, copy: bool):
        """
        :param copy: True if a copy is returned
        :return: a set of variables
        """

        if copy:
            return self.__variable_set.copy()

        return self.__variable_set

    def get_literal_set(self, copy: bool):
        """
        :param copy: True if a copy is returned
        :return: a set of literals
        """

        if copy:
            return self.__literal_set.copy()

        return self.__literal_set
    # endregion

    # region Property
    @property
    def number_of_variables(self) -> int:
        return len(self.__variable_set)

    @property
    def number_of_clauses(self) -> int:
        return len(self.clauses)

    @property
    def formula_length(self) -> int:
        return self.__formula_length

    @property
    def is_2_cnf(self) -> bool:
        return self.__is_2_cnf

    @property
    def is_horn_formula(self) -> bool:
        return self.__is_horn_formula
    # endregion
