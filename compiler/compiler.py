# Import
from formula.cnf import Cnf
from circuit.circuit import Circuit
from typing import Set, Tuple, Union
from compiler.component import Component
from formula.incidence_graph import IncidenceGraph
from compiler.hypergraph_partitioning import HypergraphPartitioning

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


class Compiler:
    """
    Compiler
    """

    """
    Private Cnf cnf
    Private bool smooth
    Private Circuit circuit
    Private float new_cut_set_threshold
    Private HypergraphPartitioning hypergraph_partitioning
    
    Private SatSolverEnum sat_solver_enum
    Private ImpliedLiteralsEnum implied_literals_enum
    Private HypergraphPartitioningCacheEnum hp_cache_enum
    Private HypergraphPartitioningSoftwareEnum hp_software_enum
    Private HypergraphPartitioningNodeWeightEnum hp_node_weight_type_enum
    Private HypergraphPartitioningHyperedgeWeightEnum hp_hyperedge_weight_type_enum
    Private HypergraphPartitioningVariableSimplificationEnum hp_variable_simplification_enum
    """

    def __init__(self, cnf: Cnf,
                 smooth: bool,
                 ub_factor: float,
                 new_cut_set_threshold: float,
                 sat_solver_enum: ss_enum.SatSolverEnum,
                 implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                 hp_cache_enum: hpc_enum.HypergraphPartitioningCacheEnum,
                 hp_software_enum: hps_enum.HypergraphPartitioningSoftwareEnum,
                 hp_node_weight_type_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum,
                 hp_hyperedge_weight_type_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum,
                 hp_variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum,
                 hp_limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                 hp_limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]] = (None, None)):
        self.__cnf: Cnf = cnf
        self.__smooth: bool = smooth
        self.__circuit: Circuit = Circuit()
        self.__new_cut_set_threshold: float = new_cut_set_threshold

        self.__sat_solver_enum: ss_enum.SatSolverEnum = sat_solver_enum
        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum

        self.__hypergraph_partitioning = HypergraphPartitioning(cnf=self.__cnf,
                                                                ub_factor=ub_factor,
                                                                cache_enum=hp_cache_enum,
                                                                software_enum=hp_software_enum,
                                                                node_weight_enum=hp_node_weight_type_enum,
                                                                hyperedge_weight_enum=hp_hyperedge_weight_type_enum,
                                                                variable_simplification_enum=hp_variable_simplification_enum,
                                                                limit_number_of_clauses_cache=hp_limit_number_of_clauses_cache,
                                                                limit_number_of_variables_cache=hp_limit_number_of_variables_cache)

    # region Public
    def create_circuit(self) -> Circuit:
        """
        :return: the created circuit
        """

        incidence_graph: IncidenceGraph = self.__cnf.get_incidence_graph()
        incidence_graph_set: Set[IncidenceGraph] = {incidence_graph}

        # More components exist
        if incidence_graph.number_of_components() > 1:
            incidence_graph_set = incidence_graph.create_incidence_graphs_for_components()

        node_id_set: Set[int] = set()
        for incidence_graph in incidence_graph_set:
            component = Component(cnf=self.__cnf,
                                  assignment_list=[],
                                  circuit=self.__circuit,
                                  new_cut_set_threshold=self.__new_cut_set_threshold,
                                  incidence_graph=incidence_graph,
                                  hypergraph_partitioning=self.__hypergraph_partitioning,
                                  sat_solver_enum=self.__sat_solver_enum,
                                  implied_literals_enum=self.__implied_literals_enum)
            node_id = component.create_circuit()
            node_id_set.add(node_id)

        # More components have to be connected
        if len(node_id_set) > 1:
            root_id = self.__circuit.create_and_node(node_id_set)
            self.__circuit.set_root(root_id)
        # Only one component exists
        else:
            root_id = (list(node_id_set))[0]
            self.__circuit.set_root(root_id)

        # Smooth
        if self.__smooth:
            self.__circuit.smooth()

        return self.circuit
    # endregion

    # region Property
    @property
    def circuit(self):
        return self.__circuit
    # endregion
