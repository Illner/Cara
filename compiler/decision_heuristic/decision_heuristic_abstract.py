# Import
from compiler.solver import Solver
from abc import ABC, abstractmethod
from typing import Set, Dict, List, Tuple, Union
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.cara_exception as c_exception
import exception.compiler.heuristic_exception as h_exception

# Import enum
import compiler.enum.heuristic.mixed_difference_heuristic_enum as mdf_enum


class DecisionHeuristicAbstract(ABC):
    """
    Decision heuristic
    """

    """
    Private PreselectionHeuristicAbstract preselection_heuristic
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract):
        self.__preselection_heuristic: PreselectionHeuristicAbstract = preselection_heuristic

    # region Abstract method
    @abstractmethod
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int,
                              additional_score_dictionary: Union[Dict[int, int], None] = None, max_number_of_returned_decision_variables: Union[int, None] = 1,
                              return_score: bool = False) -> Union[Union[int, List[int]], Tuple[Union[int, List[int]], Tuple[float, float, float, float, float]]]:
        """
        Get decision variable(s)
        :param cut_set: a cut set
        :param incidence_graph: an incidence graph
        :param solver: a solver
        :param assignment_list: a partial assignment for the solver
        :param depth: depth of the node
        :param max_number_of_returned_decision_variables: maximum number of returned decision variables (None for no limit).
        For 1, an integer is returned. Otherwise, a list is returned.
        :param additional_score_dictionary: a dictionary that contains additional scores
        :param return_score: should be the score of the decision variable returned as well
        :return: a decision variable or a list of decision variables
        :raise DecisionHeuristicDoesNotSupportReturningMoreDecisionVariablesException: if the decision heuristic does not support returning more decision variables
        """

        pass
    # endregion

    # region Protected method
    def _get_preselected_variables(self, cut_set: Set[int], incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        """
        Return a set of preselected variables based on the preselection heuristic
        :param cut_set: a cut set
        :param incidence_graph: an incidence graph
        :param depth: depth of the node where the preselection is used
        :return: a set of preselected variables
        :raises PreselectedVariableSetIsEmptyException: if the preselected variable set is empty
        """

        preselected_variable_set = self.__preselection_heuristic.preselect_variables(variable_restriction_set=cut_set,
                                                                                     incidence_graph=incidence_graph,
                                                                                     depth=depth)

        # The preselected variable set is empty
        if not preselected_variable_set:
            raise h_exception.PreselectedVariableSetIsEmptyException()

        return preselected_variable_set
    # endregion

    # region Static method
    @staticmethod
    def _process_implicit_bcp_dictionary(implicit_bcp_dictionary: Dict[int, Tuple[Union[Set[int], None], Union[Set[int], None]]]) -> \
            Tuple[Union[int, None], Dict[int, Tuple[Set[int], Set[int]]]]:

        implied_literal_dictionary: Dict[int, Tuple[Set[int], Set[int]]] = dict()   # key: a literal, value: (implied literals, complementary implied literals)

        for variable in implicit_bcp_dictionary:
            positive, negative = implicit_bcp_dictionary[variable]

            # Implied literal
            # if (positive is None) or (negative is None):
            #     return variable, dict()

            positive = set() if positive is None else positive
            negative = set() if negative is None else negative

            positive_temp = positive.union({variable})
            complementary_positive_temp = set(map(lambda l: -1 * l, positive_temp))

            negative_temp = negative.union({-variable})
            complementary_negative_temp = set(map(lambda l: -1 * l, negative_temp))

            implied_literal_dictionary[variable] = positive_temp, complementary_positive_temp
            implied_literal_dictionary[-variable] = negative_temp, complementary_negative_temp

        return None, implied_literal_dictionary

    @staticmethod
    def _compute_score_mixed_difference_heuristic(literal_score_dictionary: Dict[int, int], preselected_variable_set: Set[int],
                                                  mixed_difference_heuristic_enum: mdf_enum.MixedDifferenceHeuristicEnum) -> Dict[int, int]:
        score_dictionary: Dict[int, int] = dict()   # key: a variable, value: score of the variable

        for variable in preselected_variable_set:
            positive_score = literal_score_dictionary[variable]
            negative_score = literal_score_dictionary[-variable]

            # OK_SOLVER
            if mixed_difference_heuristic_enum == mdf_enum.MixedDifferenceHeuristicEnum.OK_SOLVER:
                score = positive_score * negative_score
            # POSIT_SATZ
            elif mixed_difference_heuristic_enum == mdf_enum.MixedDifferenceHeuristicEnum.POSIT_SATZ:
                score = 1024 * positive_score * negative_score + positive_score + negative_score
            # Not supported
            else:
                raise c_exception.FunctionNotImplementedException("compute_score_mixed_difference_heuristic",
                                                                  f"this type of mixed difference heuristic ({mixed_difference_heuristic_enum.name}) is not implemented")

            score_dictionary[variable] = score

        return score_dictionary
    # endregion
