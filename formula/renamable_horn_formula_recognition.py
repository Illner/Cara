# Import
from formula.two_cnf import TwoCnf
from other.pysat_cnf import PySatCnf
from typing import Set, Dict, List, Union


class RenamableHornFormulaRecognition:
    """
    A linear time recognition algorithm for (renamable) Horn formula
    Bengt Aspvall. Recognizing disguised NR(1) instances of the satisfiability problem. J. Algorithms, 1(1):97–103, 1980. (Cited pages 43, 44 and 121.)
    """

    """
    Private TwoCnf cnf
    Private int variable_id_counter

    Private Dict<int, int> clause_variable_dictionary                   # key: a clause, value: a variable representing the clause
    Private Dict<int, int> variable_clause_dictionary                   # key: a variable, value: a clause which is represented by the variable
    Private Dict<int, Set<int>> clause_auxiliary_variable_dictionary    # key: a clause, value: a set of auxiliary variables for the clause
    """

    def __init__(self, incidence_graph):
        self.__variable_id_counter: int = max(incidence_graph.variable_set(), default=0)

        # Mappings
        self.__clause_variable_dictionary: Dict[int, int] = dict()
        self.__variable_clause_dictionary: Dict[int, int] = dict()
        self.__clause_auxiliary_variable_dictionary: Dict[int, Set[int]] = dict()

        pysat_cnf = self.__create_cnf_formula(incidence_graph)
        self.__cnf: TwoCnf = TwoCnf(pysat_cnf, check_2_cnf=False)

    # region Private method
    def __get_new_variable_id(self) -> int:
        """
        Return a new variable ID.
        The ID counter will be incremented.
        :return: a new ID
        """

        self.__variable_id_counter += 1
        return self.__variable_id_counter

    def __create_cnf_formula(self, incidence_graph) -> PySatCnf:
        pysat_cnf: PySatCnf = PySatCnf()

        for clause_id in incidence_graph.clause_id_set():
            clause = incidence_graph.get_clause(clause_id)
            clause_len = len(clause)
            previous_y: Union[int, None] = None

            # Mappings
            clause_variable = self.__get_new_variable_id()
            self.__clause_variable_dictionary[clause_id] = clause_variable
            self.__variable_clause_dictionary[clause_variable] = clause_id
            self.__clause_auxiliary_variable_dictionary[clause_id] = {clause_variable}

            for i, lit in enumerate(clause):
                is_last = True if i == (clause_len - 1) else False

                # Unit clause
                if (previous_y is None) and is_last:
                    pysat_cnf.append([lit, clause_variable])
                    continue

                # Last literal
                if is_last:
                    pysat_cnf.append([-previous_y, lit, clause_variable])
                    continue

                new_y = self.__get_new_variable_id()
                self.__clause_auxiliary_variable_dictionary[clause_id].add(new_y)

                # First literal
                if previous_y is None:
                    pysat_cnf.append([lit, new_y, clause_variable])
                    previous_y = new_y
                    continue

                pysat_cnf.append([-previous_y, lit, clause_variable])
                pysat_cnf.append([-previous_y, new_y, clause_variable])
                pysat_cnf.append([lit, new_y, clause_variable])
                previous_y = new_y

        return pysat_cnf
    # endregion

    # region Public method
    def is_renamable_horn_formula(self, satisfied_clause_set: Set[int],
                                  unresolved_clause_set: Set[int],
                                  neg_assigned_literal_set: Set[int],
                                  variable_restriction_set: Set[int]) -> Union[Set[int], None]:
        """
        Check if the subformula is (renamable) Horn
        :param satisfied_clause_set: a set of satisfied clauses (for the subformula)
        :param unresolved_clause_set: a set of unresolved clauses (for the subformula)
        :param neg_assigned_literal_set: a partial assignment where literals are negated
        :param variable_restriction_set: a set of variables on which the model will be restricted
        :return: If the subformula is (renamable) Horn, a renaming function (a set of variables) is returned.
        If the subformula is not (renamable) Horn, None is returned.
        """

        assignment_temp: Set[int] = neg_assigned_literal_set

        # Satisfied clauses
        for clause_id in satisfied_clause_set:
            variable_temp = self.__clause_variable_dictionary[clause_id]
            assignment_temp.add(variable_temp)

        # Unresolved clauses
        for clause_id in unresolved_clause_set:
            variable_temp = self.__clause_variable_dictionary[clause_id]
            assignment_temp.add(-variable_temp)

        result = self.__cnf.get_model(list(assignment_temp), variable_restriction_set=variable_restriction_set)

        # The subformula is not (renamable) Horn
        if result is None:
            return None

        return set(filter(lambda l: (abs(l) in variable_restriction_set) and (l > 0), result))
    # endregion
