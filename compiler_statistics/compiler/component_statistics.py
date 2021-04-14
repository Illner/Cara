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
    Private StatisticsComponentTimer get_cut_set
    Private StatisticsComponentTimer get_suggested_variable_from_cut_set
    Private StatisticsComponentTimer cut_set_try_cache
    
    Private StatisticsComponentCounter unsatisfiable
    Private StatisticsComponentCounter implied_literal
    Private StatisticsComponentCounter isolated_variable
    Private StatisticsComponentCounter empty_incidence_graph
    Private StatisticsComponentCounter generate_key_cache
    Private StatisticsComponentCounter cached
    Private StatisticsComponentCounter disjoint
    Private StatisticsComponentCounter decision_variable
    Private StatisticsComponentCounter recompute_cut_set
    Private StatisticsComponentCounter cut_set_try_cache_cached
    Private StatisticsComponentCounter two_cnf_formula_length
    Private StatisticsComponentCounter renamable_horn_cnf_formula_length
    """

    def __init__(self):
        super().__init__("Component")

        self.__get_implied_literals: StatisticsComponentTimer = StatisticsComponentTimer("get implied literals")
        self._component_list.append(self.__get_implied_literals)

        self.__get_cut_set: StatisticsComponentTimer = StatisticsComponentTimer("get cut set")
        self._component_list.append(self.__get_cut_set)

        self.__get_suggested_variable_from_cut_set: StatisticsComponentTimer = StatisticsComponentTimer("suggest variable from cut set")
        self._component_list.append(self.__get_suggested_variable_from_cut_set)

        self.__unsatisfiable: StatisticsComponentCounter = StatisticsComponentCounter("unsatisfiable subformulae", True)
        self._component_list.append(self.__unsatisfiable)

        self.__implied_literal: StatisticsComponentCounter = StatisticsComponentCounter("implied literal")
        self._component_list.append(self.__implied_literal)

        self.__isolated_variable: StatisticsComponentCounter = StatisticsComponentCounter("isolated variable")
        self._component_list.append(self.__isolated_variable)

        self.__empty_incidence_graph: StatisticsComponentCounter = StatisticsComponentCounter("empty incidence graph", True)
        self._component_list.append(self.__empty_incidence_graph)

        self.__generate_key_cache: StatisticsComponentCounter = StatisticsComponentCounter("component cache - generate key cache", True)
        self._component_list.append(self.__generate_key_cache)

        self.__cached: StatisticsComponentCounter = StatisticsComponentCounter("component cache - cached")
        self._component_list.append(self.__cached)

        self.__disjoint: StatisticsComponentCounter = StatisticsComponentCounter("disjoint", True)
        self._component_list.append(self.__disjoint)

        self.__decision_variable: StatisticsComponentCounter = StatisticsComponentCounter("decision variable", True)
        self._component_list.append(self.__decision_variable)

        self.__recompute_cut_set: StatisticsComponentCounter = StatisticsComponentCounter("recompute cut set")
        self._component_list.append(self.__recompute_cut_set)

        self.__cut_set_try_cache: StatisticsComponentTimer = StatisticsComponentTimer("cut set try cache")
        self._component_list.append(self.__cut_set_try_cache)

        self.__cut_set_try_cache_cached: StatisticsComponentCounter = StatisticsComponentCounter("cut set try cache - cached")
        self._component_list.append(self.__cut_set_try_cache_cached)

        self.__two_cnf_formula_length: StatisticsComponentCounter = StatisticsComponentCounter("2-CNF - formula length")
        self._component_list.append(self.__two_cnf_formula_length)

        self.__renamable_horn_cnf_formula_length: StatisticsComponentCounter = StatisticsComponentCounter("renamable Horn formula - formula length")
        self._component_list.append(self.__renamable_horn_cnf_formula_length)

    # region Property
    @property
    def get_implied_literals(self) -> StatisticsComponentTimer:
        return self.__get_implied_literals

    @property
    def get_cut_set(self) -> StatisticsComponentTimer:
        return self.__get_cut_set

    @property
    def get_suggested_variable_from_cut_set(self) -> StatisticsComponentTimer:
        return self.__get_suggested_variable_from_cut_set

    @property
    def unsatisfiable(self) -> StatisticsComponentCounter:
        return self.__unsatisfiable

    @property
    def implied_literal(self) -> StatisticsComponentCounter:
        return self.__implied_literal

    @property
    def isolated_variable(self) -> StatisticsComponentCounter:
        return self.__isolated_variable

    @property
    def empty_incidence_graph(self) -> StatisticsComponentCounter:
        return self.__empty_incidence_graph

    @property
    def generate_key_cache(self) -> StatisticsComponentCounter:
        return self.__generate_key_cache

    @property
    def cached(self) -> StatisticsComponentCounter:
        return self.__cached

    @property
    def disjoint(self) -> StatisticsComponentCounter:
        return self.__disjoint

    @property
    def decision_variable(self) -> StatisticsComponentCounter:
        return self.__decision_variable

    @property
    def recompute_cut_set(self) -> StatisticsComponentCounter:
        return self.__recompute_cut_set

    @property
    def cut_set_try_cache(self) -> StatisticsComponentTimer:
        return self.__cut_set_try_cache

    @property
    def cut_set_try_cache_cached(self) -> StatisticsComponentCounter:
        return self.__cut_set_try_cache_cached

    @property
    def two_cnf_formula_length(self) -> StatisticsComponentCounter:
        return self.__two_cnf_formula_length

    @property
    def renamable_horn_cnf_formula_length(self) -> StatisticsComponentCounter:
        return self.__renamable_horn_cnf_formula_length
    # endregion
