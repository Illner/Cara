# Import
from typing import List, Set, Dict
from compiler.solver import Solver
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract


class ExactUnitPropagationCountHeuristic(DecisionHeuristicAbstract):
    """
    Exact Unit Propagation Count - decision heuristic
    """

    """
    Private int factor
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, factor: int):
        super().__init__(preselection_heuristic)

        self.__factor: int = factor

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int) -> int:
        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        implicit_bcp_dictionary = solver.implicit_unit_propagation(assignment_list=assignment_list,
                                                                   variable_restriction_set=preselected_variable_set)
        score_dictionary: Dict[int, int] = dict()   # key: variable, value: score of the variable

        # Compute score
        for variable in implicit_bcp_dictionary:
            temp_positive, temp_negative = implicit_bcp_dictionary[variable]

            if (temp_positive is None) or (temp_negative is None):
                return variable

            v_p, v_n = len(temp_positive), len(temp_negative)
            score_dictionary[variable] = self.__factor * v_p * v_n + v_p + v_n

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return decision_variable
    # endregion
