# Import
from typing import Set, List, Union
from formula.pysat_cnf import PySatCnf
from pysat.solvers import Minisat22, Glucose4

# Import exception
import exception.formula.formula_exception as f_exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum


class PySatHornCnf(PySatCnf):
    """
    PySAT HornCNF
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
    def append(self, clause: Union[Set[int], List[int]], check_horn: bool = True) -> None:
        """
        Append the clause to the formula
        :param check_horn: True for checking if the clause has at most 1 positive literal
        :param clause: the clause
        :return: None
        :raises FormulaIsNotHornException: if the clause contains more than one positive literal
        """

        # Check Horn
        if check_horn and sum(lit > 0 for lit in clause) > 1:
            raise f_exception.FormulaIsNotHornException(str(sorted(clause)))

        super().append(clause)
        self.__sat_solver.add_clause(clause)

    def get_model(self, assignment_list: List[int]) -> Union[List[int], None]:
        """
        Return a satisfying assignment.
        If the formula for the assignment is unsatisfiable, None is returned.
        :param assignment_list: a partial assignment
        :return: a complete assignment or None if the formula is unsatisfiable
        """

        no_conflict, assignment_list_temp = self.__sat_solver.propagate(assumptions=assignment_list)

        # The formula is not satisfiable
        if not no_conflict:
            return None

        result_model: Set[int] = set(assignment_list_temp)
        for var in self._variable_set:
            if (var not in result_model) and (-var not in result_model):
                # Negative literal
                assignment_list_temp.append(-var)
                no_conflict, _ = self.__sat_solver.propagate(assumptions=assignment_list_temp)
                assignment_list_temp.pop()

                if no_conflict:
                    result_model.add(-var)
                else:
                    result_model.add(var)   # first implied literal

        return list(result_model)
    # endregion

    # region Magic method
    def __del__(self):
        # Delete the SAT solver
        if self.__sat_solver is not None:
            self.__sat_solver.delete()
    # endregion
