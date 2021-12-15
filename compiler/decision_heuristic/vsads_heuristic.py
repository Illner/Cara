# Import
from compiler.solver import Solver
from typing import List, Set, Dict, Union, Tuple
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.compiler.heuristic_exception as h_exception


class VsadsHeuristic(DecisionHeuristicAbstract):
    """
    VSADS - decision heuristic
    """

    """
    Private bool vsids_d4_version
    Private float p_constant_factor
    Private float q_constant_factor
    Private bool ignore_binary_clauses
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, ignore_binary_clauses: bool,
                 p_constant_factor: float, q_constant_factor: float, vsids_d4_version: bool = True):
        super().__init__(preselection_heuristic)

        self.__p_constant_factor: float = p_constant_factor
        self.__q_constant_factor: float = q_constant_factor
        self.__vsids_d4_version: bool = vsids_d4_version
        self.__ignore_binary_clauses: bool = ignore_binary_clauses

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int],
                              depth: int, additional_score_dictionary: Union[Dict[int, int], None] = None,
                              max_number_of_returned_decision_variables: Union[int, None] = 1) -> Union[int, List[int]]:
        # Returning more decision variables is not supported
        if max_number_of_returned_decision_variables != 1:
            raise h_exception.DecisionHeuristicDoesNotSupportReturningMoreDecisionVariablesException()

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        vsids_score_list = solver.get_vsids_score(d4_version=self.__vsids_d4_version)

        # key: variable, value: ([additional_score], score)
        score_dictionary: Dict[int, Union[float, Tuple[int, float]]] = dict()

        # Compute score
        for variable in preselected_variable_set:
            # DLCS
            positive_score = incidence_graph.literal_number_of_occurrences(literal=variable,
                                                                           ignore_binary_clauses=self.__ignore_binary_clauses)
            negative_score = incidence_graph.literal_number_of_occurrences(literal=(-variable),
                                                                           ignore_binary_clauses=self.__ignore_binary_clauses)

            # Binary clauses are ignored
            if self.__ignore_binary_clauses:
                positive_score, _ = positive_score
                negative_score, _ = negative_score

            score_dlcs = positive_score + negative_score

            # VSIDS
            score_vsids = vsids_score_list[variable - 1]

            # VSADS
            score_vsads = self.__p_constant_factor * score_vsids + self.__q_constant_factor * score_dlcs

            additional_score: Union[int, None] = None
            # Additional score is used
            if additional_score_dictionary is not None:
                if variable in additional_score_dictionary:
                    additional_score = additional_score_dictionary[variable]
                else:
                    raise h_exception.InvalidAdditionalScoreDictionaryException(variable=variable,
                                                                                additional_score_dictionary=additional_score_dictionary)

            if additional_score is None:
                score_dictionary[variable] = score_vsads
            else:
                score_dictionary[variable] = additional_score, score_vsads

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return decision_variable
    # endregion
