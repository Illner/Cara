# Import
from formula.cnf import Cnf
from compiler.solver import Solver
from circuit.circuit import Circuit
from typing import Set, List, Union
from formula.incidence_graph import IncidenceGraph
from compiler_statistics.statistics import Statistics
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract
from compiler.hypergraph_partitioning.hypergraph_partitioning import HypergraphPartitioning
from compiler.decision_heuristic.decision_heuristic_abstract import DecisionHeuristicAbstract
from compiler.preselection_heuristic.preselection_heuristic_abstract import PreselectionHeuristicAbstract

# Import exception
import exception.cara_exception as ca_exception
import exception.compiler.compiler_exception as c_exception

# Import enum
import compiler.enum.base_class_enum as bc_enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import formula.enum.eliminating_redundant_clauses_enum as erc_enum


class Component:
    """
    Component
    """

    """
    Private Cnf cnf
    Private Solver solver
    Private Circuit circuit
    Private bool use_more_solvers
    Private Statistics statistics
    Private bool cut_set_try_cache
    Private float new_cut_set_threshold
    Private float new_cut_set_threshold_reduction
    Private Set<BaseClassEnum> base_class_enum_set
    Private int eliminating_redundant_clauses_threshold
    Private bool component_caching_after_unit_propagation
    
    Private IncidenceGraph incidence_graph
    Private ComponentCachingAbstract component_caching
    Private DecisionHeuristicAbstract decision_heuristic
    Private HypergraphPartitioning hypergraph_partitioning
    Private EliminatingRedundantClausesEnum eliminating_redundant_clauses_enum
    Private PreselectionHeuristicAbstract implied_literals_preselection_heuristic
    
    Private SatSolverEnum sat_solver_enum
    Private ImpliedLiteralsEnum implied_literals_enum
    Private FirstImpliedLiteralsEnum first_implied_literals_enum
    
    Private List<int> assignment_list
    """

    def __init__(self, cnf: Cnf,
                 use_more_solvers: bool,
                 solver: Union[Solver, None],
                 assignment_list: List[int],
                 circuit: Circuit,
                 new_cut_set_threshold: float,
                 new_cut_set_threshold_reduction: float,
                 cut_set_try_cache: bool,
                 incidence_graph: IncidenceGraph,
                 decision_heuristic: DecisionHeuristicAbstract,
                 component_caching: ComponentCachingAbstract,
                 component_caching_after_unit_propagation: bool,
                 eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum,
                 eliminating_redundant_clauses_threshold: Union[int, None],
                 hypergraph_partitioning: HypergraphPartitioning,
                 sat_solver_enum: ss_enum.SatSolverEnum,
                 base_class_enum_set: Set[bc_enum.BaseClassEnum],
                 implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                 implied_literals_preselection_heuristic: PreselectionHeuristicAbstract,
                 first_implied_literals_enum: il_enum.FirstImpliedLiteralsEnum,
                 statistics: Statistics,
                 preprocessing: bool = False):
        self.__cnf: Cnf = cnf
        self.__circuit: Circuit = circuit
        self.__use_more_solvers: bool = use_more_solvers
        self.__cut_set_try_cache: bool = cut_set_try_cache
        self.__incidence_graph: IncidenceGraph = incidence_graph
        self.__new_cut_set_threshold: float = new_cut_set_threshold
        self.__new_cut_set_threshold_reduction: float = new_cut_set_threshold_reduction
        self.__base_class_enum_set: Set[bc_enum.BaseClassEnum] = base_class_enum_set
        self.__component_caching_after_unit_propagation: bool = component_caching_after_unit_propagation
        self.__eliminating_redundant_clauses_threshold: Union[int, None] = eliminating_redundant_clauses_threshold

        self.__component_caching: ComponentCachingAbstract = component_caching
        self.__decision_heuristic: DecisionHeuristicAbstract = decision_heuristic
        self.__hypergraph_partitioning: HypergraphPartitioning = hypergraph_partitioning
        self.__implied_literals_preselection_heuristic: PreselectionHeuristicAbstract = implied_literals_preselection_heuristic

        self.__sat_solver_enum: ss_enum.SatSolverEnum = sat_solver_enum
        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum
        self.__first_implied_literals_enum: il_enum.FirstImpliedLiteralsEnum = first_implied_literals_enum
        self.__eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum = eliminating_redundant_clauses_enum

        self.__statistics: Statistics = statistics

        # Solver
        if (not use_more_solvers) and (solver is not None):
            self.__solver: Solver = solver
        else:
            clause_id_set = self.__incidence_graph.clause_id_set(copy=False)
            self.__solver: Solver = Solver(cnf=cnf,
                                           clause_id_set=clause_id_set,
                                           sat_solver_enum=sat_solver_enum,
                                           first_implied_literals_enum=self.__first_implied_literals_enum if not preprocessing else il_enum.FirstImpliedLiteralsEnum.BACKBONE,
                                           statistics=self.__statistics.solver_statistics)

        self.__assignment_list: List[int] = assignment_list

    # region Public
    def create_circuit(self, depth: int, cut_set: Union[Set[int], None] = None, previous_implied_literal_set: Union[Set[int], None] = None) -> int:
        """
        :param depth: depth of the node
        :param cut_set: a cut set (None = set())
        :param previous_implied_literal_set: an implied literal set from the parent component (None = set())
        :return: the identifier of the root of the created circuit
        """

        cut_set = set() if cut_set is None else cut_set
        new_component: bool = False if depth == 1 else True
        previous_implied_literal_set = set() if previous_implied_literal_set is None else previous_implied_literal_set

        return self.__create_circuit(cut_set=cut_set,
                                     depth=depth,
                                     new_component=new_component,
                                     implied_literal_set=previous_implied_literal_set)
    # endregion

    # region Private
    def __get_implied_literals(self, depth: int) -> Union[Set[int], None]:
        """
        Return a set of implied literals based on the assignment and implied_literals_enum.
        None is returned if the formula is unsatisfiable.
        :param depth: depth of the node
        :return: a set of implied literals
        """

        # The incidence graph is empty
        if self.__incidence_graph.number_of_nodes() == 0:
            return set()

        # NONE
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.NONE:
            return set()

        self.__statistics.component_statistics.get_implied_literals.start_stopwatch()  # timer (start - implied literals)

        # BCP
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.BCP:
            result = self.__solver.unit_propagation(self.__assignment_list)

            self.__statistics.component_statistics.get_implied_literals.stop_stopwatch()    # timer (stop - implied literals)
            return result

        # IMPLICIT_BCP, IMPLICIT_BCP_ITERATION
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.IMPLICIT_BCP or \
           self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.IMPLICIT_BCP_ITERATION:
            only_one_iteration = True if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.IMPLICIT_BCP else False

            preselection_set = self.__implied_literals_preselection_heuristic.preselect_variables(variable_restriction_set=None,
                                                                                                  incidence_graph=self.__incidence_graph,
                                                                                                  depth=depth)

            result = self.__solver.iterative_implicit_unit_propagation(assignment_list=self.__assignment_list,
                                                                       only_one_iteration=only_one_iteration,
                                                                       variable_restriction_set=preselection_set)

            self.__statistics.component_statistics.get_implied_literals.stop_stopwatch()  # timer (stop - implied literals)
            return result

        # BACKBONE
        if self.__implied_literals_enum == il_enum.ImpliedLiteralsEnum.BACKBONE:
            result = self.__solver.get_backbone_literals(self.__assignment_list)

            self.__statistics.component_statistics.get_implied_literals.stop_stopwatch()  # timer (stop - implied literals)
            return result

        self.__statistics.component_statistics.get_implied_literals.stop_stopwatch()  # timer (stop - implied literals)
        raise ca_exception.FunctionNotImplementedException("get_implied_literals",
                                                           f"this type of getting implied literals ({self.__implied_literals_enum.name}) is not implemented")

    def __get_cut_set(self, incidence_graph_is_reduced: bool) -> Set[int]:
        """
        :param incidence_graph_is_reduced: True if the incidence graph is already reduced
        :return: a new cut set
        """

        self.__statistics.component_statistics.get_cut_set.start_stopwatch()    # timer (start)

        result = self.__hypergraph_partitioning.get_cut_set(self.__incidence_graph, self.__solver, self.__assignment_list, incidence_graph_is_reduced)

        self.__statistics.component_statistics.get_cut_set.stop_stopwatch()     # timer (stop)
        return result

    def __is_suggested_new_cut_set(self, cut_set_before_restriction: Set[int], cut_set_after_restriction: Set[int], implied_literal_set: Set[int],
                                   number_of_variables_before_unit_propagation: int, number_of_variables_after_unit_propagation: int) -> bool:
        """
        :return: True if creating a new cut set is suggested. Otherwise, False is returned.
        """

        # The cut set after the restriction is empty
        if not cut_set_after_restriction:
            return True

        implied_variable_set = set(map(lambda l: abs(l), implied_literal_set))
        clause_id_set = self.__incidence_graph.clause_id_set(copy=False)
        variable_set = self.__cnf.get_variable_in_clauses(clause_id_set)
        variable_set.difference_update(filter(lambda v: v not in implied_variable_set, map(lambda l: abs(l), self.__assignment_list)))
        intersection_variable_set = variable_set.intersection(implied_variable_set)

        new_cut_set_threshold_temp = self.__new_cut_set_threshold

        # The cache for cut sets can be used
        if (self.__new_cut_set_threshold_reduction < 1) and self.__hypergraph_partitioning.cache_can_be_used(self.__incidence_graph):
            new_cut_set_threshold_temp *= self.__new_cut_set_threshold_reduction

        if (len(intersection_variable_set) / len(variable_set)) >= new_cut_set_threshold_temp:
            return True

        return False

    def __get_decision_variable_from_cut_set(self, cut_set: Set[int], depth: int) -> int:
        """
        Return a decision variable from the cut set based on the decision heuristic
        :param cut_set: a cut set
        :param depth: depth of the node
        :return: a decision variable (based on the heuristic) from the cut set
        :raises TryingGetVariableFromEmptyCutSetException: if the cut set is empty
        """

        self.__statistics.component_statistics.get_decision_variable_from_cut_set.start_stopwatch()    # timer (start)

        # The cut set is empty
        if not cut_set:
            raise c_exception.TryingGetVariableFromEmptyCutSetException()

        decision_variable = self.__decision_heuristic.get_decision_variable(cut_set=cut_set,
                                                                            incidence_graph=self.__incidence_graph,
                                                                            solver=self.__solver,
                                                                            assignment_list=self.__assignment_list,
                                                                            depth=depth)

        self.__statistics.component_statistics.get_decision_variable_from_cut_set.stop_stopwatch()     # timer (stop)
        return decision_variable

    def __exist_more_components(self) -> bool:
        """
        Check if more components exist
        :return: True if more components exist. Otherwise, False is returned.
        """

        # return True if self.__incidence_graph.number_of_components() > 1 else False
        return not self.__incidence_graph.is_connected()

    def __get_eliminating_redundant_clauses_enum(self) -> Union[erc_enum.EliminatingRedundantClausesEnum, None]:
        # No threshold
        if self.__eliminating_redundant_clauses_threshold is None:
            return self.__eliminating_redundant_clauses_enum

        if self.__incidence_graph.number_of_clauses() <= self.__eliminating_redundant_clauses_threshold:
            return self.__eliminating_redundant_clauses_enum

        return None

    def __create_circuit(self, cut_set: Set[int], depth: int, new_component: bool, implied_literal_set: Set[int]) -> int:
        """
        :param cut_set: a cut set
        :param depth: depth of the node
        :param new_component: True if the subformula represents a new component (not satisfiability test needed etc.)
        :param implied_literal_set: an implied literal set (hack for new components)
        :return: the identifier of the root of the created circuit
        """

        def remove_implied_literals(implied_literals_set_func: Set[int]) -> None:
            """
            implied_literals_set_func will be destroyed !!!
            """

            # New component => no implied literals have been derived
            if new_component:
                return

            for _ in range(len(implied_literals_set_func)):
                self.__assignment_list.pop()
            self.__incidence_graph.restore_backup_literal_set(implied_literals_set_func)

        model = None

        if not new_component:
            model = self.__solver.get_model(self.__assignment_list)
            # The formula is unsatisfiable
            if model is None:
                self.__statistics.component_statistics.unsatisfiable.add_count(1)   # counter
                return self.__circuit.create_constant_leaf(False)

        # Component caching (before unit propagation)
        self.__statistics.component_statistics.component_caching_generate_key.start_stopwatch()     # timer (start)
        key_before_unit_propagation = self.__component_caching.generate_key_cache(self.__incidence_graph)
        self.__statistics.component_statistics.component_caching_generate_key.stop_stopwatch()      # timer (stop)

        value = self.__component_caching.get(key_before_unit_propagation)
        # Hit
        if value is not None:
            self.__statistics.component_statistics.component_caching_formula_length.add_count(self.__incidence_graph.number_of_edges())    # counter
            self.__statistics.component_statistics.component_caching_hit.add_count(1)  # counter

            return value
        else:
            self.__statistics.component_statistics.component_caching_hit.add_count(0)  # counter

        number_of_variables_before_unit_propagation = self.__incidence_graph.number_of_variables()

        # Implied literals
        if not new_component:
            implied_literal_set = self.__get_implied_literals(depth)
            implied_literal_list = list(implied_literal_set)
            self.__statistics.component_statistics.implied_literal.add_count(len(implied_literal_set))  # counter

            self.__assignment_list.extend(implied_literal_list)
            isolated_variable_set = self.__incidence_graph.remove_literal_list(implied_literal_list, self.__get_eliminating_redundant_clauses_enum())
            self.__statistics.component_statistics.isolated_variable.add_count(len(isolated_variable_set))  # counter

            implied_literal_id_set = self.__circuit.create_literal_leaf_set(implied_literal_set)
        else:
            implied_literal_id_set = set()

        number_of_variables_after_unit_propagation = self.__incidence_graph.number_of_variables()

        # The formula is empty after the unit propagation
        if not new_component and self.__incidence_graph.number_of_nodes() == 0:
            node_id = self.__circuit.create_and_node(implied_literal_id_set)

            self.__statistics.component_statistics.empty_incidence_graph.add_count(1)   # counter

            # Component caching
            self.__component_caching.add(key_before_unit_propagation, node_id)

            remove_implied_literals(implied_literal_set)    # restore the implied literals
            return node_id

        # Component caching (after unit propagation)
        key_after_unit_propagation = None
        if self.__component_caching_after_unit_propagation and not new_component:
            self.__statistics.component_statistics.component_caching_after_generate_key.start_stopwatch()   # timer (start)
            key_after_unit_propagation = self.__component_caching.generate_key_cache(self.__incidence_graph)
            self.__statistics.component_statistics.component_caching_after_generate_key.stop_stopwatch()    # timer (stop)

            value = self.__component_caching.get(key_after_unit_propagation)
            # Hit
            if value is not None:
                self.__statistics.component_statistics.component_caching_after_formula_length.add_count(self.__incidence_graph.number_of_edges())   # counter
                self.__statistics.component_statistics.component_caching_after_hit.add_count(1)     # counter

                node_id = self.__circuit.create_and_node({value}.union(implied_literal_id_set))

                remove_implied_literals(implied_literal_set)    # restore the implied literals
                return node_id
            else:
                self.__statistics.component_statistics.component_caching_after_hit.add_count(0)  # counter

        # 2-CNF
        if (bc_enum.BaseClassEnum.TWO_CNF in self.__base_class_enum_set) and self.__incidence_graph.is_2_cnf():
            two_cnf = self.__incidence_graph.convert_to_2_cnf()

            self.__statistics.component_statistics.two_cnf_formula_length.add_count(two_cnf.formula_length)     # counter

            node_id_temp = self.__circuit.create_2_cnf_leaf(two_cnf)
            node_id = self.__circuit.create_and_node({node_id_temp}.union(implied_literal_id_set))

            # Component caching
            self.__component_caching.add(key_after_unit_propagation, node_id_temp)
            self.__component_caching.add(key_before_unit_propagation, node_id)

            remove_implied_literals(implied_literal_set)  # restore the implied literals
            return node_id

        # Renamable Horn CNF
        if bc_enum.BaseClassEnum.RENAMABLE_HORN_CNF in self.__base_class_enum_set:
            renaming_function_temp = self.__incidence_graph.is_renamable_horn_formula()
            if renaming_function_temp is not None:
                horn_cnf = self.__incidence_graph.convert_to_horn_cnf(renaming_function_temp)

                self.__statistics.component_statistics.renamable_horn_cnf_formula_length.add_count(horn_cnf.formula_length)     # counter

                node_id_temp = self.__circuit.create_renamable_horn_cnf_leaf(horn_cnf, renaming_function_temp)
                node_id = self.__circuit.create_and_node({node_id_temp}.union(implied_literal_id_set))

                # Component caching
                self.__component_caching.add(key_after_unit_propagation, node_id_temp)
                self.__component_caching.add(key_before_unit_propagation, node_id)

                remove_implied_literals(implied_literal_set)  # restore the implied literals
                return node_id

        # Check if more components exist
        if not new_component and self.__exist_more_components():
            self.__statistics.component_statistics.split.add_count(1)    # counter
            incidence_graph_set = self.__incidence_graph.create_incidence_graphs_for_components()

            node_id_set = set()
            for incidence_graph in incidence_graph_set:
                # Assignment
                if self.__use_more_solvers:
                    assignment_list = self.__assignment_list
                else:
                    missing_variable_set = self.__incidence_graph.variable_set(copy=False).difference(incidence_graph.variable_set(copy=False))
                    extended_assignment_list = [var if var in model else -var for var in missing_variable_set]
                    assignment_list = self.__assignment_list.copy()
                    assignment_list.extend(extended_assignment_list)

                component_temp = Component(cnf=self.__cnf,
                                           use_more_solvers=self.__use_more_solvers,
                                           solver=None if self.__use_more_solvers else self.__solver,
                                           assignment_list=assignment_list,
                                           circuit=self.__circuit,
                                           new_cut_set_threshold=self.__new_cut_set_threshold,
                                           new_cut_set_threshold_reduction=self.__new_cut_set_threshold_reduction,
                                           cut_set_try_cache=self.__cut_set_try_cache,
                                           incidence_graph=incidence_graph,
                                           decision_heuristic=self.__decision_heuristic,
                                           component_caching=self.__component_caching,
                                           component_caching_after_unit_propagation=self.__component_caching_after_unit_propagation,
                                           eliminating_redundant_clauses_enum=self.__eliminating_redundant_clauses_enum,
                                           eliminating_redundant_clauses_threshold=self.__eliminating_redundant_clauses_threshold,
                                           hypergraph_partitioning=self.__hypergraph_partitioning,
                                           sat_solver_enum=self.__sat_solver_enum,
                                           base_class_enum_set=self.__base_class_enum_set,
                                           implied_literals_enum=self.__implied_literals_enum,
                                           implied_literals_preselection_heuristic=self.__implied_literals_preselection_heuristic,
                                           first_implied_literals_enum=self.__first_implied_literals_enum,
                                           statistics=self.__statistics)
                cut_set_restriction = cut_set.intersection(incidence_graph.variable_set(copy=False))
                node_id = component_temp.create_circuit(depth=(depth + 1),
                                                        cut_set=cut_set_restriction,
                                                        previous_implied_literal_set=implied_literal_set)
                node_id_set.add(node_id)

            node_id_temp = self.__circuit.create_and_node(node_id_set)
            node_id = self.__circuit.create_and_node({node_id_temp}.union(implied_literal_id_set))

            # Component caching
            self.__component_caching.add(key_after_unit_propagation, node_id_temp)
            self.__component_caching.add(key_before_unit_propagation, node_id)

            remove_implied_literals(implied_literal_set)    # restore the implied literals
            return node_id

        # Only one component exists
        cut_set_restriction = cut_set.intersection(self.__incidence_graph.variable_set(copy=False))
        # cut_set_restriction = cut_set.difference(map(lambda l: abs(l), implied_literal_set))  # restriction
        # cut_set_restriction.difference_update(isolated_variable_set)   # because of isolated variables

        # Try cache
        incidence_graph_is_reduced: bool = False
        result_cache_cut_set: Union[Set[int], None] = None
        if self.__cut_set_try_cache and self.__hypergraph_partitioning.cache_can_be_used(self.__incidence_graph):
            self.__statistics.component_statistics.cut_set_try_cache.start_stopwatch()  # timer (start)

            incidence_graph_is_reduced = True
            self.__hypergraph_partitioning.reduce_incidence_graph(self.__incidence_graph, self.__solver, self.__assignment_list)
            result_cache_cut_set, _ = self.__hypergraph_partitioning.check_cache(self.__incidence_graph)

            # A cut set has been found using the cache
            if result_cache_cut_set is not None:
                self.__statistics.component_statistics.cut_set_try_cache_hit.add_count(1)    # counter
                self.__statistics.hypergraph_partitioning_statistics.cache_hit.add_count(1)  # counter

                self.__hypergraph_partitioning.remove_reduction_incidence_graph(self.__incidence_graph)
                cut_set_restriction = result_cache_cut_set
            else:
                self.__statistics.component_statistics.cut_set_try_cache_hit.add_count(0)    # counter

            self.__statistics.component_statistics.cut_set_try_cache.stop_stopwatch()   # timer (stop)

        # Cache did not work
        if result_cache_cut_set is None:
            # A new cut set is needed
            if self.__is_suggested_new_cut_set(cut_set_before_restriction=cut_set,
                                               cut_set_after_restriction=cut_set_restriction,
                                               implied_literal_set=implied_literal_set,
                                               number_of_variables_before_unit_propagation=number_of_variables_before_unit_propagation,
                                               number_of_variables_after_unit_propagation=number_of_variables_after_unit_propagation):
                cut_set_restriction = self.__get_cut_set(incidence_graph_is_reduced)
                self.__statistics.component_statistics.recompute_cut_set.add_count(1)   # counter
            else:
                if incidence_graph_is_reduced:
                    self.__hypergraph_partitioning.remove_reduction_incidence_graph(self.__incidence_graph)     # because of cut set - try cache
                self.__statistics.component_statistics.recompute_cut_set.add_count(0)   # counter

        decision_variable = self.__get_decision_variable_from_cut_set(cut_set=cut_set_restriction,
                                                                      depth=depth)
        cut_set_restriction.remove(decision_variable)
        self.__statistics.component_statistics.decision_variable.add_count(1)   # counter

        node_id_list = []
        for sign in [+1, -1]:
            literal = sign * decision_variable

            self.__assignment_list.append(literal)
            isolated_variable_set = self.__incidence_graph.remove_literal(literal, self.__get_eliminating_redundant_clauses_enum())
            self.__statistics.component_statistics.isolated_variable.add_count(len(isolated_variable_set))  # counter

            # Isolated variables
            isolated_variable_in_cut_set_restriction_set = isolated_variable_set.intersection(cut_set_restriction)
            cut_set_restriction.difference_update(isolated_variable_in_cut_set_restriction_set)

            node_id = self.__create_circuit(cut_set=cut_set_restriction,
                                            depth=(depth + 1),
                                            new_component=False,
                                            implied_literal_set=set())  # not necessary
            node_id_list.append(node_id)

            self.__assignment_list.pop()
            self.__incidence_graph.restore_backup_literal(literal)
            cut_set_restriction.update(isolated_variable_in_cut_set_restriction_set)  # isolated variables

        decision_node_id = self.__circuit.create_decision_node(decision_variable, node_id_list[0], node_id_list[1])
        node_id = self.__circuit.create_and_node({decision_node_id}.union(implied_literal_id_set))

        # Component caching
        self.__component_caching.add(key_after_unit_propagation, decision_node_id)
        self.__component_caching.add(key_before_unit_propagation, node_id)

        remove_implied_literals(implied_literal_set)    # Restore the implied literals
        return node_id
    # endregion
