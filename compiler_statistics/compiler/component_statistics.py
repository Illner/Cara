# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract


class ComponentStatistics(StatisticsTemplateAbstract):
    """
    Component - statistics
    """

    """
    Private StatisticsComponentTimer get_implied_literals
    Private StatisticsComponentTimer get_first_implied_literals
    Private StatisticsComponentTimer get_cut_set
    Private StatisticsComponentTimer get_decision_variable_from_cut_set
    Private StatisticsComponentTimer cut_set_try_cache
    Private StatisticsComponentTimer component_caching_generate_key
    Private StatisticsComponentTimer component_caching_after_generate_key
    Private StatisticsComponentTimer is_suggested_new_cut_set
    Private StatisticsComponentTimer copying_circuits
    Private StatisticsComponentTimer copying_circuits_after
    
    Private StatisticsComponentCounter unsatisfiable
    Private StatisticsComponentCounter implied_literal
    Private StatisticsComponentCounter empty_incidence_graph
    Private StatisticsComponentCounter component_caching_hit
    Private StatisticsComponentCounter component_caching_formula_length
    Private StatisticsComponentCounter component_caching_after_hit
    Private StatisticsComponentCounter component_caching_after_formula_length
    Private StatisticsComponentCounter component_caching_cara_mapping_length
    Private StatisticsComponentCounter component_caching_after_cara_mapping_length
    Private StatisticsComponentCounter split
    Private StatisticsComponentCounter decision_variable
    Private StatisticsComponentCounter recompute_cut_set
    Private StatisticsComponentCounter cut_set_try_cache_hit
    Private StatisticsComponentCounter two_cnf_formula_length
    Private StatisticsComponentCounter renamable_horn_cnf_formula_length
    Private StatisticsComponentCounter copying_circuits_size
    Private StatisticsComponentCounter copying_circuits_identity
    Private StatisticsComponentCounter copying_circuits_formula_length
    Private StatisticsComponentCounter copying_circuits_after_size
    Private StatisticsComponentCounter copying_circuits_after_identity
    Private StatisticsComponentCounter copying_circuits_after_formula_length
    """

    def __init__(self, active: bool):
        super().__init__("Component")

        self.__get_implied_literals: StatisticsComponentTimer = StatisticsComponentTimer(name="get implied literals", active=active)
        self._component_list.append(self.__get_implied_literals)

        self.__get_first_implied_literals: StatisticsComponentTimer = StatisticsComponentTimer(name="get first implied literals", active=active)
        self._component_list.append(self.__get_first_implied_literals)

        self.__get_cut_set: StatisticsComponentTimer = StatisticsComponentTimer(name="get cut set", active=active)
        self._component_list.append(self.__get_cut_set)

        self.__get_decision_variable_from_cut_set: StatisticsComponentTimer = StatisticsComponentTimer(name="get decision variable", active=active)
        self._component_list.append(self.__get_decision_variable_from_cut_set)

        self.__unsatisfiable: StatisticsComponentCounter = StatisticsComponentCounter(name="unsatisfiable subformulae",
                                                                                      active=active,
                                                                                      show_only_number_of_calls=True)
        self._component_list.append(self.__unsatisfiable)

        self.__implied_literal: StatisticsComponentCounter = StatisticsComponentCounter(name="implied literal", active=active)
        self._component_list.append(self.__implied_literal)

        self.__empty_incidence_graph: StatisticsComponentCounter = StatisticsComponentCounter(name="empty incidence graph",
                                                                                              active=active,
                                                                                              show_only_number_of_calls=True)
        self._component_list.append(self.__empty_incidence_graph)

        self.__component_caching_generate_key: StatisticsComponentTimer = StatisticsComponentTimer(name="component caching (before BCP) - generate key", active=active)
        self._component_list.append(self.__component_caching_generate_key)

        self.__component_caching_hit: StatisticsComponentCounter = StatisticsComponentCounter(name="component caching (before BCP) - hit", active=active)
        self._component_list.append(self.__component_caching_hit)

        self.__component_caching_formula_length: StatisticsComponentCounter = StatisticsComponentCounter(name="component caching (before BCP) - formula length", active=active)
        self._component_list.append(self.__component_caching_formula_length)

        self.__component_caching_after_generate_key: StatisticsComponentTimer = StatisticsComponentTimer(name="component caching (after BCP) - generate key", active=active)
        self._component_list.append(self.__component_caching_after_generate_key)

        self.__component_caching_after_hit: StatisticsComponentCounter = StatisticsComponentCounter(name="component caching (after BCP) - hit", active=active)
        self._component_list.append(self.__component_caching_after_hit)

        self.__component_caching_after_formula_length: StatisticsComponentCounter = StatisticsComponentCounter(name="component caching (after BCP) - formula length", active=active)
        self._component_list.append(self.__component_caching_after_formula_length)

        self.__component_caching_cara_mapping_length: StatisticsComponentCounter = StatisticsComponentCounter(name="component caching (before BCP) - cara caching scheme - mapping length", active=active)
        self._component_list.append(self.__component_caching_cara_mapping_length)

        self.__component_caching_after_cara_mapping_length: StatisticsComponentCounter = StatisticsComponentCounter(name="component caching (after BCP) - cara caching scheme - mapping length", active=active)
        self._component_list.append(self.__component_caching_after_cara_mapping_length)

        self.__split: StatisticsComponentCounter = StatisticsComponentCounter(name="split",
                                                                              active=active,
                                                                              show_only_number_of_calls=True)
        self._component_list.append(self.__split)

        self.__decision_variable: StatisticsComponentCounter = StatisticsComponentCounter(name="decision variable",
                                                                                          active=active,
                                                                                          show_only_number_of_calls=True)
        self._component_list.append(self.__decision_variable)

        self.__recompute_cut_set: StatisticsComponentCounter = StatisticsComponentCounter(name="recompute cut set", active=active)
        self._component_list.append(self.__recompute_cut_set)

        self.__is_suggested_new_cut_set: StatisticsComponentTimer = StatisticsComponentTimer(name="is suggested new cut set", active=active)
        self._component_list.append(self.__is_suggested_new_cut_set)

        self.__cut_set_try_cache: StatisticsComponentTimer = StatisticsComponentTimer(name="cut set try cache", active=active)
        self._component_list.append(self.__cut_set_try_cache)

        self.__cut_set_try_cache_hit: StatisticsComponentCounter = StatisticsComponentCounter(name="cut set try cache - hit", active=active)
        self._component_list.append(self.__cut_set_try_cache_hit)

        self.__two_cnf_formula_length: StatisticsComponentCounter = StatisticsComponentCounter(name="2-CNF - formula length", active=active)
        self._component_list.append(self.__two_cnf_formula_length)

        self.__renamable_horn_cnf_formula_length: StatisticsComponentCounter = StatisticsComponentCounter(name="renamable Horn formula - formula length", active=active)
        self._component_list.append(self.__renamable_horn_cnf_formula_length)

        self.__copying_circuits: StatisticsComponentTimer = StatisticsComponentTimer(name="copying circuits (before BCP)", active=active)
        self._component_list.append(self.__copying_circuits)

        self.__copying_circuits_after: StatisticsComponentTimer = StatisticsComponentTimer(name="copying circuits (after BCP)", active=active)
        self._component_list.append(self.__copying_circuits_after)

        self.__copying_circuits_size: StatisticsComponentCounter = StatisticsComponentCounter(name="copying circuits (before BCP) - circuit size", active=active)
        self._component_list.append(self.__copying_circuits_size)

        self.__copying_circuits_identity: StatisticsComponentCounter = StatisticsComponentCounter(name="copying circuits (before BCP) - identity", active=active)
        self._component_list.append(self.__copying_circuits_identity)

        self.__copying_circuits_formula_length: StatisticsComponentCounter = StatisticsComponentCounter(name="copying circuits (before BCP) - formula length", active=active)
        self._component_list.append(self.__copying_circuits_formula_length)

        self.__copying_circuits_after_size: StatisticsComponentCounter = StatisticsComponentCounter(name="copying circuits (after BCP) - circuit size", active=active)
        self._component_list.append(self.__copying_circuits_after_size)

        self.__copying_circuits_after_identity: StatisticsComponentCounter = StatisticsComponentCounter(name="copying circuits (after BCP) - identity", active=active)
        self._component_list.append(self.__copying_circuits_after_identity)

        self.__copying_circuits_after_formula_length: StatisticsComponentCounter = StatisticsComponentCounter(name="copying circuits (after BCP) - formula length", active=active)
        self._component_list.append(self.__copying_circuits_after_formula_length)

    # region Property
    @property
    def get_implied_literals(self) -> StatisticsComponentTimer:
        return self.__get_implied_literals

    @property
    def get_first_implied_literals(self) -> StatisticsComponentTimer:
        return self.__get_first_implied_literals

    @property
    def get_cut_set(self) -> StatisticsComponentTimer:
        return self.__get_cut_set

    @property
    def get_decision_variable_from_cut_set(self) -> StatisticsComponentTimer:
        return self.__get_decision_variable_from_cut_set

    @property
    def unsatisfiable(self) -> StatisticsComponentCounter:
        return self.__unsatisfiable

    @property
    def implied_literal(self) -> StatisticsComponentCounter:
        return self.__implied_literal

    @property
    def empty_incidence_graph(self) -> StatisticsComponentCounter:
        return self.__empty_incidence_graph

    @property
    def component_caching_generate_key(self) -> StatisticsComponentTimer:
        return self.__component_caching_generate_key

    @property
    def component_caching_hit(self) -> StatisticsComponentCounter:
        return self.__component_caching_hit

    @property
    def component_caching_formula_length(self) -> StatisticsComponentCounter:
        return self.__component_caching_formula_length

    @property
    def component_caching_after_generate_key(self) -> StatisticsComponentTimer:
        return self.__component_caching_after_generate_key

    @property
    def component_caching_after_hit(self) -> StatisticsComponentCounter:
        return self.__component_caching_after_hit

    @property
    def component_caching_after_formula_length(self) -> StatisticsComponentCounter:
        return self.__component_caching_after_formula_length

    @property
    def component_caching_cara_mapping_length(self) -> StatisticsComponentCounter:
        return self.__component_caching_cara_mapping_length

    @property
    def component_caching_after_cara_mapping_length(self) -> StatisticsComponentCounter:
        return self.__component_caching_after_cara_mapping_length

    @property
    def split(self) -> StatisticsComponentCounter:
        return self.__split

    @property
    def decision_variable(self) -> StatisticsComponentCounter:
        return self.__decision_variable

    @property
    def recompute_cut_set(self) -> StatisticsComponentCounter:
        return self.__recompute_cut_set

    @property
    def is_suggested_new_cut_set(self) -> StatisticsComponentTimer:
        return self.__is_suggested_new_cut_set

    @property
    def cut_set_try_cache(self) -> StatisticsComponentTimer:
        return self.__cut_set_try_cache

    @property
    def cut_set_try_cache_hit(self) -> StatisticsComponentCounter:
        return self.__cut_set_try_cache_hit

    @property
    def two_cnf_formula_length(self) -> StatisticsComponentCounter:
        return self.__two_cnf_formula_length

    @property
    def renamable_horn_cnf_formula_length(self) -> StatisticsComponentCounter:
        return self.__renamable_horn_cnf_formula_length

    @property
    def copying_circuits(self) -> StatisticsComponentTimer:
        return self.__copying_circuits

    @property
    def copying_circuits_after(self) -> StatisticsComponentTimer:
        return self.__copying_circuits_after

    @property
    def copying_circuits_size(self) -> StatisticsComponentCounter:
        return self.__copying_circuits_size

    @property
    def copying_circuits_identity(self) -> StatisticsComponentCounter:
        return self.__copying_circuits_identity

    @property
    def copying_circuits_formula_length(self) -> StatisticsComponentCounter:
        return self.__copying_circuits_formula_length

    @property
    def copying_circuits_after_size(self) -> StatisticsComponentCounter:
        return self.__copying_circuits_after_size

    @property
    def copying_circuits_after_identity(self) -> StatisticsComponentCounter:
        return self.__copying_circuits_after_identity

    @property
    def copying_circuits_after_formula_length(self) -> StatisticsComponentCounter:
        return self.__copying_circuits_after_formula_length
    # endregion
