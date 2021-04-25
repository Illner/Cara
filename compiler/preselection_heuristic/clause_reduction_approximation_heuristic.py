# Import
import math
from typing import Set, Dict
from formula.incidence_graph import IncidenceGraph
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.compiler.compiler_exception as c_exception


class ClauseReductionApproximationHeuristic(PreselectionHeuristicAbstract):
    """
    Clause reduction approximation (CRA) - preselection heuristic
    """

    """
    Private float rank
    Private int total_number_of_variables
    Private int number_of_returned_variables
    """

    def __init__(self, rank: float, total_number_of_variables: int):
        super().__init__()

        self.__rank: float = rank
        self.__total_number_of_variables: int = total_number_of_variables
        self.__number_of_returned_variables: int = math.ceil(self.__rank * self.__total_number_of_variables)

    # region Override method
    def preselect_variables(self, incidence_graph: IncidenceGraph, depth: int) -> Set[int]:
        approximated_set_dictionary: Dict[int, Set[int]] = dict()           # key: literal, value: set of literals
        occurrences_in_binary_clauses_dictionary: Dict[int, int] = dict()   # key: literal, value: number of binary clauses where the literal occurs

        if incidence_graph.number_of_variables() <= self.__number_of_returned_variables:
            return incidence_graph.variable_set(copy=False)

        # Get the approximated set
        for binary_clause_id in incidence_graph.get_binary_clause_set(copy=False):
            clause = list(incidence_graph.get_clause(binary_clause_id))

            # The clause is not binary
            if len(clause) != 2:
                raise c_exception.ClauseIsNotBinaryException(clause)

            temp_list = [[clause[0], clause[1]], [clause[1], clause[0]]]
            for lit_1, lit_2 in temp_list:
                if lit_1 not in approximated_set_dictionary:
                    approximated_set_dictionary[lit_1] = set()
                    occurrences_in_binary_clauses_dictionary[lit_1] = 0

                approximated_set_dictionary[lit_1].add(-lit_2)
                occurrences_in_binary_clauses_dictionary[lit_1] += 1

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
        for variable in incidence_graph.variable_set(copy=False):
            score = compute_score_for_literal(variable) * compute_score_for_literal(-variable)
            score_dictionary[variable] = score

        # Pick the best ones
        temp = sorted(score_dictionary.items(), key=lambda item: item[1], reverse=True)
        temp = [item[0] for item in temp]
        temp = set(temp[:self.__number_of_returned_variables])

        return temp
    # endregion
