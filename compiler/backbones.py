# Import
from compiler.solver import Solver
from typing import Set, List, Union


class Backbones:
    """
    Backbones
    """

    """
    Private Solver solver
    """

    def __init__(self, solver: Solver):
        self.__solver: Solver = solver

    # region Public method
    def get_backbone_literals(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Return a set of backbone literals for the assignment.
        If the formula is unsatisfiable, None is returned.
        :param assignment_list: an assignment
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

        result = self.__solver.get_model(assignment_list)

        # The formula is unsatisfiable => no backbones
        if result is None:
            return None

        literal_to_try_set = set(result)
        backbone_literal_set = set()

        while len(literal_to_try_set):
            literal = literal_to_try_set.pop()

            assignment_list.append(-literal)
            result = self.__solver.get_model(assignment_list)
            assignment_list.pop()

            # A backbone literal has been found
            if result is None:
                backbone_literal_set.add(literal)
                assignment_list.append(literal)
            else:
                literal_to_try_set.intersection_update(result)

        return backbone_literal_set
    # endregion
