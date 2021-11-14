# Import
from compiler.solver import Solver
from typing import List, Set, Dict, Union
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.compiler.heuristic_exception as h_exception

# Import enum
import formula.enum.lp_formulation_objective_function_enum as lpfof_enum


class MaximumRenamableHornHeuristic(DecisionHeuristicAbstract):
    """
    Maximum renamable Horn - decision heuristic
    """

    """
    Private bool is_exact
    Private bool use_conflicts
    Private bool prefer_conflict_variables
    Private int weight_for_clauses_without_variables_in_cut_set
    
    Private DecisionHeuristicAbstract decision_heuristic
    Private LpFormulationObjectiveFunctionEnum objective_function
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, decision_heuristic: DecisionHeuristicAbstract,
                 is_exact: bool, use_conflicts: bool, prefer_conflict_variables: bool, objective_function: lpfof_enum.LpFormulationObjectiveFunctionEnum,
                 weight_for_clauses_without_variables_in_cut_set: int):
        super().__init__(preselection_heuristic)

        self.__is_exact: bool = is_exact
        self.__use_conflicts: bool = use_conflicts
        self.__prefer_conflict_variables: bool = prefer_conflict_variables
        self.__weight_for_clauses_without_variables_in_cut_set: int = weight_for_clauses_without_variables_in_cut_set

        self.__decision_heuristic: DecisionHeuristicAbstract = decision_heuristic
        self.__objective_function: lpfof_enum.LpFormulationObjectiveFunctionEnum = objective_function

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int],
                              depth: int, additional_score_dictionary: Union[Dict[int, int], None] = None) -> int:
        # Additional score is used
        if additional_score_dictionary is not None:
            raise h_exception.AdditionalScoreIsNotSupportedException()

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        is_renamable_horn, conflict_variable_set, variable_score_dictionary = incidence_graph.get_maximum_renamable_horn_subformula(is_exact=self.__is_exact,
                                                                                                                                    objective_function=self.__objective_function,
                                                                                                                                    cut_set=cut_set,
                                                                                                                                    weight_for_clauses_without_variables_in_cut_set=self.__weight_for_clauses_without_variables_in_cut_set)

        # The formula is renamable Horn
        if is_renamable_horn:
            decision_variable = self.__decision_heuristic.get_decision_variable(cut_set=preselected_variable_set,
                                                                                incidence_graph=incidence_graph,
                                                                                solver=solver,
                                                                                assignment_list=assignment_list,
                                                                                depth=depth,
                                                                                additional_score_dictionary=None)

            return decision_variable

        intersection_set = conflict_variable_set.intersection(preselected_variable_set)
        if not intersection_set:
            if self.__prefer_conflict_variables:
                intersection_set = conflict_variable_set
            else:
                intersection_set = preselected_variable_set

        decision_variable = self.__decision_heuristic.get_decision_variable(cut_set=intersection_set,
                                                                            incidence_graph=incidence_graph,
                                                                            solver=solver,
                                                                            assignment_list=assignment_list,
                                                                            depth=depth,
                                                                            additional_score_dictionary=variable_score_dictionary if self.__use_conflicts else None)

        return decision_variable
    # endregion
