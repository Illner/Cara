# Import
from compiler.solver import Solver
from typing import List, Dict, Set, Tuple, Union
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.compiler.heuristic_exception as h_exception


class JeroslowWangHeuristic(DecisionHeuristicAbstract):
    """
    Jeroslow-Wang - decision heuristic
    """

    """
    Private bool one_sided
    Private bool ignore_binary_clauses
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, one_sided: bool, ignore_binary_clauses: bool):
        super().__init__(preselection_heuristic)

        self.__one_sided: bool = one_sided
        self.__ignore_binary_clauses: bool = ignore_binary_clauses

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int,
                              additional_score_dictionary: Union[Dict[int, int], None] = None, max_number_of_returned_decision_variables: Union[int, None] = 1,
                              return_score: bool = False) -> Union[Union[int, List[int]], Tuple[Union[int, List[int]], Union[int, Tuple[int, int], Tuple[int, int, int]]]]:
        # Returning more decision variables is not supported
        if max_number_of_returned_decision_variables != 1:
            raise h_exception.DecisionHeuristicDoesNotSupportReturningMoreDecisionVariablesException()

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            decision_variable = list(preselected_variable_set)[0]
            return (decision_variable, 0) if return_score else decision_variable

        # key: variable, value: ([additional_score], score_1, [score_2])
        score_dictionary: Dict[int, Union[int, Tuple[int, int], Tuple[int, int, int]]] = dict()

        # Compute score
        for variable in preselected_variable_set:
            positive_score = incidence_graph.literal_sum_lengths_clauses(literal=variable,
                                                                         jeroslow_wang=True,
                                                                         ignore_binary_clauses=self.__ignore_binary_clauses)
            negative_score = incidence_graph.literal_sum_lengths_clauses(literal=(-variable),
                                                                         jeroslow_wang=True,
                                                                         ignore_binary_clauses=self.__ignore_binary_clauses)

            # One-sided
            if self.__one_sided:
                # Binary clauses are ignored
                if self.__ignore_binary_clauses:
                    score = max(positive_score[0], negative_score[0]), max(positive_score[1], negative_score[1])
                else:
                    score = max(positive_score, negative_score)
            # Two-sided
            else:
                # Binary clauses are ignored
                if self.__ignore_binary_clauses:
                    score = positive_score[0] + negative_score[0], positive_score[1] + negative_score[1]
                else:
                    score = positive_score + negative_score

            score_dictionary[variable] = score

            # Additional score is used
            if additional_score_dictionary is not None:
                if variable in additional_score_dictionary:
                    additional_score = additional_score_dictionary[variable]

                    if self.__ignore_binary_clauses:
                        score_dictionary[variable] = additional_score, score[0], score[1]
                    else:
                        score_dictionary[variable] = additional_score, score
                else:
                    raise h_exception.InvalidAdditionalScoreDictionaryException(variable=variable,
                                                                                additional_score_dictionary=additional_score_dictionary)

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return (decision_variable, score_dictionary[decision_variable]) if return_score else decision_variable
    # endregion
