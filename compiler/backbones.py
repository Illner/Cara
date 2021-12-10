# Import
from compiler.solver import Solver
from typing import Set, List, Union
from compiler_statistics.compiler.solver_statistics import SolverStatistics


class Backbones:
    """
    Backbones
    Janota, Mikoláš & Lynce, Ines & Marques-Sliva, Joao. (2015). Algorithms for computing backbones of propositional formulae. Ai Communications. 28. 161-177. 10.3233/AIC-140640.
    """

    """
    Private Solver solver
    Private SolverStatistics statistics
    """

    def __init__(self, solver: Solver, statistics: Union[SolverStatistics, None] = None):
        # Statistics
        if statistics is None:
            self.__statistics: SolverStatistics = SolverStatistics(active=False)
        else:
            self.__statistics: SolverStatistics = statistics

        self.__solver: Solver = solver

    # region Public method
    def get_backbone_literals(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Return a set of backbone literals for the assignment.
        If the formula is unsatisfiable, None is returned.
        :param assignment_list: a partial assignment
        :return: a set of backbone literals or None if the formula is unsatisfiable
        """

        assignment_list_temp = assignment_list.copy()

        return self.__get_backbone_literal_iterative_algorithm(assignment_list_temp)
    # endregion

    # region Private method
    def __get_backbone_literal_iterative_algorithm(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Iterative algorithm (one test per variable)
        """

        # Get implied literals by unit propagation
        result = self.__solver.unit_propagation(assignment_list=assignment_list)

        # The formula is unsatisfiable => no backbones
        if result is None:
            return None

        backbone_literal_set = result
        for implied_literal in result:
            assignment_list.append(implied_literal)

        # Get model
        result = self.__solver.get_model(assignment_list=assignment_list)

        # The formula is unsatisfiable => no backbones
        if result is None:
            return None

        number_of_iterations: int = 0
        literal_to_try_set = set(result)

        while len(literal_to_try_set):
            number_of_iterations += 1

            literal = literal_to_try_set.pop()

            assignment_list.append(-literal)
            result = self.__solver.get_model(assignment_list=assignment_list)
            assignment_list.pop()

            # A backbone literal has been found
            if result is None:
                backbone_literal_set.add(literal)
                assignment_list.append(literal)
            else:
                literal_to_try_set.intersection_update(result)

        self.__statistics.backbone_literals_iteration.add_count(number_of_iterations)   # counter
        return backbone_literal_set
    # endregion
