# Import
from compiler.solver import Solver
from typing import List, Set, Dict, Tuple
from formula.incidence_graph import IncidenceGraph
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.cara_exception as c_exception
import exception.compiler.heuristic_exception as h_exception

# Import enum
import compiler.enum.heuristic.mixed_difference_heuristic_enum as mdf_enum


class ClauseReductionHeuristic(DecisionHeuristicAbstract):
    """
    Clause reduction - decision heuristic
    """

    """
    Private bool weight_for_satisfied_clauses
    Private MixedDifferenceHeuristicEnum mixed_difference_heuristic_enum
    """

    def __init__(self, preselection_heuristic: PreselectionHeuristicAbstract, weight_for_satisfied_clauses: bool,
                 mixed_difference_heuristic_enum: mdf_enum.MixedDifferenceHeuristicEnum):
        super().__init__(preselection_heuristic)

        self.__weight_for_satisfied_clauses: bool = weight_for_satisfied_clauses
        self.__mixed_difference_heuristic_enum: mdf_enum.MixedDifferenceHeuristicEnum = mixed_difference_heuristic_enum

    # region Private method
    def __get_weight(self, k: int) -> float:
        """
        :return: the weight (importance) of a clause with the size k
        :raises WeightDoesNotExistForSizeOfClauseException: if the weight does not exist for this size
        """

        if k < 0:
            raise h_exception.WeightDoesNotExistForSizeOfClauseException(k)

        # Satisfied clause (= empty clause)
        if k == 0:
            if self.__weight_for_satisfied_clauses:
                return 20
            else:
                return 0

        # Unsatisfied clause (because of no unit propagation)
        if k == 1:
            return -10000

        if k == 2:
            return 1

        if k == 3:
            return 0.2

        if k == 4:
            return 0.05

        if k == 5:
            return 0.01

        if k == 6:
            return 0.003

        return 20.4514 * (0.218673 ** k)
    # endregion

    # region Override method
    def get_decision_variable(self, cut_set: Set[int], incidence_graph: IncidenceGraph, solver: Solver, assignment_list: List[int], depth: int) -> int:
        preselected_variable_set = self._get_preselected_variables(cut_set, incidence_graph, depth)

        if len(preselected_variable_set) == 1:
            return list(preselected_variable_set)[0]

        implicit_bcp_dictionary = solver.implicit_unit_propagation(assignment_list=assignment_list,
                                                                   variable_restriction_set=preselected_variable_set)
        implied_literal_dictionary: Dict[int, Tuple[Set[int], Set[int]]] = dict()   # key: a literal, value: (implied literals, complementary implied literals)

        for variable in implicit_bcp_dictionary:
            positive, negative = implicit_bcp_dictionary[variable]

            # Implied literal
            if (positive is None) or (negative is None):
                return variable

            positive_temp = positive.union({variable})
            complementary_positive_temp = set(map(lambda l: -1 * l, positive_temp))

            negative_temp = negative.union({-variable})
            complementary_negative_temp = set(map(lambda l: -1 * l, negative_temp))

            implied_literal_dictionary[variable] = positive_temp, complementary_positive_temp
            implied_literal_dictionary[-variable] = negative_temp, complementary_negative_temp

        literal_clause_size_dictionary: Dict[int, Dict[int, int]] = dict()  # key: a literal, value: (size k, number of clauses with the size k)
        for literal in implied_literal_dictionary:
            literal_clause_size_dictionary[literal] = {0: 0}

        # Get newly created clauses
        for clause_id in incidence_graph.clause_id_set(copy=False):
            clause = incidence_graph.get_clause(clause_id)

            for literal in implied_literal_dictionary:
                implied_literal_set, complementary_implied_literal_set = implied_literal_dictionary[literal]
                clause_size_dictionary = literal_clause_size_dictionary[literal]

                # The clause is satisfied
                if len(clause.intersection(implied_literal_set)):
                    clause_size_dictionary[0] += 1
                    continue

                clause_size_before = len(clause)
                clause_size_after = len(clause.difference(complementary_implied_literal_set))

                # Nothing has changed
                if clause_size_before == clause_size_after:
                    continue

                if clause_size_after not in clause_size_dictionary:
                    clause_size_dictionary[clause_size_after] = 1
                else:
                    clause_size_dictionary[clause_size_after] += 1

        literal_score_dictionary: Dict[int, int] = dict()  # key: literal, value: score of the literal

        # Compute score for literals
        for literal in literal_clause_size_dictionary:
            clause_size_dictionary = literal_clause_size_dictionary[literal]

            score = 0
            for clause_size in clause_size_dictionary:
                number_of_clauses = clause_size_dictionary[clause_size]
                score += self.__get_weight(clause_size) * number_of_clauses

            literal_score_dictionary[literal] = score

        score_dictionary: Dict[int, int] = dict()   # key: variable, value: score of the variable

        # Compute score
        for variable in preselected_variable_set:
            positive_score = literal_score_dictionary[variable]
            negative_score = literal_score_dictionary[-variable]

            # OK_SOLVER
            if self.__mixed_difference_heuristic_enum == mdf_enum.MixedDifferenceHeuristicEnum.OK_SOLVER:
                score = positive_score * negative_score
            # POSIT_SATZ
            elif self.__mixed_difference_heuristic_enum == mdf_enum.MixedDifferenceHeuristicEnum.POSIT_SATZ:
                score = 1024 * positive_score * negative_score + positive_score + negative_score
            # Not supported
            else:
                raise c_exception.FunctionNotImplementedException("get_decision_variable",
                                                                  f"this type of mixed difference heuristic ({self.__mixed_difference_heuristic_enum.name}) is not implemented")

            score_dictionary[variable] = score

        # Pick the best one
        decision_variable = max(score_dictionary, key=score_dictionary.get)

        return decision_variable
    # endregion
