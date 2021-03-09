# Import
from formula.cnf import Cnf
from pysat.formula import CNF
from other.sorted_list import SortedList
from typing import Set, Dict, List, Tuple, Union
from pysat.solvers import Minisat22, Glucose4, Lingeling, Cadical

# Import exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.backbones_enum as b_enum
import compiler.enum.sat_solver_enum as ss_enum


class Solver:
    """
    SAT Solver
    """

    """
    Private CNF cnf
    Private Set<int> variable_set
    Private Set<int> implied_literal_set        # implied literals (implicit BCP) without any assumption
    Private SatSolverEnum sat_solver_enum

    Private Backbones backbones

    Private Solver sat_main                     # main SAT solver
    Private Solver sat_unit_propagation         # for unit propagation

    Private Dict<str, Dict<int, Tuple<Set<int>, Set<int>>>> implicit_bcp_dictionary_cache   # key = {number}+, value: implicit_bcp_dictionary
    """

    def __init__(self, cnf: Cnf,
                 clause_id_set: Union[Set[int], None],
                 backbones_chunk_size: Union[int, float],
                 sat_solver_enum: ss_enum.SatSolverEnum,
                 backbones_enum: b_enum.BackbonesEnum):
        self.__cnf: CNF = CNF()
        self.__sat_solver_enum: ss_enum.SatSolverEnum = sat_solver_enum

        # Create a subformula
        # The clause_id_set is implicitly given
        if clause_id_set is not None:
            for clause_id in clause_id_set:
                self.__cnf.append(cnf._get_clause(clause_id))
            self.__variable_set: Set[int] = cnf.get_variable_in_clauses(clause_id_set)
        # The whole formula is taken into account
        else:
            for clause_id in range(cnf.real_number_of_clauses):
                self.__cnf.append(cnf._get_clause(clause_id))
            self.__variable_set: Set[int] = cnf._get_variable_set(copy=True)

        # Cache
        self.__implicit_bcp_dictionary_cache: \
            Dict[str, Union[Dict[int, Tuple[Union[Set[int], None], Union[Set[int], None]]], None]] = dict()

        # Create SAT solvers
        self.__sat_main = None
        self.__sat_unit_propagation = None
        # MiniSat
        if self.__sat_solver_enum == ss_enum.SatSolverEnum.MiniSAT:
            self.__sat_main = Minisat22(bootstrap_with=self.__cnf.clauses, use_timer=True)
            self.__sat_unit_propagation = self.__sat_main
        # Glucose
        elif self.__sat_solver_enum == ss_enum.SatSolverEnum.Glucose:
            self.__sat_main = Glucose4(bootstrap_with=self.__cnf.clauses, use_timer=True)
            self.__sat_unit_propagation = self.__sat_main
        # Lingeling
        elif self.__sat_solver_enum == ss_enum.SatSolverEnum.Lingeling:
            self.__sat_main = Lingeling(bootstrap_with=self.__cnf.clauses, use_timer=True)
            self.__sat_unit_propagation = Minisat22(bootstrap_with=self.__cnf.clauses, use_timer=True)
        # CaDiCal
        elif self.__sat_solver_enum == ss_enum.SatSolverEnum.CaDiCal:
            self.__sat_main = Cadical(bootstrap_with=self.__cnf.clauses, use_timer=True)
            self.__sat_unit_propagation = Minisat22(bootstrap_with=self.__cnf.clauses, use_timer=True)
        # Not supported
        else:
            raise c_exception.SatSolverIsNotSupportedException(self.__sat_solver_enum)

        # Implied literals without any assumption
        self.__implied_literal_set: Set[int] = set()
        temp = self.iterative_implicit_unit_propagation([])
        if temp is not None:
            self.__implied_literal_set = temp

        # Backbones
        from compiler.backbones import Backbones
        self.__backbones = Backbones(self, backbones_enum, backbones_chunk_size)

    # region Public method
    def is_satisfiable(self, assignment_list: List[int]) -> bool:
        """
        Check if the formula is satisfiable for the assignment
        :param assignment_list: the assignment
        :return: True if the formula is satisfiable, otherwise False is returned
        """

        return self.__sat_main.solve(assumptions=self.__create_assumption_list(assignment_list))

    def get_model(self, assignment_list: List[int]) -> Union[List[int], None]:
        """
        Return a satisfying assignment.
        If the formula for the assignment is unsatisfiable, return None.
        :param assignment_list: the partial assignment
        :return: a complete assignment or None if the formula is unsatisfiable
        """

        self.__sat_main.solve(assumptions=self.__create_assumption_list(assignment_list))
        return self.__sat_main.get_model()

    def unit_propagation(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Do unit propagation (boolean constraint propagation).
        If the formula for the assignment is unsatisfiable, return None.
        :param assignment_list: the assignment
        :return: a set of implied literals or None if the formula is unsatisfiable
        """

        is_sat, implied_literals = self.__sat_unit_propagation.propagate(assumptions=self.__create_assumption_list(assignment_list))

        # The formula is not satisfiable
        if not is_sat:
            return None

        implied_literals = (set(implied_literals)).union(self.__implied_literal_set)
        implied_literals.difference_update(set(assignment_list))

        return implied_literals

    def implicit_unit_propagation(self, assignment_list: List[int]) -> Union[Dict[int, Tuple[Union[Set[int], None], Union[Set[int], None]]], None]:
        """
        Do implicit unit propagation (implicit boolean constraint propagation).
        If the formula for the assignment is unsatisfiable, return None.
        :param assignment_list: the assignment
        :return: For each variable is returned a tuple. The first element contains a set of implied literals if the variable is set to True,
        the second element of the tuple contains a set of implied literals if the variable is set to False.
        If the formula is unsatisfiable after setting a variable, None will appear in the tuple instead of a set.
        """
        # TODO subset of variables

        # Cache
        key = self.__generate_key_cache(assignment_list)
        exist, value = self.__get_implicit_bcp_dictionary_cache(key)
        if exist:
            return value

        temp_set = set(map(lambda l: abs(l), assignment_list))
        variable_to_try_set = self.__variable_set.difference(temp_set)
        result_dictionary = dict()

        for var in variable_to_try_set:
            # Positive literal
            assignment_list.append(var)
            temp_positive = self.unit_propagation(assignment_list)
            assignment_list.pop()

            # Negative literal
            assignment_list.append(-var)
            temp_negative = self.unit_propagation(assignment_list)
            assignment_list.pop()

            # The formula is unsatisfiable
            if (temp_positive is None) and (temp_negative is None):
                self.__add_implicit_bcp_dictionary_cache(key, None)
                return None

            result_dictionary[var] = (temp_positive, temp_negative)

        self.__add_implicit_bcp_dictionary_cache(key, result_dictionary)
        return result_dictionary

    def iterative_implicit_unit_propagation(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Repeat implicit unit propagation (implicit boolean constraint propagation) until a new implied literal is found.
        If the formula for the assignment is unsatisfiable, return None.
        :param assignment_list: the assignment
        :return: a set of implied literals
        """

        repeat = True
        assignment_list_temp = assignment_list.copy()

        while repeat:
            repeat = False

            implicit_bcp_dictionary = self.implicit_unit_propagation(assignment_list_temp)
            # The formula is unsatisfiable
            if implicit_bcp_dictionary is None:
                return None

            for variable in implicit_bcp_dictionary:
                temp_positive, temp_negative = implicit_bcp_dictionary[variable]

                # The negative literal is implied
                if temp_positive is None:
                    assignment_list_temp.append(-variable)
                    repeat = True
                    continue

                # The positive literal is implied
                if temp_negative is None:
                    assignment_list_temp.append(variable)
                    repeat = True
                    continue

                # l_2 e (BCP u {l_1}) and l_2 e (BCP u {-l_1}) => l_2
                intersection_temp = temp_positive.intersection(temp_negative)
                if intersection_temp:
                    assignment_list_temp.extend(intersection_temp)
                    repeat = True

        implied_literals = set(assignment_list_temp)
        implied_literals.difference_update(set(assignment_list))

        return implied_literals

    def get_backbones(self, assignment_list: List[int]) -> Union[Set[int], None]:
        """
        Return a set of backbone literals for the assignment.
        If the formula is unsatisfiable, None is returned.
        :param assignment_list: the assignment
        :return: a set of backbone literals or None if the formula is unsatisfiable
        """

        backbone_literal_set = self.__backbones.get_backbones(assignment_list)

        if backbone_literal_set is None:
            return None

        backbone_literal_set.update(self.__implied_literal_set)
        backbone_literal_set.difference_update(set(assignment_list))

        return backbone_literal_set
    # endregion

    # region Private method
    def __create_assumption_list(self, assignment_list: List[int]) -> List[int]:
        return list(self.__implied_literal_set.union(set(assignment_list)))

    def __generate_key_cache(self, assignment_list: List[int]) -> str:
        """
        Generate a key for caching.
        Cache: implicit_bcp_dictionary_cache
        :param assignment_list: the assignment (can be empty)
        :return: the generated key based on the assignment
        """

        assignment_sorted_list = SortedList(assignment_list)
        return assignment_sorted_list.str_delimiter("-")

    def __add_implicit_bcp_dictionary_cache(self, key: str, implicit_bcp_dictionary) -> None:
        """
        Add a new record to the cache.
        If the record already exists in the cache, the value of the record will be updated.
        :param key: the key
        :param implicit_bcp_dictionary: the value
        :return: None
        """

        self.__implicit_bcp_dictionary_cache[key] = implicit_bcp_dictionary

    def __get_implicit_bcp_dictionary_cache(self, key: str) -> \
            Tuple[bool, Union[Dict[int, Tuple[Union[Set[int], None], Union[Set[int], None]]], None]]:
        """
        Return the value of the record with the key from the cache.
        If the record does not exist in the cache, (False, None) is returned.
        :param key: the key
        :return: (True, the record's value) if the record exists. Otherwise, (False, None) is returned.
        """

        # The record does not exist
        if key not in self.__implicit_bcp_dictionary_cache:
            return False, None

        return True, self.__implicit_bcp_dictionary_cache[key]
    # endregion

    # region Magic function
    def __del__(self):
        # Delete the main SAT Solver
        if self.__sat_main is not None:
            self.__sat_main.delete()

        # Delete the SAT solver for unit propagation
        if self.__sat_unit_propagation is not None:
            self.__sat_unit_propagation.delete()
    # endregion
