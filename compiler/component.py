# Import
from formula.cnf import Cnf
from compiler.solver import Solver
from circuit.circuit import Circuit
from typing import Set, List, Union, Tuple, Dict
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
    Private str node_statistics
    Private Statistics statistics
    Private str mapping_node_statistics
    Private IncidenceGraph incidence_graph
    Private ComponentCachingAbstract component_caching
    Private DecisionHeuristicAbstract decision_heuristic
    Private HypergraphPartitioning hypergraph_partitioning
    Private PreselectionHeuristicAbstract implied_literals_preselection_heuristic
    Private PreselectionHeuristicAbstract first_implied_literals_preselection_heuristic
    
    Private bool disable_sat
    Private bool cara_circuit
    Private bool cut_set_try_cache
    Private int base_class_threshold
    Private List<int> assignment_list
    Private float new_cut_set_threshold
    Private float base_class_ratio_threshold
    Private float new_cut_set_threshold_reduction
    Private Set<BaseClassEnum> base_class_enum_set
    Private int eliminating_redundant_clauses_threshold
    Private bool component_caching_after_unit_propagation
    Private bool component_caching_before_unit_propagation
    
    Private ImpliedLiteralsEnum implied_literals_enum
    Private ImpliedLiteralsEnum first_implied_literals_enum
    Private EliminatingRedundantClausesEnum eliminating_redundant_clauses_enum
    """

    __CREATE_COMPONENTS_THRESHOLD: int = 50

    def __init__(self, cnf: Cnf,
                 solver: Solver,
                 circuit: Circuit,
                 assignment_list: List[int],
                 new_cut_set_threshold: float,
                 new_cut_set_threshold_reduction: float,
                 cut_set_try_cache: bool,
                 incidence_graph: IncidenceGraph,
                 decision_heuristic: DecisionHeuristicAbstract,
                 component_caching: ComponentCachingAbstract,
                 component_caching_before_unit_propagation: bool,
                 component_caching_after_unit_propagation: bool,
                 eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum,
                 eliminating_redundant_clauses_threshold: Union[int, None],
                 hypergraph_partitioning: HypergraphPartitioning,
                 base_class_enum_set: Set[bc_enum.BaseClassEnum],
                 base_class_threshold: Union[int, None],
                 base_class_ratio_threshold: Union[float, None],
                 implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                 implied_literals_preselection_heuristic: PreselectionHeuristicAbstract,
                 first_implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                 first_implied_literals_preselection_heuristic: PreselectionHeuristicAbstract,
                 statistics: Statistics,
                 mapping_node_statistics: Union[str, None],
                 node_statistics: Union[str, None],
                 disable_sat: bool,
                 cara_circuit: bool):
        self.__cnf: Cnf = cnf
        self.__solver: Solver = solver
        self.__circuit: Circuit = circuit
        self.__statistics: Statistics = statistics
        self.__incidence_graph: IncidenceGraph = incidence_graph
        self.__node_statistics: Union[str, None] = node_statistics
        self.__component_caching: ComponentCachingAbstract = component_caching
        self.__decision_heuristic: DecisionHeuristicAbstract = decision_heuristic
        self.__mapping_node_statistics: Union[str, None] = mapping_node_statistics
        self.__hypergraph_partitioning: HypergraphPartitioning = hypergraph_partitioning
        self.__implied_literals_preselection_heuristic: PreselectionHeuristicAbstract = implied_literals_preselection_heuristic
        self.__first_implied_literals_preselection_heuristic: PreselectionHeuristicAbstract = first_implied_literals_preselection_heuristic

        self.__disable_sat: bool = disable_sat
        self.__cara_circuit: bool = cara_circuit
        self.__cut_set_try_cache: bool = cut_set_try_cache
        self.__assignment_list: List[int] = assignment_list
        self.__new_cut_set_threshold: float = new_cut_set_threshold
        self.__base_class_threshold: Union[int, None] = base_class_threshold
        self.__base_class_enum_set: Set[bc_enum.BaseClassEnum] = base_class_enum_set
        self.__new_cut_set_threshold_reduction: float = new_cut_set_threshold_reduction
        self.__base_class_ratio_threshold: Union[float, None] = base_class_ratio_threshold
        self.__component_caching_after_unit_propagation: bool = component_caching_after_unit_propagation
        self.__component_caching_before_unit_propagation: bool = component_caching_before_unit_propagation
        self.__eliminating_redundant_clauses_threshold: Union[int, None] = eliminating_redundant_clauses_threshold

        self.__implied_literals_enum: il_enum.ImpliedLiteralsEnum = implied_literals_enum
        self.__first_implied_literals_enum: il_enum.ImpliedLiteralsEnum = first_implied_literals_enum
        self.__eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum = eliminating_redundant_clauses_enum

    # region Public
    def create_circuit(self, depth: int = 1, cut_set: Union[Set[int], None] = None, previous_implied_literal_set: Union[Set[int], None] = None) -> int:
        """
        :param depth: depth of the node
        :param cut_set: a cut set
        :param previous_implied_literal_set: an implied literal set from the parent component
        :return: the identifier of the root of the created circuit
        """

        cut_set = set() if cut_set is None else cut_set

        return self.__create_circuit(depth=depth,
                                     cut_set=cut_set,
                                     first_implied_literals=False,
                                     previous_implied_literal_set=previous_implied_literal_set)
    # endregion

    # region Private
    def __create_mapping_node_statistics(self, node_id: int, mapping_function_dictionary: Dict[int, int]) -> None:
        """
        Create an actual mapping node statistic
        :param node_id: the identifier of the mapping node
        :param mapping_function_dictionary: the mapping function
        :return: None
        """

        if self.__mapping_node_statistics is None:
            return

        mapping_node_statistics_file = self.__mapping_node_statistics + f".{node_id}.temp.mn.stat"
        with open(mapping_node_statistics_file, "w", encoding="utf-8") as file:
            # Mapping function
            mapping_function_sorted_list = sorted(mapping_function_dictionary.keys())

            for variable_id in mapping_function_sorted_list:
                mapping_id = mapping_function_dictionary[variable_id]
                file.write(f"{variable_id} {mapping_id} ")

            file.write("\n\n")

            # Formula
            file.write(self.__incidence_graph.convert_to_cnf().str_with_mapping(horn_renaming_function=set(),
                                                                                normalize_variables=False)[0])

    def __get_implied_literals(self, depth: int, first_implied_literals: bool) -> Union[Set[int], None]:
        """
        Return a set of implied literals based on the assignment and implied_literals_enum (or first_implied_literals_enum).
        None is returned if the formula is unsatisfiable.
        :param depth: depth of the node
        :param first_implied_literals: True if the method for first implied literals is used
        :return: a set of implied literals
        """

        # The incidence graph is empty
        if self.__incidence_graph.number_of_nodes() == 0:
            return set()

        implied_literals_enum_temp = self.__first_implied_literals_enum if first_implied_literals else self.__implied_literals_enum
        implied_literals_preselection_heuristic_temp = self.__first_implied_literals_preselection_heuristic if first_implied_literals else self.__implied_literals_preselection_heuristic
        get_implied_literals_temp = self.__statistics.component_statistics.get_first_implied_literals if first_implied_literals else self.__statistics.component_statistics.get_implied_literals

        get_implied_literals_temp.start_stopwatch()     # timer (start)

        # NONE
        if implied_literals_enum_temp == il_enum.ImpliedLiteralsEnum.NONE:
            get_implied_literals_temp.stop_stopwatch()  # timer (stop)
            return set()

        # BCP
        if implied_literals_enum_temp == il_enum.ImpliedLiteralsEnum.BCP:
            result = self.__solver.unit_propagation(self.__assignment_list)

            get_implied_literals_temp.stop_stopwatch()  # timer (stop)
            return result

        # IMPLICIT_BCP, IMPLICIT_BCP_ITERATION
        if (implied_literals_enum_temp == il_enum.ImpliedLiteralsEnum.IMPLICIT_BCP) or \
           (implied_literals_enum_temp == il_enum.ImpliedLiteralsEnum.IMPLICIT_BCP_ITERATION):
            only_one_iteration = True if implied_literals_enum_temp == il_enum.ImpliedLiteralsEnum.IMPLICIT_BCP else False

            preselection_set = implied_literals_preselection_heuristic_temp.preselect_variables(variable_restriction_set=None,
                                                                                                incidence_graph=self.__incidence_graph,
                                                                                                depth=depth)

            result = self.__solver.iterative_implicit_unit_propagation(assignment_list=self.__assignment_list,
                                                                       only_one_iteration=only_one_iteration,
                                                                       variable_restriction_set=preselection_set)

            get_implied_literals_temp.stop_stopwatch()  # timer (stop)
            return result

        # BACKBONE
        if implied_literals_enum_temp == il_enum.ImpliedLiteralsEnum.BACKBONE:
            result = self.__solver.get_backbone_literals(self.__assignment_list)

            get_implied_literals_temp.stop_stopwatch()  # timer (stop)
            return result

        raise ca_exception.FunctionNotImplementedException("get_implied_literals",
                                                           f"this type of getting implied literals ({implied_literals_enum_temp.name}) is not implemented")

    def __get_cut_set(self, incidence_graph_is_reduced: bool) -> Set[int]:
        """
        :param incidence_graph_is_reduced: True if the incidence graph has been already reduced
        :return: a new cut set
        """

        self.__statistics.component_statistics.get_cut_set.start_stopwatch()    # timer (start)

        result = self.__hypergraph_partitioning.get_cut_set(incidence_graph=self.__incidence_graph,
                                                            solver=self.__solver,
                                                            assignment=self.__assignment_list,
                                                            incidence_graph_is_reduced=incidence_graph_is_reduced,
                                                            use_restriction=self.__disable_sat)

        self.__statistics.component_statistics.get_cut_set.stop_stopwatch()     # timer (stop)
        return result

    def __is_suggested_new_cut_set(self, cut_set: Set[int], implied_literal_set: Set[int]) -> bool:
        """
        :return: True if creating a new cut set is suggested. Otherwise, False is returned.
        """

        self.__statistics.component_statistics.is_suggested_new_cut_set.start_stopwatch()   # timer (start)

        # The cut set (after the restriction) is empty
        if not cut_set:
            self.__statistics.component_statistics.is_suggested_new_cut_set.stop_stopwatch()    # timer (stop)
            return True

        implied_variable_set = set(map(lambda l: abs(l), implied_literal_set))
        clause_id_set = self.__incidence_graph._clause_id_set
        variable_set = self.__cnf.get_variable_in_clauses(clause_id_set)
        variable_set.difference_update(filter(lambda v: v not in implied_variable_set, map(lambda l: abs(l), self.__assignment_list)))
        intersection_variable_set = variable_set.intersection(implied_variable_set)

        new_cut_set_threshold_temp = self.__new_cut_set_threshold

        # The cache for cut sets can be used
        if (self.__new_cut_set_threshold_reduction < 1) and self.__hypergraph_partitioning.cache_can_be_used(self.__incidence_graph):
            new_cut_set_threshold_temp *= self.__new_cut_set_threshold_reduction

        if (len(intersection_variable_set) / len(variable_set)) >= new_cut_set_threshold_temp:
            self.__statistics.component_statistics.is_suggested_new_cut_set.stop_stopwatch()    # timer (stop)
            return True

        self.__statistics.component_statistics.is_suggested_new_cut_set.stop_stopwatch()    # timer (stop)
        return False

    def __get_decision_variable_from_cut_set(self, cut_set: Set[int], depth: int) -> int:
        """
        Return a decision variable from the cut set based on the decision heuristic (decision_heuristic)
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

        return not self.__incidence_graph.is_connected()

    def __get_eliminating_redundant_clauses_enum(self) -> Union[erc_enum.EliminatingRedundantClausesEnum, None]:
        # No threshold
        if self.__eliminating_redundant_clauses_threshold is None:
            return self.__eliminating_redundant_clauses_enum

        if self.__incidence_graph.number_of_clauses() <= self.__eliminating_redundant_clauses_threshold:
            return self.__eliminating_redundant_clauses_enum

        return None

    def __remove_literals(self, literal_set: Set[int]) -> None:
        """
        Remove the literals in the set from the assignment and restore them in the incidence graph.
        literal_set will be destroyed !!!
        """

        for _ in range(len(literal_set)):
            self.__assignment_list.pop()

        self.__incidence_graph.restore_backup_literal_set(literal_set)

    def __add_literals(self, literal_list: List[int]) -> Tuple[Set[int], Set[int]]:
        """
        Add the literals in the literal_list to the assignment and remove them from the incidence graph
        :return: a tuple. The first element is a set of updated literals in the literal_list ("isolated literals" are removed).
        The second element is a set of isolated variables.
        """

        isolated_variable_set = self.__incidence_graph.remove_literal_list(literal_list, self.__get_eliminating_redundant_clauses_enum())

        literal_set_temp = set(filter(lambda l: abs(l) not in isolated_variable_set, literal_list))
        self.__assignment_list.extend(literal_set_temp)

        return literal_set_temp, isolated_variable_set

    def __create_circuit_more_components_create_incidence_graphs_for_components(self, depth: int, cut_set: Set[int],
                                                                                model: Union[List[int], None], implied_literal_set: Set[int]) -> Set[int]:
        node_id_set = set()
        incidence_graph_set = self.__incidence_graph.create_incidence_graphs_for_components()

        for incidence_graph in incidence_graph_set:
            missing_variable_set = self.__incidence_graph._variable_set.difference(incidence_graph._variable_set)

            # Unsatisfied formula (disabled SAT solver)
            if model is None:
                extended_assignment_list = []
            else:
                extended_assignment_list = [var if var in model else -var for var in missing_variable_set]

            assignment_list = self.__assignment_list.copy()
            assignment_list.extend(extended_assignment_list)

            component_temp = Component(cnf=self.__cnf,
                                       solver=self.__solver,
                                       circuit=self.__circuit,
                                       assignment_list=assignment_list,
                                       new_cut_set_threshold=self.__new_cut_set_threshold,
                                       new_cut_set_threshold_reduction=self.__new_cut_set_threshold_reduction,
                                       cut_set_try_cache=self.__cut_set_try_cache,
                                       incidence_graph=incidence_graph,
                                       decision_heuristic=self.__decision_heuristic,
                                       component_caching=self.__component_caching,
                                       component_caching_before_unit_propagation=self.__component_caching_before_unit_propagation,
                                       component_caching_after_unit_propagation=self.__component_caching_after_unit_propagation,
                                       eliminating_redundant_clauses_enum=self.__eliminating_redundant_clauses_enum,
                                       eliminating_redundant_clauses_threshold=self.__eliminating_redundant_clauses_threshold,
                                       hypergraph_partitioning=self.__hypergraph_partitioning,
                                       base_class_enum_set=self.__base_class_enum_set,
                                       base_class_threshold=self.__base_class_threshold,
                                       base_class_ratio_threshold=self.__base_class_ratio_threshold,
                                       implied_literals_enum=self.__implied_literals_enum,
                                       implied_literals_preselection_heuristic=self.__implied_literals_preselection_heuristic,
                                       first_implied_literals_enum=self.__first_implied_literals_enum,
                                       first_implied_literals_preselection_heuristic=self.__first_implied_literals_preselection_heuristic,
                                       statistics=self.__statistics,
                                       mapping_node_statistics=self.__mapping_node_statistics,
                                       node_statistics=self.__node_statistics,
                                       disable_sat=self.__disable_sat,
                                       cara_circuit=self.__cara_circuit)

            # cut_set_restriction = cut_set.intersection(incidence_graph.variable_set(copy=False))
            node_id = component_temp.create_circuit(depth=(depth + 1),
                                                    cut_set=cut_set,
                                                    previous_implied_literal_set=implied_literal_set)
            node_id_set.add(node_id)

        return node_id_set

    def __create_circuit_more_components(self, depth: int, cut_set: Set[int], model: List[int], implied_literal_set: Set[int]) -> Set[int]:
        node_id_set = set()
        component_list = self.__incidence_graph.get_connected_components()

        for component in component_list:
            missing_variable_set = self.__incidence_graph._variable_set.difference(component)
            extended_assignment_list = [var if var in model else -var for var in missing_variable_set]
            extended_assignment_set, _ = self.__add_literals(extended_assignment_list)

            node_id = self.__create_circuit(depth=(depth + 1),
                                            cut_set=cut_set,
                                            first_implied_literals=False,
                                            previous_implied_literal_set=implied_literal_set)
            node_id_set.add(node_id)

            self.__remove_literals(extended_assignment_set)

        return node_id_set

    def __create_circuit_one_component(self, depth: int, cut_set: Set[int], implied_literal_set: Set[int], new_component: bool) -> int:
        cut_set_restriction = set()     # ballast
        incidence_graph_is_reduced: bool = False
        result_cache_cut_set: Union[Set[int], None] = None

        # Try cache
        if self.__cut_set_try_cache and self.__hypergraph_partitioning.cache_can_be_used(self.__incidence_graph):
            self.__statistics.component_statistics.cut_set_try_cache.start_stopwatch()  # timer (start)

            incidence_graph_is_reduced = True
            self.__hypergraph_partitioning.reduce_incidence_graph(incidence_graph=self.__incidence_graph,
                                                                  solver=self.__solver,
                                                                  assignment=self.__assignment_list,
                                                                  use_restriction=self.__disable_sat)
            result_cache_cut_set, _ = self.__hypergraph_partitioning.check_cache(self.__incidence_graph)

            # A cut set has been found using the cache
            if result_cache_cut_set is not None:
                self.__statistics.component_statistics.cut_set_try_cache_hit.add_count(1)       # counter
                self.__statistics.hypergraph_partitioning_statistics.cache_hit.add_count(1)     # counter

                HypergraphPartitioning.remove_reduction_incidence_graph(self.__incidence_graph)
                cut_set_restriction = result_cache_cut_set
            else:
                self.__statistics.component_statistics.cut_set_try_cache_hit.add_count(0)       # counter

            self.__statistics.component_statistics.cut_set_try_cache.stop_stopwatch()   # timer (stop)

        # Cache did not work
        if result_cache_cut_set is None:
            cut_set_restriction = cut_set.intersection(self.__incidence_graph._variable_set)

            # A new cut set is needed
            if self.__is_suggested_new_cut_set(cut_set=cut_set_restriction,
                                               implied_literal_set=implied_literal_set):
                cut_set_restriction = self.__get_cut_set(incidence_graph_is_reduced)
                self.__statistics.component_statistics.recompute_cut_set.add_count(1)   # counter
            else:
                if incidence_graph_is_reduced:
                    HypergraphPartitioning.remove_reduction_incidence_graph(self.__incidence_graph)     # because of cut set - try cache
                self.__statistics.component_statistics.recompute_cut_set.add_count(0)   # counter

        decision_variable = self.__get_decision_variable_from_cut_set(cut_set=cut_set_restriction,
                                                                      depth=depth)
        self.__statistics.component_statistics.decision_variable.add_count(1)   # counter

        node_id_list = []
        for sign in [+1, -1]:
            literal = sign * decision_variable

            self.__add_literals([literal])
            node_id = self.__create_circuit(depth=(depth + 1),
                                            cut_set=cut_set_restriction,
                                            first_implied_literals=new_component,
                                            previous_implied_literal_set=None)
            node_id_list.append(node_id)

            self.__remove_literals({literal})

        decision_node_id = self.__circuit.create_decision_node(decision_variable, node_id_list[0], node_id_list[1])

        # Node statistics
        if self.__node_statistics is not None:
            node_statistics_file = self.__node_statistics + f".{decision_node_id}.temp.n.stat"
            with open(node_statistics_file, "w", encoding="utf-8") as file:
                file.write(self.__incidence_graph.convert_to_cnf().str_with_mapping(horn_renaming_function=set(),
                                                                                    normalize_variables=False)[0])

        return decision_node_id

    def __create_circuit(self, depth: int, cut_set: Set[int], first_implied_literals: bool, previous_implied_literal_set: Union[Set[int], None]) -> int:
        """
        :param depth: depth of the node
        :param cut_set: a cut set
        :param first_implied_literals: True if the method for first implied literals is used
        :param previous_implied_literal_set: an implied literal set from the parent component (= a flag for a new component)
        :return: the identifier of the root of the created circuit
        """

        model: Union[List[int], None] = None
        new_component = True if previous_implied_literal_set is not None else False

        if not new_component:
            model = self.__solver.get_model(self.__assignment_list)

            # The formula is unsatisfiable
            if model is None:
                if not self.__disable_sat:
                    self.__statistics.component_statistics.unsatisfiable.add_count(1)   # counter
                    return self.__circuit.create_constant_leaf(False)

                # Disabled SAT solver
                else:
                    implied_literal_set = self.__get_implied_literals(depth=depth,
                                                                      first_implied_literals=False)

                    if implied_literal_set is None:
                        self.__statistics.component_statistics.unsatisfiable.add_count(1)  # counter
                        return self.__circuit.create_constant_leaf(False)

        # Component caching (before unit propagation)
        cache_key_before_unit_propagation = None
        cache_variable_id_mapping_id_before_unit_propagation = None
        if self.__component_caching_before_unit_propagation:
            self.__statistics.component_statistics.component_caching_generate_key.start_stopwatch()     # timer (start)
            cache_key_before_unit_propagation, cache_mapping_before_unit_propagation = self.__component_caching.generate_key_cache(self.__incidence_graph)
            self.__statistics.component_statistics.component_caching_generate_key.stop_stopwatch()      # timer (stop)

            # Mapping is used
            if cache_mapping_before_unit_propagation is not None:
                cache_variable_id_mapping_id_before_unit_propagation, _ = cache_mapping_before_unit_propagation

            cache_id, cache_mapping = self.__component_caching.get(cache_key_before_unit_propagation)
            # Hit
            if cache_id is not None:
                self.__statistics.component_statistics.component_caching_formula_length.add_count(self.__incidence_graph.number_of_edges())    # counter
                self.__statistics.component_statistics.component_caching_hit.add_count(1)  # counter

                # Mapping is not used
                if cache_mapping_before_unit_propagation is None:
                    return cache_id

                # Mapping is used
                # cd-DNNF
                if self.__cara_circuit:
                    node_id, mapping_variable_id_variable_cache_dictionary = self.__circuit.create_mapping_node(child_id=cache_id,
                                                                                                                variable_id_mapping_id_dictionary=cache_mapping,
                                                                                                                mapping_id_variable_id_dictionary=cache_mapping_before_unit_propagation[1])

                    # Mapping is used - statistics
                    if node_id != cache_id:
                        self.__statistics.component_statistics.component_caching_cara_mapping_length.add_count(len(cache_mapping))  # counter

                        # Mapping node statistics
                        self.__create_mapping_node_statistics(node_id, mapping_variable_id_variable_cache_dictionary)
                # d-DNNF
                else:
                    is_identity, composed_mapping_variable_id_variable_cache_dictionary, composed_mapping_variable_cache_variable_id_dictionary = Circuit.compose_mappings(variable_id_mapping_id_dictionary_cache=cache_mapping,
                                                                                                                                                                           mapping_id_variable_id_dictionary=cache_mapping_before_unit_propagation[1])
                    # Copying is not needed
                    if is_identity:
                        node_id = cache_id
                        self.__statistics.component_statistics.copying_circuits_identity.add_count(1)   # counter
                    # Copying is needed
                    else:
                        cache_node = self.__circuit.get_node(cache_id)
                        self.__statistics.component_statistics.copying_circuits.start_stopwatch()   # timer (start)

                        node_id, size_temp = cache_node.copy_circuit(mapping_dictionary=composed_mapping_variable_cache_variable_id_dictionary,
                                                                     circuit=self.__circuit)

                        self.__statistics.component_statistics.copying_circuits.stop_stopwatch()    # timer (stop)
                        self.__statistics.component_statistics.copying_circuits_formula_length.add_count(self.__incidence_graph.number_of_edges())  # counter
                        self.__statistics.component_statistics.copying_circuits_identity.add_count(0)       # counter
                        self.__statistics.component_statistics.copying_circuits_size.add_count(size_temp)   # counter

                return node_id
            else:
                self.__statistics.component_statistics.component_caching_hit.add_count(0)  # counter

        # Implied literals
        if not new_component:
            implied_literal_set = self.__get_implied_literals(depth=depth,
                                                              first_implied_literals=first_implied_literals)

            self.__statistics.component_statistics.implied_literal.add_count(len(implied_literal_set))  # counter
            implied_literal_set, _ = self.__add_literals(list(implied_literal_set))
            implied_literal_id_set = self.__circuit.create_literal_leaf_set(implied_literal_set)
        else:
            implied_literal_set = set()
            implied_literal_id_set = set()

        # The formula is empty after the unit propagation
        if not new_component and (self.__incidence_graph.number_of_nodes() == 0):
            node_id = self.__circuit.create_and_node(implied_literal_id_set)

            self.__statistics.component_statistics.empty_incidence_graph.add_count(1)   # counter

            # Component caching
            self.__component_caching.add(cache_key_before_unit_propagation, node_id, cache_variable_id_mapping_id_before_unit_propagation)

            self.__remove_literals(implied_literal_set)    # restore the implied literals
            return node_id

        # Component caching (after unit propagation)
        cache_key_after_unit_propagation = None
        cache_variable_id_mapping_id_after_unit_propagation = None
        if self.__component_caching_after_unit_propagation and (implied_literal_set or (not implied_literal_set and not self.__component_caching_before_unit_propagation)):
            self.__statistics.component_statistics.component_caching_after_generate_key.start_stopwatch()   # timer (start)
            cache_key_after_unit_propagation, cache_mapping_after_unit_propagation = self.__component_caching.generate_key_cache(self.__incidence_graph)
            self.__statistics.component_statistics.component_caching_after_generate_key.stop_stopwatch()    # timer (stop)

            # Mapping is used
            if cache_mapping_after_unit_propagation is not None:
                cache_variable_id_mapping_id_after_unit_propagation, _ = cache_mapping_after_unit_propagation

            cache_id, cache_mapping = self.__component_caching.get(cache_key_after_unit_propagation)
            # Hit
            if cache_id is not None:
                self.__statistics.component_statistics.component_caching_after_formula_length.add_count(self.__incidence_graph.number_of_edges())   # counter
                self.__statistics.component_statistics.component_caching_after_hit.add_count(1)     # counter

                # Mapping is used
                if cache_mapping_after_unit_propagation is not None:
                    # cd-DNNF
                    if self.__cara_circuit:
                        node_temp, mapping_variable_id_variable_cache_dictionary = self.__circuit.create_mapping_node(child_id=cache_id,
                                                                                                                      variable_id_mapping_id_dictionary=cache_mapping,
                                                                                                                      mapping_id_variable_id_dictionary=cache_mapping_after_unit_propagation[1])

                        # Mapping is used - statistics
                        if node_temp != cache_id:
                            self.__statistics.component_statistics.component_caching_after_cara_mapping_length.add_count(len(cache_mapping))    # counter

                            # Mapping node statistics
                            self.__create_mapping_node_statistics(node_temp, mapping_variable_id_variable_cache_dictionary)
                    # d-DNNF
                    else:
                        is_identity, composed_mapping_variable_id_variable_cache_dictionary, composed_mapping_variable_cache_variable_id_dictionary = Circuit.compose_mappings(variable_id_mapping_id_dictionary_cache=cache_mapping,
                                                                                                                                                                               mapping_id_variable_id_dictionary=cache_mapping_after_unit_propagation[1])
                        # Copying is not needed
                        if is_identity:
                            node_temp = cache_id
                            self.__statistics.component_statistics.copying_circuits_after_identity.add_count(1)     # counter
                        # Copying is needed
                        else:
                            cache_node = self.__circuit.get_node(cache_id)
                            self.__statistics.component_statistics.copying_circuits_after.start_stopwatch()  # timer (start)

                            node_temp, size_temp = cache_node.copy_circuit(mapping_dictionary=composed_mapping_variable_cache_variable_id_dictionary,
                                                                           circuit=self.__circuit)

                            self.__statistics.component_statistics.copying_circuits_after.stop_stopwatch()  # timer (stop)
                            self.__statistics.component_statistics.copying_circuits_after_formula_length.add_count(self.__incidence_graph.number_of_edges())    # counter
                            self.__statistics.component_statistics.copying_circuits_after_identity.add_count(0)         # counter
                            self.__statistics.component_statistics.copying_circuits_after_size.add_count(size_temp)     # counter

                    cache_id = node_temp

                node_id = self.__circuit.create_and_node({cache_id}.union(implied_literal_id_set))

                self.__remove_literals(implied_literal_set)    # restore the implied literals
                return node_id
            else:
                self.__statistics.component_statistics.component_caching_after_hit.add_count(0)  # counter

        # 2-CNF and Renamable Horn CNF
        if ((self.__base_class_threshold is None) or (self.__base_class_threshold <= self.__incidence_graph.number_of_edges())) and \
           ((self.__base_class_ratio_threshold is None) or (self.__base_class_ratio_threshold <= self.__incidence_graph.get_ratio())):
            # 2-CNF
            if (bc_enum.BaseClassEnum.TWO_CNF in self.__base_class_enum_set) and (self.__incidence_graph.number_of_variables() > 1) and self.__incidence_graph.is_2_cnf():
                two_cnf = self.__incidence_graph.convert_to_2_cnf()

                self.__statistics.component_statistics.two_cnf_formula_length.add_count(two_cnf.formula_length)     # counter

                node_id_temp = self.__circuit.create_2_cnf_leaf(two_cnf)
                node_id = self.__circuit.create_and_node({node_id_temp}.union(implied_literal_id_set))

                # Component caching
                self.__component_caching.add(cache_key_after_unit_propagation, node_id_temp, cache_variable_id_mapping_id_after_unit_propagation)
                self.__component_caching.add(cache_key_before_unit_propagation, node_id, cache_variable_id_mapping_id_before_unit_propagation)

                self.__remove_literals(implied_literal_set)     # restore the implied literals
                return node_id

            # Renamable Horn CNF
            if (bc_enum.BaseClassEnum.RENAMABLE_HORN_CNF in self.__base_class_enum_set) and (self.__incidence_graph.number_of_variables() > 1):
                renaming_function_temp = self.__incidence_graph.is_renamable_horn_formula()
                if renaming_function_temp is not None:
                    horn_cnf = self.__incidence_graph.convert_to_horn_cnf(renaming_function_temp)

                    self.__statistics.component_statistics.renamable_horn_cnf_formula_length.add_count(horn_cnf.formula_length)     # counter

                    node_id_temp = self.__circuit.create_renamable_horn_cnf_leaf(horn_cnf, renaming_function_temp)
                    node_id = self.__circuit.create_and_node({node_id_temp}.union(implied_literal_id_set))

                    # Component caching
                    self.__component_caching.add(cache_key_after_unit_propagation, node_id_temp, cache_variable_id_mapping_id_after_unit_propagation)
                    self.__component_caching.add(cache_key_before_unit_propagation, node_id, cache_variable_id_mapping_id_before_unit_propagation)

                    self.__remove_literals(implied_literal_set)     # restore the implied literals
                    return node_id

        # More components exist
        if not new_component and self.__exist_more_components():
            self.__statistics.component_statistics.split.add_count(1)   # counter

            # DON'T create new incidence graphs
            if (model is not None) and (self.__incidence_graph.number_of_variables() <= Component.__CREATE_COMPONENTS_THRESHOLD):
                node_id_set = self.__create_circuit_more_components(depth=depth,
                                                                    cut_set=cut_set,
                                                                    model=model,
                                                                    implied_literal_set=implied_literal_set)
            # DO create new incidence graphs
            else:
                node_id_set = self.__create_circuit_more_components_create_incidence_graphs_for_components(depth=depth,
                                                                                                           cut_set=cut_set,
                                                                                                           model=model,
                                                                                                           implied_literal_set=implied_literal_set)
            # Component caching
            if self.__component_caching_after_unit_propagation and (cache_key_after_unit_propagation is not None):
                node_id_temp = self.__circuit.create_and_node(node_id_set)
                node_id = self.__circuit.create_and_node({node_id_temp}.union(implied_literal_id_set))

                self.__component_caching.add(cache_key_after_unit_propagation, node_id_temp, cache_variable_id_mapping_id_after_unit_propagation)
                self.__component_caching.add(cache_key_before_unit_propagation, node_id, cache_variable_id_mapping_id_before_unit_propagation)
            else:
                node_id = self.__circuit.create_and_node(node_id_set.union(implied_literal_id_set))

                self.__component_caching.add(cache_key_before_unit_propagation, node_id, cache_variable_id_mapping_id_before_unit_propagation)

            self.__remove_literals(implied_literal_set)     # restore the implied literals
            return node_id

        # Only one component exists
        decision_node_id = self.__create_circuit_one_component(depth=depth,
                                                               cut_set=cut_set,
                                                               implied_literal_set=previous_implied_literal_set if new_component else implied_literal_set,
                                                               new_component=new_component)
        node_id = self.__circuit.create_and_node({decision_node_id}.union(implied_literal_id_set))

        # Component caching
        self.__component_caching.add(cache_key_after_unit_propagation, decision_node_id, cache_variable_id_mapping_id_after_unit_propagation)
        self.__component_caching.add(cache_key_before_unit_propagation, node_id, cache_variable_id_mapping_id_before_unit_propagation)

        self.__remove_literals(implied_literal_set)     # Restore the implied literals
        return node_id
    # endregion
