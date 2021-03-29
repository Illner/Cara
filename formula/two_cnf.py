# Import
from typing import Set, List, Union
from other.pysat_cnf import PySatCnf
from pysat.solvers import Minisat22, Glucose4

# Import exception
import exception.formula.formula_exception as f_exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum


class TwoCnf:
    """
    2-CNF representation
    """

    """
    Private PySatCnf cnf
    Private Solver sat_solver
    """

    def __init__(self, cnf: Union[PySatCnf, None] = None, check_2_cnf: bool = True,
                 propagate_sat_solver_enum: ss_enum.PropagateSatSolverEnum = ss_enum.PropagateSatSolverEnum.MiniSAT):
        self.__sat_solver = None

        # CNF
        if cnf is None:
            self.__cnf: PySatCnf = PySatCnf()
        else:
            # Check 2-CNF
            if check_2_cnf and not cnf.is_2_cnf:
                raise f_exception.FormulaIsNot2CnfException()

            self.__cnf: PySatCnf = cnf

        # Create SAT solver
        # MiniSAT
        if propagate_sat_solver_enum == ss_enum.PropagateSatSolverEnum.MiniSAT:
            self.__sat_solver = Minisat22(bootstrap_with=self.__cnf.clauses, use_timer=True)
        # Glucose
        elif propagate_sat_solver_enum == ss_enum.PropagateSatSolverEnum.Glucose:
            self.__sat_solver = Glucose4(bootstrap_with=self.__cnf.clauses, use_timer=True)
        # Not supported
        else:
            raise c_exception.SatSolverIsNotSupportedException(propagate_sat_solver_enum)

    # region Public method
    def append(self, clause: Union[Set[int], List[int]]) -> None:
        """
        Append the clause to the formula.
        If the clause contains more than two literals, raise an exception (FormulaIsNot2CnfException).
        :param clause: the clause
        :return: None
        """

        # Check 2-CNF
        if len(clause) > 2:
            raise f_exception.FormulaIsNot2CnfException(str(clause))

        self.__cnf.append(clause)
        self.__sat_solver.add_clause(clause)

    def get_model(self, assignment_list: List[int], variable_restriction_set: Union[Set[int], None] = None) -> Union[List[int], None]:
        """
        Return a satisfying assignment.
        If the formula for the assignment is unsatisfiable, return None.
        :param assignment_list: a partial assignment
        :param variable_restriction_set: a set of variables on which the model will be restricted
        :return: a complete assignment or None if the formula is unsatisfiable
        """

        no_conflict, assignment_list_temp = self.__sat_solver.propagate(assumptions=assignment_list)

        # The formula is not satisfiable
        if not no_conflict:
            return None

        result_model: List[int] = []

        if variable_restriction_set is None:
            variable_to_try_set = self.__cnf.get_variable_set(copy=True)
        else:
            variable_to_try_set = variable_restriction_set.copy()

        while variable_to_try_set:
            var = variable_to_try_set.pop()

            # Positive literal
            assignment_list_temp.append(var)
            no_conflict, implied_literals = self.__sat_solver.propagate(assumptions=assignment_list_temp)

            if no_conflict:
                result_model.append(var)
                assignment_list_temp = implied_literals
                continue

            assignment_list_temp.pop()

            # Negative literal
            assignment_list_temp.append(-var)
            no_conflict, implied_literals = self.__sat_solver.propagate(assumptions=assignment_list_temp)

            if no_conflict:
                result_model.append(-var)
                assignment_list_temp = implied_literals
                continue

            # The formula is not satisfiable
            return None

        return result_model
    # endregion

    # region Magic method
    def __str__(self):
        return str(self.__cnf)

    def __del__(self):
        # Delete the SAT solver
        if self.__sat_solver is not None:
            self.__sat_solver.delete()
    # endregion

    # region Property
    @property
    def number_of_variables(self):
        return self.__cnf.number_of_variables

    @property
    def number_of_clauses(self):
        return self.__cnf.number_of_clauses

    @property
    def formula_length(self):
        return self.__cnf.formula_length
    # endregion
