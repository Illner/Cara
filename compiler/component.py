# Import
from formula.cnf import Cnf
from compiler.solver import Solver
from circuit.circuit import Circuit
from formula.incidence_graph import IncidenceGraph
from compiler.hypergraph_partitioning import HypergraphPartitioning
from typing import Set, Dict, List, Tuple, Union

# Import exception
import exception.cara_exception as ca_exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum


class Component:
    """
    Component
    """

    """
    Private Solver solver
    Private Circuit circuit
    Private IncidenceGraph incidence_graph
    Private HypergraphPartitioning hypergraph_partitioning
    
    Private ImpliedLiteralsEnum implied_literals_enum
    
    Private List[int] assignment_list
    """

    def __init__(self, cnf: Cnf, assignment_list: List[int], circuit: Circuit,
                 incidence_graph: IncidenceGraph, hypergraph_partitioning: HypergraphPartitioning,
                 sat_solver_enum: ss_enum.SatSolverEnum, implied_literals_enum: il_enum.ImpliedLiteralsEnum):
        self.__circuit: Circuit = circuit
        self.__incidence_graph: IncidenceGraph = incidence_graph
        self.__hypergraph_partitioning: HypergraphPartitioning = hypergraph_partitioning

        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum

        clause_id_set = self.__incidence_graph.clause_id_set()
        self.__solver: Solver = Solver(cnf, clause_id_set, sat_solver_enum)

        self.__assignment_list: List[int] = assignment_list

    # region Public
    def create_circuit(self) -> int:
        """
        :return: the root's id of the created circuit
        """

        # Get a new cut set
        cut_set = self.__hypergraph_partitioning.get_cut_set(self.__incidence_graph, self.__solver, self.__assignment_list)
        sorted_cut_set = self.__sort_cut_set(cut_set)

        return self.__create_circuit(sorted_cut_set)
    # endregion

    # region Private
    def __get_implied_literals(self) -> Union[Set[int], None]:
        """
        Return a set of implied literals based on the assignment and implied_literals_enum.
        None is returned if the formula is unsatisfiable.
        :return: a set of implied literals
        """

        # NONE
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.NONE:
            return set()

        # BCP
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.BCP:
            return self.__solver.unit_propagation(self.__assignment_list)

        # IMPLICIT_BCP
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.IMPLICIT_BCP:
            return self.__solver.iterative_implicit_unit_propagation(self.__assignment_list)

        # BACKBONE
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.BACKBONE:
            # TODO BACKBONE
            pass

        raise ca_exception.FunctionNotImplementedException("get_implied_literals",
                                                           f"this type of getting implied literals ({self.__implied_literals_enum.name}) is not implemented")

    def __sort_cut_set(self, cut_set: Set[int]) -> List[int]:
        """
        Sort the cut set based on the heuristic.
        The list is sorted in increasing order (the best variable is at the end of the list).
        :param cut_set: the cut set
        :return: the sorted cut set
        """

        # TODO Sort cut set
        return list(cut_set)

    def __exist_more_components(self) -> bool:
        """
        Check if more components exist
        :return: True if more components exist, otherwise False is returned
        """

        return True if self.__incidence_graph.number_of_components() > 1 else False

    def __create_circuit(self, cut_set: List[int]) -> int:
        """
        :return: the root's id of the created circuit
        """

        decision_variable = cut_set.pop()

        # TODO Create circuit
        pass
    # endregion
