# Import
from compiler.solver import Solver
from typing import List, Set, Dict, Tuple, Union
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.cara_exception as c_exception


class RenamableHornHeuristic(DecisionHeuristicAbstract):
    """
    Renamable Horn - decision heuristic
    """

    """
    Private bool ignore_binary_clauses
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, ignore_binary_clauses: bool):
        self.__preselection_heuristic = preselection_heuristic
        super().__init__(preselection_heuristic)

        self.__ignore_binary_clauses: bool = ignore_binary_clauses

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int) -> int:
        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        is_renamable_horn, conflict_structure = incidence_graph.is_renamable_horn_formula_using_implication_graph()

        if is_renamable_horn:
            raise c_exception.SomethingWrongException("RenamableHornHeuristic - the formula is renamable Horn")

        conflict_variable_set, conflict_variable_component_dictionary, component_number_of_conflict_variables_dictionary = conflict_structure

        intersection_set = conflict_variable_set.intersection(preselected_variable_set)
        if not intersection_set:
            intersection_set = conflict_variable_set

        # key: variable, value: (number of conflicts in the strongly connected component, DLCS, DLIS)
        score_dictionary: Dict[int, Union[Tuple[int, int, int], Tuple[int, int, int, int, int]]] = dict()

        # Compute score
        for variable in intersection_set:
            component = conflict_variable_component_dictionary[variable]
            number_of_conflict_variables = component_number_of_conflict_variables_dictionary[component]

            positive_score = incidence_graph.literal_number_of_occurrences(literal=variable, ignore_binary_clauses=self.__ignore_binary_clauses)
            negative_score = incidence_graph.literal_number_of_occurrences(literal=(-variable), ignore_binary_clauses=self.__ignore_binary_clauses)

            # Binary clauses are ignored
            if self.__ignore_binary_clauses:
                dlcs_1 = sum([positive_score[0], negative_score[0]])
                dlcs_2 = sum([positive_score[1], negative_score[1]])
                dlis_1 = max([positive_score[0], negative_score[0]])
                dlis_2 = max([positive_score[1], negative_score[1]])

                score_dictionary[variable] = number_of_conflict_variables, dlcs_1, dlcs_2, dlis_1, dlis_2
            else:
                dlcs = sum([positive_score, negative_score])
                dlis = max([positive_score, negative_score])

                score_dictionary[variable] = number_of_conflict_variables, dlcs, dlis

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return decision_variable
    # endregion
