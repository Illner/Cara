# Import
import math
from typing import Set, Dict, Union
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract
from compiler_statistics.compiler.preselection_heuristic_statistics import PreselectionHeuristicStatistics

# Import exception
import exception.compiler.heuristic_exception as h_exception


class ClauseReductionApproximationHeuristic(PreselectionHeuristicAbstract):
    """
    Clause reduction approximation (CRA) - preselection heuristic
    """

    """
    Private float rank
    Private int total_number_of_variables
    Private int number_of_returned_variables
    """

    def __init__(self, rank: float, total_number_of_variables: int, number_of_returned_variables: Union[int, None] = None,
                 statistics: Union[PreselectionHeuristicStatistics, None] = None):
        super().__init__(statistics)

        self.__rank: float = rank
        self.__total_number_of_variables: int = total_number_of_variables

        # The number of returned variables is explicitly mentioned
        if number_of_returned_variables is not None:
            self.__number_of_returned_variables: int = number_of_returned_variables
        else:
            self.__number_of_returned_variables: int = math.ceil(self.__rank * self.__total_number_of_variables)

    # region Override method
    def preselect_variables(self, variable_restriction_set: Union[Set[int], None], incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        self._statistics.get_preselected_variables.start_stopwatch()    # timer (start)

        variable_restriction_set = incidence_graph._variable_set if variable_restriction_set is None else variable_restriction_set

        approximated_set_dictionary: Dict[int, Set[int]] = dict()           # key: literal, value: set of literals
        occurrences_in_binary_clauses_dictionary: Dict[int, int] = dict()   # key: literal, value: number of binary clauses where the literal occurs

        if len(variable_restriction_set) <= self.__number_of_returned_variables:
            self._update_statistics(preselected_variable_set=variable_restriction_set,
                                    variable_restriction_set=variable_restriction_set)

            self._statistics.get_preselected_variables.stop_stopwatch()     # timer (stop)
            return variable_restriction_set

        # Compute the approximated set
        for binary_clause_id in incidence_graph.get_binary_clause_set(copy=False):
            clause = list(incidence_graph.get_clause(binary_clause_id, copy=False))

            # The clause is not binary
            if len(clause) != 2:
                raise h_exception.ClauseIsNotBinaryException(clause)

            # occurrences_in_binary_clauses_dictionary
            for lit in clause:
                if lit not in occurrences_in_binary_clauses_dictionary:
                    occurrences_in_binary_clauses_dictionary[lit] = 1
                else:
                    occurrences_in_binary_clauses_dictionary[lit] += 1

            lit_1, lit_2 = clause[0], clause[1]
            if (abs(lit_1) not in variable_restriction_set) and (abs(lit_2) not in variable_restriction_set):
                continue

            temp_list = [[lit_1, lit_2], [lit_2, lit_1]]
            for l_1, l_2 in temp_list:
                if l_1 not in approximated_set_dictionary:
                    approximated_set_dictionary[l_1] = set()

                approximated_set_dictionary[l_1].add(-l_2)

        def compute_score_for_literal(literal_func: int) -> int:
            approximated_set_dictionary_func = set()
            if literal_func in approximated_set_dictionary:
                approximated_set_dictionary_func = approximated_set_dictionary[literal_func]

            score_func = incidence_graph.literal_set_number_of_occurrences(approximated_set_dictionary_func)
            for literal in approximated_set_dictionary_func:
                if literal in occurrences_in_binary_clauses_dictionary:
                    score_func -= occurrences_in_binary_clauses_dictionary[literal]

            return score_func

        score_dictionary: Dict[int, int] = dict()   # key: variable, value: score of the variable

        # Compute score
        for variable in variable_restriction_set:
            score = compute_score_for_literal(variable) * compute_score_for_literal(-variable)
            score_dictionary[variable] = score

        # Pick the best ones
        variable_set = sorted(score_dictionary, key=score_dictionary.get, reverse=True)
        variable_set = set(variable_set[:self.__number_of_returned_variables])

        self._update_statistics(preselected_variable_set=variable_set,
                                variable_restriction_set=variable_restriction_set)

        self._statistics.get_preselected_variables.stop_stopwatch()     # timer (stop)
        return variable_set
    # endregion
