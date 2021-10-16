# Import
from compiler.solver import Solver
from typing import List, Set, Dict, Union
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
    Private bool use_total_number_of_conflict_variables
    Private DecisionHeuristicAbstract decision_heuristic
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, decision_heuristic: DecisionHeuristicAbstract,
                 use_total_number_of_conflict_variables: bool):
        super().__init__(preselection_heuristic)

        self.__decision_heuristic: DecisionHeuristicAbstract = decision_heuristic
        self.__use_total_number_of_conflict_variables: bool = use_total_number_of_conflict_variables

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int],
                              depth: int, additional_score_dictionary: Union[Dict[int, int], None] = None) -> int:
        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        is_renamable_horn, conflict_structure = incidence_graph.is_renamable_horn_formula_using_implication_graph()

        # The formula is renamable Horn
        if is_renamable_horn:
            raise c_exception.SomethingWrongException(f"RenamableHornHeuristic - the formula is renamable Horn ({incidence_graph})")

        conflict_variable_set, conflict_variable_component_dictionary, component_number_of_conflict_variables_dictionary, component_total_number_of_conflict_variables_dictionary = conflict_structure

        intersection_set = conflict_variable_set.intersection(preselected_variable_set)
        if not intersection_set:
            intersection_set = conflict_variable_set

        # Additional score
        additional_score_dictionary: Dict[int, int] = dict()
        for variable in intersection_set:
            component = conflict_variable_component_dictionary[variable]

            if self.__use_total_number_of_conflict_variables:
                number_of_conflict_variables = component_total_number_of_conflict_variables_dictionary[component]
            else:
                number_of_conflict_variables = component_number_of_conflict_variables_dictionary[component]

            additional_score_dictionary[variable] = number_of_conflict_variables

        decision_variable = self.__decision_heuristic.get_decision_variable(cut_set=intersection_set,
                                                                            incidence_graph=incidence_graph,
                                                                            solver=solver,
                                                                            assignment_list=assignment_list,
                                                                            depth=depth,
                                                                            additional_score_dictionary=additional_score_dictionary)

        return decision_variable
    # endregion
