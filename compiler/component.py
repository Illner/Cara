# Import
from formula.cnf import Cnf
from compiler.solver import Solver
from circuit.circuit import Circuit
from compiler.compiler import Compiler
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
    
    """

    def __init__(self, cnf: Cnf, compiler: Compiler, circuit: Circuit,
                 incidence_graph: IncidenceGraph, hypergraph_partitioning: HypergraphPartitioning,
                 sat_solver_enum: ss_enum.SatSolverEnum, implied_literals_enum: il_enum.ImpliedLiteralsEnum):
        pass

    # region Public
    def create_circuit(self) -> int:
        pass
    # endregion
