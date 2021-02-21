# Import
import itertools
from formula.cnf import Cnf
from pysat.formula import CNF
from pysat.solvers import Minisat22, Glucose4, Lingeling, Cadical
from typing import Set, Dict, List, Tuple, Union

# Import exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.sat_solver_enum as ss_enum


class Solver:
    """
    SAT Solver
    """

    """
    Private CNF cnf
    Private Set<int> variable_set
    
    Private SatSolverEnum sat_solver_enum
    Private Solver sat_main                 # main SAT solver
    Private Solver sat_unit_propagation     # for unit propagation
    """

    def __init__(self, cnf: Cnf, clause_id_set: Set[int],
                 sat_solver_enum: ss_enum.SatSolverEnum = ss_enum.SatSolverEnum.MiniSAT):
        self.__cnf: CNF = CNF()
        self.__sat_solver_enum: ss_enum.SatSolverEnum = sat_solver_enum

        # Create a subformula
        for clause_id in clause_id_set:
            self.__cnf.append(cnf._get_clause(clause_id))

        self.__variable_set: Set[int] = cnf.get_variable_in_clauses(clause_id_set)

        # Create SAT solvers
        self.__sat_main = None
        self.__sat_unit_propagation = None
        # MiniSat
        if self.__sat_solver_enum == ss_enum.SatSolverEnum.MiniSAT:
            self.__sat_main = Minisat22(bootstrap_with=self.__cnf.clauses, use_timer=True)
            self.__sat_unit_propagation = self.__sat_main
        # Glucose
        elif self.__sat_solver_enum == ss_enum.SatSolverEnum.Glucose:
            self.__sat_main = Glucose4(bootstrap_with=self.__cnf.clauses, use_timer=True)
            self.__sat_unit_propagation = self.__sat_main
        # Lingeling
        elif self.__sat_solver_enum == ss_enum.SatSolverEnum.Lingeling:
            self.__sat_main = Lingeling(bootstrap_with=self.__cnf.clauses, use_timer=True)
            self.__sat_unit_propagation = Minisat22(bootstrap_with=self.__cnf.clauses, use_timer=True)
        # CaDiCal
        elif self.__sat_solver_enum == ss_enum.SatSolverEnum.CaDiCal:
            self.__sat_main = Cadical(bootstrap_with=self.__cnf.clauses, use_timer=True)
            self.__sat_unit_propagation = Minisat22(bootstrap_with=self.__cnf.clauses, use_timer=True)
        # Not supported
        else:
            raise c_exception.SatSolverIsNotSupportedException(self.__sat_solver_enum)

    # region Public method
    def is_satisfiable(self, assignment: List[int]) -> bool:
        """
        Check if the formula is satisfiable for the assignment
        :param assignment: the assignment
        :return: True if the formula is satisfiable, otherwise False is returned
        """

        return self.__sat_main.solve(assumptions=assignment)

    def unit_propagation(self, assignment: List[int]) -> Union[Set[int], None]:
        """
        Do unit propagation (boolean constraint propagation).
        If the formula for the assignment is unsatisfiable, return None.
        :param assignment: the assignment
        :return: a list of implied literals or None if the formula is unsatisfiable
        """

        is_sat, implied_literals = self.__sat_unit_propagation.propagate(assumptions=assignment)

        # The formula is not satisfiable
        if not is_sat:
            return None

        implied_literals = set(implied_literals)
        implied_literals.difference_update(set(assignment))

        return implied_literals

    def implicit_unit_propagation(self, assignment: List[int]) -> Union[Dict[int, Tuple[Union[List[int], None], Union[List[int], None]]], None]:
        """
        Do implicit unit propagation (implicit boolean constraint propagation).
        If the formula for the assignment is unsatisfiable, return None.
        :param assignment: the assignment
        :return: For each variable is returned a tuple. The first element contains a set of implied literals if the variable is set to True,
        the second element of the tuple contains a set of implied literals if the variable is set to False.
        If the formula is unsatisfiable after setting a variable, None will appear in the tuple instead of a list.
        """

        implied_literal_set = self.unit_propagation(assignment)

        # The formula is unsatisfiable
        if implied_literal_set is None:
            return None

        temp_set = set(map(lambda l: abs(l), itertools.chain(assignment, implied_literal_set)))
        variable_to_try_set = self.__variable_set.difference(temp_set)
        result_dictionary = dict()

        for var in variable_to_try_set:
            # Positive literal
            assignment.append(var)
            temp_positive = self.unit_propagation(assignment)
            assignment.pop()

            # Negative literal
            assignment.append(-var)
            temp_negative = self.unit_propagation(assignment)
            assignment.pop()

            result_dictionary[var] = (temp_positive, temp_negative)

        return result_dictionary
    # endregion

    # region Magic function
    def __del__(self):
        # Delete the main SAT Solver
        if self.__sat_main is not None:
            self.__sat_main.delete()

        # Delete the SAT solver for unit propagation
        if self.__sat_unit_propagation is not None:
            self.__sat_unit_propagation.delete()
    # endregion
