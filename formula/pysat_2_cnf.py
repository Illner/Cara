# Import
from typing import Set, List, Union
from formula.pysat_cnf import PySatCnf
from pysat.solvers import Minisat22, Glucose4

# Import exception
import exception.formula.formula_exception as f_exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum


class PySat2Cnf(PySatCnf):
    """
    PySAT 2-CNF
    """

    """
    Private Solver sat_solver
    """

    def __init__(self, propagate_sat_solver_enum: ss_enum.PropagateSatSolverEnum = ss_enum.PropagateSatSolverEnum.MiniSAT):
        super().__init__()

        # Create a SAT solver
        self.__sat_solver = None
        # MiniSAT
        if propagate_sat_solver_enum == ss_enum.PropagateSatSolverEnum.MiniSAT:
            self.__sat_solver = Minisat22(bootstrap_with=self.clauses)
        # Glucose
        elif propagate_sat_solver_enum == ss_enum.PropagateSatSolverEnum.Glucose:
            self.__sat_solver = Glucose4(bootstrap_with=self.clauses)
        # Not supported
        else:
            raise c_exception.SatSolverIsNotSupportedException(propagate_sat_solver_enum)

    # region Public method
    def append(self, clause: Union[Set[int], List[int]], check_2_cnf: bool = True) -> None:
        """
        Append the clause to the formula
        :param check_2_cnf: True for checking if the clause has at most 2 literals
        :param clause: the clause
        :return: None
        :raises FormulaIsNot2CnfException: if the clause contains more than two literals
        """

        # Check 2-CNF
        if check_2_cnf and len(clause) > 2:
            raise f_exception.FormulaIsNot2CnfException(str(sorted(clause)))

        super().append(clause)
        self.__sat_solver.add_clause(clause)

    def get_model(self, assignment_list: List[int], variable_restriction_set: Union[Set[int], None] = None) -> Union[List[int], None]:
        """
        Return a satisfying assignment.
        If the formula for the assignment is unsatisfiable, None is returned.
        :param assignment_list: a partial assignment
        :param variable_restriction_set: a set of variables on which the model will be restricted
        :return: a complete assignment or None if the formula is unsatisfiable
        """

        no_conflict, assignment_list_temp = self.__sat_solver.propagate(assumptions=assignment_list)

        # The formula is not satisfiable
        if not no_conflict:
            return None

        result_model: List[int] = []

        # Variable restriction
        if variable_restriction_set is None:
            variable_to_try_set = self.get_variable_set(copy=True)
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
    def __del__(self):
        # Delete the SAT solver
        if self.__sat_solver is not None:
            self.__sat_solver.delete()
    # endregion
