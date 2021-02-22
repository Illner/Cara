# Import
from formula.cnf import Cnf
from circuit.circuit import Circuit
from typing import Set, Dict, List, Tuple, Union

# Import enum
import compiler.sat_solver_enum as ss_enum
import compiler.implied_literals_enum as il_enum


class Compiler:
    """
    Compiler
    """

    """
    Private Cnf cnf
    Private Circuit circuit
    Private ImpliedLiteralsEnum implied_literals_enum
    Private SatSolverEnum sat_solver_enum
    """

    def __init__(self, cnf: Cnf, implied_literals_enum: il_enum.ImpliedLiteralsEnum, sat_solver_enum: ss_enum.SatSolverEnum):
        self.__cnf: Cnf = cnf
        self.__circuit: Circuit = Circuit()
        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum
        self.__sat_solver_enum: ss_enum.SatSolverEnum = sat_solver_enum

    # region Property
    @property
    def cnf(self):
        return self.__cnf

    @property
    def circuit(self):
        return self.__circuit

    @property
    def implied_literals_enum(self):
        return self.__implied_literals_enum

    @property
    def sat_solver_enum(self):
        return self.__sat_solver_enum
    # endregion
