# Import
import random
from compiler.solver import Solver
from typing import Set, List, Dict, Union
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.compiler.heuristic_exception as h_exception

# Import enum
import compiler.enum.heuristic.mixed_difference_heuristic_enum as mdf_enum


class WeightedBinariesHeuristic(DecisionHeuristicAbstract):
    """
    Weighted binaries - decision heuristic (backbone_search_heuristic = False)
    Backbone search   - decision heuristic (backbone_search_heuristic = True)
    """

    """
    Private bool backbone_search_heuristic
    Private bool weight_for_satisfied_clauses
    Private MixedDifferenceHeuristicEnum mixed_difference_heuristic_enum
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract,
                 mixed_difference_heuristic_enum: mdf_enum.MixedDifferenceHeuristicEnum,
                 weight_for_satisfied_clauses: bool, backbone_search_heuristic: bool = False):
        super().__init__(preselection_heuristic)

        self.__backbone_search_heuristic: bool = backbone_search_heuristic
        self.__weight_for_satisfied_clauses: bool = weight_for_satisfied_clauses
        self.__mixed_difference_heuristic_enum: mdf_enum.MixedDifferenceHeuristicEnum = mixed_difference_heuristic_enum

    # region Private method
    def __get_weight(self, k: int) -> float:
        """
        :return: the weight (importance) of a clause with the size k
        """

        if (k == 0) and (not self.__weight_for_satisfied_clauses):
            return 0

        return 5 ** (3-k)
    # endregion

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int],
                              depth: int, additional_score_dictionary: Union[Dict[int, int], None] = None) -> int:
        # Additional score is used
        if additional_score_dictionary is not None:
            raise h_exception.AdditionalScoreIsNotSupportedException()

        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        literal_weight_dictionary: Dict[int, int] = dict()  # key: a literal, value: weight of the literal

        # Compute weights
        for variable in incidence_graph._variable_set:
            for sign in [+1, -1]:
                literal = sign * variable

                weight = 0
                number_of_occurrences_dictionary = incidence_graph.literal_number_of_occurrences_dictionary(literal)
                for clause_length in number_of_occurrences_dictionary:
                    number_of_occurrences = number_of_occurrences_dictionary[clause_length]
                    weight += self.__get_weight(clause_length) * number_of_occurrences

                literal_weight_dictionary[literal] = weight

        implicit_bcp_dictionary = solver.implicit_unit_propagation(assignment_list=assignment_list,
                                                                   variable_restriction_set=preselected_variable_set)

        # disable_sat => the formula can be unsatisfiable
        if implicit_bcp_dictionary is None:
            return random.sample(preselected_variable_set, 1)[0]

        implied_variable, implied_literal_dictionary = DecisionHeuristicAbstract._process_implicit_bcp_dictionary(implicit_bcp_dictionary)
        if implied_variable is not None:
            return implied_variable

        literal_score_dictionary: Dict[int, int] = dict()   # key: a literal, value: score of the literal
        for literal in implied_literal_dictionary:
            literal_score_dictionary[literal] = 0

        # Compute score for literals
        for clause_id in incidence_graph._clause_id_set:
            clause = incidence_graph.get_clause(clause_id, copy=False)

            for literal in implied_literal_dictionary:
                implied_literal_set, complementary_implied_literal_set = implied_literal_dictionary[literal]

                # The clause is satisfied
                if len(clause.intersection(implied_literal_set)):
                    literal_score_dictionary[literal] += self.__get_weight(0)

                    continue

                clause_size_before = len(clause)
                changed_clause = list(clause.difference(complementary_implied_literal_set))
                clause_size_after = len(changed_clause)

                # Nothing has changed
                if clause_size_before == clause_size_after:
                    continue

                # Not a binary clause
                if clause_size_after != 2:
                    continue

                lit_1, lit_2 = changed_clause[0], changed_clause[1]
                weight_complementary_lit_1 = literal_weight_dictionary[(-1 * lit_1)]
                weight_complementary_lit_2 = literal_weight_dictionary[(-1 * lit_2)]

                # Backbone search heuristic
                if self.__backbone_search_heuristic:
                    score = weight_complementary_lit_1 * weight_complementary_lit_2
                # Weighted binaries heuristic
                else:
                    score = weight_complementary_lit_1 + weight_complementary_lit_2

                literal_score_dictionary[literal] += score

        score_dictionary = DecisionHeuristicAbstract._compute_score_mixed_difference_heuristic(literal_score_dictionary=literal_score_dictionary,
                                                                                               preselected_variable_set=preselected_variable_set,
                                                                                               mixed_difference_heuristic_enum=self.__mixed_difference_heuristic_enum)

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return decision_variable
    # endregion
