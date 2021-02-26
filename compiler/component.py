# Import
from formula.cnf import Cnf
from compiler.solver import Solver
from circuit.circuit import Circuit
from compiler.compiler import Compiler
from typing import Set, Dict, List, Tuple, Union

# Import exception
import exception.cara_exception as ca_exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.implied_literals_enum as il_enum


class Component:
    """
    Component
    """

    """
    Private Cnf cnf
    Private Solver solver
    Private Circuit circuit
    Private Compiler compiler
    Private DynamicGraph dynamic_graph
    
    Private Set[int] variable_set
    Private Set[int] clause_id_set
    Private Set[int] assignment_set
    Private List[int] assignment_list
    Private Set[int] unassigned_variable_set
    
    Private Set[int] satisfied_clause_set
    Private Dict<int, Set<int>> literal_satisfied_clauses_dictionary    # key: literal, value: a set of clauses that are satisfied because of the literal
    
    Private ImpliedLiteralsEnum implied_literals_enum
    Private Dict<int, Set<int>> adjacency_literal_dictionary    # key: literal, value: a set of clauses where the literal appears
    """

    # TODO CopyComponent

    def __init__(self, compiler: Compiler, clause_id_set: Set[int], assignment_list: List[int]):
        self.__compiler: Compiler = compiler
        self.__cnf: Cnf = self.__compiler.cnf
        self.__circuit: Circuit = self.__compiler.circuit
        self.__solver: Solver = Solver(self.__cnf, clause_id_set, self.__compiler.sat_solver_enum)

        self.__clause_id_set: Set[int] = clause_id_set
        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = self.__compiler.implied_literals_enum

        self.__satisfied_clause_set: Set[int] = set()
        self.__literal_satisfied_clauses_dictionary: Dict[int, Set[int]] = dict()

        # Adjacency literal dictionary
        self.__adjacency_literal_dictionary: Dict[int, Set[int]] = dict()
        self.__variable_set: Set[int] = set()
        for clause_id in clause_id_set:
            clause_set_temp = self.__cnf._get_clause(clause_id)
            for lit in clause_set_temp:
                if lit not in self.__adjacency_literal_dictionary:
                    self.__adjacency_literal_dictionary[lit] = {clause_id}
                else:
                    self.__adjacency_literal_dictionary[lit].add(clause_id)

                self.__variable_set.add(abs(lit))

                # Check if the clause is satisfiable
                if lit in assignment_list:
                    self.__satisfied_clause_set.add(clause_id)

        self.__assignment_list: List[int] = assignment_list
        self.__assignment_set: Set[int] = set(assignment_list)
        self.__unassigned_variable_set: Set[int] = self.__variable_set.difference(self.__assignment_set)

        self.__create_dynamic_graph()

    # region Private method
    def __create_dynamic_graph(self) -> None:
        """
        Create a dynamic graph
        :return: None
        """

        # TODO
        pass

    def __get_implied_literals(self) -> Union[Set[int], None]:
        """
        Return a set of implied literals based on the assignment and implied_literals_enum.
        If the formula is unsatisfiable, None is returned.
        :return: a set of implied literals
        """

        is_sat = self.__solver.is_satisfiable(self.__assignment_list)

        # The formula is not satisfiable:
        if not is_sat:
            return None

        # None
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.NONE:
            return set()

        # BCP
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.BCP:
            return self.__solver.unit_propagation(self.__assignment_list)

        # IMPLICIT BCP
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.IMPLICIT_BCP:
            implicit_bcp_dictionary = self.__get_implicit_bcp_dictionary()
            implied_literal_set = set()

            for var in implicit_bcp_dictionary:
                positive_lit_temp, negative_lit_temp = implicit_bcp_dictionary[var]

                # The negative literal is an implied literal
                if positive_lit_temp is None:
                    implied_literal_set.add(-var)
                    continue

                # The positive literal is an implied literal
                if negative_lit_temp is None:
                    implied_literal_set.add(var)
                    continue

            return implied_literal_set

        # BACKBONE
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.BACKBONE:
            # TODO
            pass

        raise ca_exception.FunctionNotImplementedException("get_implied_literals", f"({self.__implied_literals_enum.name}) is not implemented")

    def __get_implicit_bcp_dictionary(self) -> Union[Dict[int, Tuple[Union[List[int], None], Union[List[int], None]]], None]:
        """
        Return the implicit BCP dictionary.
        For each variable is returned a tuple. The first element contains a set of implied literals if the variable is set to True.
        The second element of the tuple contains a set of implied literals if the variable is set to False.
        If the formula is unsatisfiable after setting a variable, None will appear in the tuple instead of a list.
        :return: the implicit BCP dictionary
        """

        return self.__solver.implicit_unit_propagation(self.__assignment_list)

    def __add_literal_to_assignment(self, literal: int) -> None:
        """
        Add the literal to the partial assignment.
        If the literal already exists in the assignment, raise an exception (LiteralAlreadyExistsInAssignmentException).
        If the opposite literal already exists in the assignment, raise an exception (OppositeLiteralAlreadyExistsInAssignmentException).
        :param literal: the literal
        :return: None
        """

        # The literal already exists in the assignment
        if literal in self.__assignment_set:
            raise c_exception.LiteralAlreadyExistsInAssignmentException(literal)

        # The opposite literal already exists in the assignment
        if -literal in self.__assignment_set:
            raise c_exception.OppositeLiteralAlreadyExistsInAssignmentException(literal)

        self.__assignment_list.append(literal)
        self.__assignment_set.add(literal)
        self.__unassigned_variable_set.remove(abs(literal))

        # Satisfied clauses
        self.__literal_satisfied_clauses_dictionary[literal] = set()
        for clause_id in self.__adjacency_literal_dictionary[literal]:
            # The clause is already satisfied
            if clause_id in self.__satisfied_clause_set:
                continue

            self.__satisfied_clause_set.add(clause_id)
            self.__literal_satisfied_clauses_dictionary[literal].add(clause_id)

        # TODO Graph

    def __remove_literal_from_assignment(self, literal: int) -> None:
        """
        Remove the literal from the partial assignment.
        If the literal does not exist in the assignment, raise an exception (LiteralDoesNotExistInAssignmentException).
        If the assignment is empty, raise an exception (InconsistentAssignmentException).
        If the literal is not on the top of the stack (assignment), raise an exception (InconsistentAssignmentException).
        :param literal: the literal
        :return: None
        """

        # The literal does not exist in the assignment
        if literal not in self.__assignment_set:
            raise c_exception.LiteralDoesNotExistInAssignmentException(literal)

        # The assignment is empty
        if not self.__assignment_set:
            raise c_exception.InconsistentAssignmentException(f"trying to remove the literal ({literal}) from the empty assignment")

        # The literal is not on the top of the stack (assignment)
        # TODO check len > 0
        if self.__assignment_list[-1] != literal:
            raise c_exception.InconsistentAssignmentException(f"trying to remove the literal ({literal}) which is not on the top of the stack")

        self.__assignment_list.pop()
        self.__assignment_set.remove(literal)
        self.__unassigned_variable_set.add(abs(literal))

        # Satisfied clauses
        self.__satisfied_clause_set.difference_update(self.__literal_satisfied_clauses_dictionary[literal])
        del self.__literal_satisfied_clauses_dictionary[literal]

        # TODO Graph

    def __all_variables_are_assigned(self) -> bool:
        """
        Check if all variables are assigned
        :return: True if all variables which appear in the formula are assigned, otherwise False is returned
        """

        return False if self.__unassigned_variable_set else True

    def __sort_cut_set(self, cut_set: Set[int]) -> List[int]:
        """
        Sort the cut set based on the heuristic.
        The list is sorted in increasing order (the best variable is at the end of the list).
        :param cut_set: the cut set
        :return: the sorted cut set
        """

        # TODO
        return list(cut_set)

    def __exist_more_components(self) -> bool:
        """
        Check if more components exist
        :return: True if more components exist, otherwise False is returned
        """

        # TODO
        return False

    def __create_circuit(self, cut_set: List[int]) -> int:
        decision_variable = cut_set.pop()

        # TODO
        pass
    # endregion

    # region Public method
    def create_circuit(self) -> int:
        """
        Create a circuit of the formula
        :return: the root's ID of the circuit
        """

        implied_literal_set = self.__get_implied_literals()

        # The formula is unsatisfiable
        if implied_literal_set is None:
            return self.__circuit.create_constant_leaf(False)

        # Assign implied literals
        child_id_set = set()
        for lit in implied_literal_set:
            self.__add_literal_to_assignment(lit)
            node_id_temp = self.__circuit.create_literal_leaf(lit)
            child_id_set.add(node_id_temp)

        # The formula is satisfied
        if self.__all_variables_are_assigned():
            return self.__circuit.create_and_node(child_id_set)

        # Just one component exists
        if not self.__exist_more_components():
            cut_set = self.__cnf.hypergraph.get_cut_set(self.__clause_id_set, self.__assignment_list)
            sorted_cut_set = self.__sort_cut_set(cut_set)

            node_id = self.__create_circuit(sorted_cut_set)
            child_id_set.add(node_id)
            return self.__circuit.create_and_node(child_id_set)
        # More components exist
        else:
            # TODO
            pass
    # endregion
