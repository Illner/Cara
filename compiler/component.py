# Import
from formula.cnf import Cnf
from compiler.solver import Solver
from circuit.circuit import Circuit
from formula.incidence_graph import IncidenceGraph
from compiler.hypergraph_partitioning import HypergraphPartitioning

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
    """

    def __init__(self, cnf: Cnf, circuit: Circuit,
                 incidence_graph: IncidenceGraph, hypergraph_partitioning: HypergraphPartitioning,
                 sat_solver_enum: ss_enum.SatSolverEnum, implied_literals_enum: il_enum.ImpliedLiteralsEnum):
        self.__circuit: Circuit = circuit
        self.__incidence_graph: IncidenceGraph = incidence_graph
        self.__hypergraph_partitioning: HypergraphPartitioning = hypergraph_partitioning

        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum

        clause_id_set = self.__incidence_graph.clause_id_set()
        self.__solver: Solver = Solver(cnf, clause_id_set, sat_solver_enum)

    # region Public
    def create_circuit(self) -> int:
        pass
    # endregion
