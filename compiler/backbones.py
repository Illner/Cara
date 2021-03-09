# Wang, Zipeng & Bao, Yiping & Xing, Junhao & Chen, Xinyu & Liu, Sihan. (2016).
# Algorithm for Computing Backbones of Propositional Formulae Based on Solved Backbone Information.
# 10.2991/amsm-16.2016.8.

# Import
from compiler.solver import Solver
from typing import Set, Dict, List, Tuple, Union

# Import exception
import exception.cara_exception as c_exception
import exception.compiler.backbones_exception as b_exception

# Import enum
import compiler.enum.backbones_enum as b_enum


class Backbones:
    """
    Backbones
    """

    """
    Private Solver solver
    Private BackbonesEnum backbones_enum
    Private int/float backbones_chunk_size
    """

    def __init__(self, solver: Solver, backbones_enum: b_enum.BackbonesEnum, backbones_chunk_size: Union[int, float]):
        self.__solver: Solver = solver
        self.__backbones_enum: b_enum.BackbonesEnum = backbones_enum

        # Check if the chunk size is valid
        if backbones_chunk_size <= 0:
            raise b_exception.InvalidChunkSizeException(backbones_chunk_size)

        if backbones_chunk_size > 1:
            backbones_chunk_size = int(backbones_chunk_size)

        self.__backbones_chunk_size: Union[int, float] = backbones_chunk_size

    # region Public method
    def get_backbones(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Return a set of backbone literals for the assignment.
        If the formula is unsatisfiable, None is returned.
        :param assignment_list: the assignment
        :return: a set of backbone literals or None if the formula is unsatisfiable
        """

        assignment_list_temp = assignment_list.copy()

        # Iterative algorithm
        if self.__backbones_enum == b_enum.BackbonesEnum.ITERATIVE_ALGORITHM:
            return self.__get_backbones_iterative_algorithm(assignment_list_temp)

        # Chunking algorithm
        if self.__backbones_enum == b_enum.BackbonesEnum.CHUNKING_ALGORITHM:
            return self.__get_backbones_chunking_algorithm(assignment_list_temp)

        # Core-based Algorithm with Chunking
        if self.__backbones_enum == b_enum.BackbonesEnum.CORE_BASED_ALGORITHM_WITH_CHUNKING:
            return self.__get_backbones_core_based_algorithm_with_chunking(assignment_list_temp)

        raise c_exception.FunctionNotImplementedException("get_backbones",
                                                           f"this type of getting backbones ({self.__backbones_enum.name}) is not implemented")
    # endregion

    # region Private method
    def __get_backbones_iterative_algorithm(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Algorithm 3: Iterative algorithm (one test per variable)
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

            # A backbone has been found
            if result is None:
                backbone_literal_set.add(literal)
                assignment_list.append(literal)
            else:
                literal_to_try_set.intersection_update(result)

        return backbone_literal_set

    def __get_backbones_chunking_algorithm(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Algorithm 5: Chunking algorithm
        """

        pass

    def __get_backbones_core_based_algorithm_with_chunking(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Algorithm 7: Core-based Algorithm with Chunking
        """

        pass
    # endregion
