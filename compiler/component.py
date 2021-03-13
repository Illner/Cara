# Import
from formula.cnf import Cnf
from compiler.solver import Solver
from circuit.circuit import Circuit
from typing import Set, List, Union
from formula.incidence_graph import IncidenceGraph
from compiler_statistics.statistics import Statistics
from compiler.hypergraph_partitioning import HypergraphPartitioning
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract

# Import exception
import exception.cara_exception as ca_exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum

# TODO Cut set heuristic


class Component:
    """
    Component
    """

    """
    Private Cnf cnf
    Private Solver solver
    Private Circuit circuit
    Private Statistics statistics
    Private float new_cut_set_threshold
    Private IncidenceGraph incidence_graph
    Private ComponentCachingAbstract component_caching
    Private HypergraphPartitioning hypergraph_partitioning
    
    Private SatSolverEnum sat_solver_enum
    Private ImpliedLiteralsEnum implied_literals_enum
    
    Private List<int> assignment_list
    """

    def __init__(self, cnf: Cnf,
                 assignment_list: List[int],
                 circuit: Circuit,
                 new_cut_set_threshold: float,
                 incidence_graph: IncidenceGraph,
                 component_caching: ComponentCachingAbstract,
                 hypergraph_partitioning: HypergraphPartitioning,
                 sat_solver_enum: ss_enum.SatSolverEnum,
                 implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                 statistics: Statistics):
        self.__cnf: Cnf = cnf
        self.__circuit: Circuit = circuit
        self.__incidence_graph: IncidenceGraph = incidence_graph
        self.__new_cut_set_threshold: float = new_cut_set_threshold
        self.__component_caching: ComponentCachingAbstract = component_caching
        self.__hypergraph_partitioning: HypergraphPartitioning = hypergraph_partitioning

        self.__sat_solver_enum: ss_enum.SatSolverEnum = sat_solver_enum
        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum

        self.__statistics: Statistics = statistics

        clause_id_set = self.__incidence_graph.clause_id_set()
        self.__solver: Solver = Solver(cnf=cnf,
                                       clause_id_set=clause_id_set,
                                       sat_solver_enum=sat_solver_enum,
                                       statistics=self.__statistics.solver_statistics)

        self.__assignment_list: List[int] = assignment_list

    # region Public
    def create_circuit(self) -> int:
        """
        :return: the root's id of the created circuit
        """

        return self.__create_circuit(set())
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
            return self.__solver.get_backbone_literals(self.__assignment_list)

        raise ca_exception.FunctionNotImplementedException("get_implied_literals",
                                                           f"this type of getting implied literals ({self.__implied_literals_enum.name}) is not implemented")

    def __get_cut_set(self) -> Set[int]:
        """
        :return: a new cut set
        """

        return self.__hypergraph_partitioning.get_cut_set(self.__incidence_graph, self.__solver, self.__assignment_list)

    def __is_suggested_new_cut_set(self, cut_set_before_restriction: Set[int], cut_set_after_restriction: Set[int],
                                   number_of_variables_before_unit_propagation: int, number_of_variables_after_unit_propagation: int) -> bool:
        """
        :return: True if creating a new cut set is suggested. Otherwise, False is returned.
        """

        # The cut set after the restriction is empty
        if not cut_set_after_restriction:
            return True

        number_of_removed_variables = number_of_variables_before_unit_propagation - number_of_variables_after_unit_propagation
        if (number_of_removed_variables / number_of_variables_before_unit_propagation) >= self.__new_cut_set_threshold:
            return True

        return False

    def __get_suggested_variable_from_cut_set(self, cut_set: Set[int]) -> int:
        """
        Return a suggested variable from the cut set based on the heuristic.
        If the cut set is empty, raise an exception (TryingGetVariableFromEmptyCutSetException).
        :param cut_set: the cut set
        :return: a suggested variable (based on the heuristic) from the cut set
        """

        # The cut set is empty
        if not cut_set:
            raise c_exception.TryingGetVariableFromEmptyCutSetException()

        max = 0
        max_variable = None

        for variable in cut_set:
            temp = self.__incidence_graph.number_of_neighbours_variable(variable)

            if temp > max:
                max = temp
                max_variable = variable

        return max_variable

    def __exist_more_components(self) -> bool:
        """
        Check if more components exist
        :return: True if more components exist, otherwise False is returned
        """

        return True if self.__incidence_graph.number_of_components() > 1 else False

    def __create_circuit(self, cut_set: Set[int]) -> int:
        """
        :return: the root's id of the created circuit
        """

        def remove_implied_literals(implied_literals_set_func: Set[int]) -> None:
            """
            implied_literals_set_func will be destroyed !!!
            """

            for _ in range(len(implied_literals_set_func)):
                self.__assignment_list.pop()
            self.__incidence_graph.restore_backup_literal_set(implied_literals_set_func)

        # The formula is unsatisfiable
        if not self.__solver.is_satisfiable(self.__assignment_list):
            return self.__circuit.create_constant_leaf(False)

        number_of_variables_before_unit_propagation = self.__incidence_graph.number_of_variables()

        # Implied literals
        implied_literal_set = self.__get_implied_literals()
        self.__assignment_list.extend(implied_literal_set)
        isolated_variable_set = self.__incidence_graph.remove_literal_set(implied_literal_set)
        implied_literal_id_set = self.__circuit.create_literal_leaf_set(implied_literal_set)

        number_of_variables_after_unit_propagation = self.__incidence_graph.number_of_variables()

        # The formula is empty after the unit propagation
        if self.__incidence_graph.number_of_nodes() == 0:
            remove_implied_literals(implied_literal_set)    # Restore the implied literals
            return self.__circuit.create_and_node(implied_literal_id_set)

        # TODO Formula type

        # Component caching
        key = self.__component_caching.generate_key_cache(self.__incidence_graph)
        value = self.__component_caching.get(key)
        if value is not None:
            node_id = self.__circuit.create_and_node({value}.union(implied_literal_id_set))
            remove_implied_literals(implied_literal_set)    # Restore the implied literals

            return node_id

        # Check if more components exist
        if self.__exist_more_components():
            incidence_graph_set = self.__incidence_graph.create_incidence_graphs_for_components()

            node_id_set = set()
            for incidence_graph in incidence_graph_set:
                component_temp = Component(cnf=self.__cnf,
                                           assignment_list=self.__assignment_list,
                                           circuit=self.__circuit,
                                           new_cut_set_threshold=self.__new_cut_set_threshold,
                                           incidence_graph=incidence_graph,
                                           component_caching=self.__component_caching,
                                           hypergraph_partitioning=self.__hypergraph_partitioning,
                                           sat_solver_enum=self.__sat_solver_enum,
                                           implied_literals_enum=self.__implied_literals_enum,
                                           statistics=self.__statistics)
                node_id = component_temp.create_circuit()
                node_id_set.add(node_id)

            node_id_cache = self.__circuit.create_and_node(node_id_set)
            node_id = self.__circuit.create_and_node({node_id_cache}.union(implied_literal_id_set))

            # Component caching
            self.__component_caching.add(key, node_id_cache)

            remove_implied_literals(implied_literal_set)    # Restore the implied literals
            return node_id

        # Only one component exists
        cut_set_restriction = cut_set.difference(map(lambda l: abs(l), implied_literal_set))  # restriction
        cut_set_restriction.difference_update(isolated_variable_set)   # because of isolated variables
        # cut_set_restriction = cut_set_restriction.intersection(self.__incidence_graph.variable_set())

        # A new cut set is needed
        if self.__is_suggested_new_cut_set(cut_set, cut_set_restriction, number_of_variables_before_unit_propagation, number_of_variables_after_unit_propagation):
            cut_set_restriction = self.__get_cut_set()

        decision_variable = self.__get_suggested_variable_from_cut_set(cut_set_restriction)
        cut_set_restriction.remove(decision_variable)

        node_id_list = []
        for sign in [+1, -1]:
            literal = sign * decision_variable

            self.__assignment_list.append(literal)
            isolated_variable_set = self.__incidence_graph.remove_literal(literal)

            # Isolated variables
            isolated_variable_in_cut_set_restriction_set = isolated_variable_set.intersection(cut_set_restriction)
            cut_set_restriction.difference_update(isolated_variable_in_cut_set_restriction_set)

            node_id = self.__create_circuit(cut_set_restriction)
            node_id_list.append(node_id)

            self.__assignment_list.pop()
            self.__incidence_graph.restore_backup_literal(literal)
            cut_set_restriction.update(isolated_variable_in_cut_set_restriction_set)  # isolated variables

        decision_node_id = self.__circuit.create_decision_node(decision_variable, node_id_list[0], node_id_list[1])
        node_id = self.__circuit.create_and_node({decision_node_id}.union(implied_literal_id_set))

        # Component caching
        self.__component_caching.add(key, decision_node_id)

        remove_implied_literals(implied_literal_set)    # Restore the implied literals
        return node_id
    # endregion
