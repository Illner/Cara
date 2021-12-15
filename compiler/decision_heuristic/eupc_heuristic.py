# Import
import random
from compiler.solver import Solver
from typing import List, Set, Dict, Union
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.cara_exception as c_exception
import exception.compiler.heuristic_exception as h_exception

# Import enum
import compiler.enum.heuristic.mixed_difference_heuristic_enum as mdf_enum


class ExactUnitPropagationCountHeuristic(DecisionHeuristicAbstract):
    """
    Exact Unit Propagation Count - decision heuristic
    """

    """
    Private MixedDifferenceHeuristicEnum mixed_difference_heuristic_enum
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract,
                 mixed_difference_heuristic_enum: mdf_enum.MixedDifferenceHeuristicEnum):
        super().__init__(preselection_heuristic)

        self.__mixed_difference_heuristic_enum: mdf_enum.MixedDifferenceHeuristicEnum = mixed_difference_heuristic_enum

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int],
                              depth: int, additional_score_dictionary: Union[Dict[int, int], None] = None,
                              max_number_of_returned_decision_variables: Union[int, None] = 1) -> Union[int, List[int]]:
        # Additional score is used
        if additional_score_dictionary is not None:
            raise h_exception.AdditionalScoreIsNotSupportedException()

        # Returning more decision variables is not supported
        if max_number_of_returned_decision_variables != 1:
            raise h_exception.DecisionHeuristicDoesNotSupportReturningMoreDecisionVariablesException()

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        implicit_bcp_dictionary = solver.implicit_unit_propagation(assignment_list=assignment_list,
                                                                   variable_restriction_set=preselected_variable_set)

        # disable_sat => the formula can be unsatisfiable
        if implicit_bcp_dictionary is None:
            return random.sample(preselected_variable_set, 1)[0]

        score_dictionary: Dict[int, int] = dict()   # key: variable, value: score of the variable

        # Compute score
        for variable in implicit_bcp_dictionary:
            temp_positive, temp_negative = implicit_bcp_dictionary[variable]

            # Implied literal
            # if (temp_positive is None) or (temp_negative is None):
            #     return variable

            v_p = 0 if temp_positive is None else len(temp_positive)
            v_n = 0 if temp_negative is None else len(temp_negative)

            # OK_SOLVER
            if self.__mixed_difference_heuristic_enum == mdf_enum.MixedDifferenceHeuristicEnum.OK_SOLVER:
                score = v_p * v_n
            # POSIT_SATZ
            elif self.__mixed_difference_heuristic_enum == mdf_enum.MixedDifferenceHeuristicEnum.POSIT_SATZ:
                score = 1024 * v_p * v_n + v_p + v_n
            # Not supported
            else:
                raise c_exception.FunctionNotImplementedException("get_decision_variable",
                                                                  f"this type of mixed difference heuristic ({self.__mixed_difference_heuristic_enum.name}) is not implemented")

            score_dictionary[variable] = score

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return decision_variable
    # endregion
