# Import
from compiler.solver import Solver
from typing import List, Set, Dict, Union, Tuple
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.cara_exception as c_exception
import exception.compiler.heuristic_exception as h_exception

# Import enum
import compiler.enum.heuristic.literal_count_heuristic_function_enum as lchf_enum


class LiteralCountHeuristic(DecisionHeuristicAbstract):
    """
    Literal count - decision heuristic
    """

    """
    Private function
    Private tie_breaker_function
    Private bool ignore_binary_clauses
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, ignore_binary_clauses: bool,
                 function_enum: lchf_enum.LiteralCountHeuristicFunctionEnum,
                 tie_breaker_function_enum: Union[lchf_enum.LiteralCountHeuristicFunctionEnum, None] = None):
        super().__init__(preselection_heuristic)

        self.__ignore_binary_clauses: bool = ignore_binary_clauses

        # (tie-breaker) function
        self.__function = LiteralCountHeuristic.__get_function(function_enum)
        if tie_breaker_function_enum is None:
            self.__tie_breaker_function = self.__function
        else:
            self.__tie_breaker_function = LiteralCountHeuristic.__get_function(tie_breaker_function_enum)

    # region Static method
    @staticmethod
    def __avg(v):
        return sum(v) / len(v)
    # endregion

    # region Static method
    @staticmethod
    def __get_function(function_enum: lchf_enum.LiteralCountHeuristicFunctionEnum):
        # SUM
        if function_enum == lchf_enum.LiteralCountHeuristicFunctionEnum.SUM:
            return sum

        # MAX
        if function_enum == lchf_enum.LiteralCountHeuristicFunctionEnum.MAX:
            return max

        # MIN
        if function_enum == lchf_enum.LiteralCountHeuristicFunctionEnum.MIN:
            return min

        # AVG
        if function_enum == lchf_enum.LiteralCountHeuristicFunctionEnum.AVG:
            return LiteralCountHeuristic.__avg

        # Not supported
        raise c_exception.FunctionNotImplementedException("get_function",
                                                          f"this type of function ({function_enum.name}) is not implemented")
    # endregion

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int,
                              additional_score_dictionary: Union[Dict[int, int], None] = None, max_number_of_returned_decision_variables: Union[int, None] = 1,
                              return_score: bool = False) -> Union[Union[int, List[int]], Tuple[Union[int, List[int]], Union[int, Tuple[int, int], Tuple[int, int, int], Tuple[int, int, int, int], Tuple[int, int, int, int, int]]]]:
        # Returning more decision variables is not supported
        if max_number_of_returned_decision_variables != 1:
            raise h_exception.DecisionHeuristicDoesNotSupportReturningMoreDecisionVariablesException()

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            decision_variable = list(preselected_variable_set)[0]
            return (decision_variable, 0) if return_score else decision_variable

        # key: variable, value: ([additional_score], score_1, score_2, [score_3, score_4])
        score_dictionary: Dict[int, Union[Tuple[int, int], Tuple[int, int, int], Tuple[int, int, int, int], Tuple[int, int, int, int, int]]] = dict()

        # Compute score
        for variable in preselected_variable_set:
            positive_score = incidence_graph.literal_number_of_occurrences(literal=variable,
                                                                           ignore_binary_clauses=self.__ignore_binary_clauses)
            negative_score = incidence_graph.literal_number_of_occurrences(literal=(-variable),
                                                                           ignore_binary_clauses=self.__ignore_binary_clauses)

            additional_score: Union[int, None] = None
            # Additional score is used
            if additional_score_dictionary is not None:
                if variable in additional_score_dictionary:
                    additional_score = additional_score_dictionary[variable]
                else:
                    raise h_exception.InvalidAdditionalScoreDictionaryException(variable=variable,
                                                                                additional_score_dictionary=additional_score_dictionary)

            # Binary clauses are ignored
            if self.__ignore_binary_clauses:
                score_1 = self.__function([positive_score[0], negative_score[0]])
                score_2 = self.__function([positive_score[1], negative_score[1]])
                score_3 = self.__tie_breaker_function([positive_score[0], negative_score[0]])
                score_4 = self.__tie_breaker_function([positive_score[1], negative_score[1]])

                if additional_score is None:
                    score_dictionary[variable] = score_1, score_2, score_3, score_4
                else:
                    score_dictionary[variable] = additional_score, score_1, score_2, score_3, score_4
            else:
                score_1 = self.__function([positive_score, negative_score])
                score_2 = self.__tie_breaker_function([positive_score, negative_score])

                if additional_score is None:
                    score_dictionary[variable] = score_1, score_2
                else:
                    score_dictionary[variable] = additional_score, score_1, score_2

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return (decision_variable, score_dictionary[decision_variable]) if return_score else decision_variable
    # endregion
