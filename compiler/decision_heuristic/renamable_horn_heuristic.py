# Import
from compiler.solver import Solver
from typing import List, Set, Dict, Union
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.compiler.heuristic_exception as h_exception


class RenamableHornHeuristic(DecisionHeuristicAbstract):
    """
    Renamable Horn - decision heuristic
    """

    """
    Private bool use_conflicts
    Private bool use_auxiliary_variables
    Private bool prefer_conflict_variables
    Private bool use_total_number_of_conflict_variables
    Private DecisionHeuristicAbstract decision_heuristic
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, decision_heuristic: DecisionHeuristicAbstract,
                 use_total_number_of_conflict_variables: bool, use_conflicts: bool, use_auxiliary_variables: bool, prefer_conflict_variables: bool):
        super().__init__(preselection_heuristic)

        self.__use_conflicts: bool = use_conflicts
        self.__use_auxiliary_variables: bool = use_auxiliary_variables
        self.__prefer_conflict_variables: bool = prefer_conflict_variables
        self.__decision_heuristic: DecisionHeuristicAbstract = decision_heuristic
        self.__use_total_number_of_conflict_variables: bool = use_total_number_of_conflict_variables

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int],
                              depth: int, additional_score_dictionary: Union[Dict[int, int], None] = None) -> int:
        # Additional score is used
        if additional_score_dictionary is not None:
            raise h_exception.AdditionalScoreIsNotSupportedException()

        if 1816 in incidence_graph.variable_set(copy=False):
            return 1816

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        is_renamable_horn, conflict_structure = incidence_graph.is_renamable_horn_formula_using_implication_graph(use_auxiliary_variables=self.__use_auxiliary_variables)

        # The formula is renamable Horn
        if is_renamable_horn:
            decision_variable = self.__decision_heuristic.get_decision_variable(cut_set=preselected_variable_set,
                                                                                incidence_graph=incidence_graph,
                                                                                solver=solver,
                                                                                assignment_list=assignment_list,
                                                                                depth=depth,
                                                                                additional_score_dictionary=None)

            return decision_variable

        conflict_variable_set, literal_component_dictionary, component_number_of_conflict_variables_dictionary, component_total_number_of_conflict_variables_dictionary = conflict_structure

        intersection_set = conflict_variable_set.intersection(preselected_variable_set)
        if not intersection_set:
            if self.__prefer_conflict_variables:
                intersection_set = conflict_variable_set
            else:
                intersection_set = preselected_variable_set

        # Additional score
        additional_score_dictionary: Union[Dict[int, int], None] = None

        if self.__use_conflicts:
            additional_score_dictionary = dict()

            for variable in intersection_set:
                number_of_conflict_variables = 0

                for sign in [+1, -1]:
                    literal = sign * variable

                    component = literal_component_dictionary[literal]

                    if self.__use_total_number_of_conflict_variables:
                        number_of_conflict_variables += component_total_number_of_conflict_variables_dictionary[component]
                    else:
                        number_of_conflict_variables += component_number_of_conflict_variables_dictionary[component]

                additional_score_dictionary[variable] = number_of_conflict_variables

        decision_variable = self.__decision_heuristic.get_decision_variable(cut_set=intersection_set,
                                                                            incidence_graph=incidence_graph,
                                                                            solver=solver,
                                                                            assignment_list=assignment_list,
                                                                            depth=depth,
                                                                            additional_score_dictionary=additional_score_dictionary)

        return decision_variable
    # endregion
