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
    
    Private StatisticsComponentCounter unsatisfiable
    Private StatisticsComponentCounter implied_literal
    Private StatisticsComponentCounter isolated_variable
    Private StatisticsComponentCounter empty_incidence_graph
    Private StatisticsComponentCounter generate_key_cache
    Private StatisticsComponentCounter cached
    Private StatisticsComponentCounter disjoint
    Private StatisticsComponentCounter decision_variable
    Private StatisticsComponentCounter recompute_cut_set
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

        self.__generate_key_cache: StatisticsComponentCounter = StatisticsComponentCounter("generate key cache", True)
        self._component_list.append(self.__generate_key_cache)

        self.__cached: StatisticsComponentCounter = StatisticsComponentCounter("cached")
        self._component_list.append(self.__cached)

        self.__disjoint: StatisticsComponentCounter = StatisticsComponentCounter("disjoint", True)
        self._component_list.append(self.__disjoint)

        self.__decision_variable: StatisticsComponentCounter = StatisticsComponentCounter("decision variable", True)
        self._component_list.append(self.__decision_variable)

        self.__recompute_cut_set: StatisticsComponentCounter = StatisticsComponentCounter("recompute cut set")
        self._component_list.append(self.__recompute_cut_set)

    # region Property
    @property
    def get_implied_literals(self):
        return self.__get_implied_literals

    @property
    def get_cut_set(self):
        return self.__get_cut_set

    @property
    def get_suggested_variable_from_cut_set(self):
        return self.__get_suggested_variable_from_cut_set

    @property
    def unsatisfiable(self):
        return self.__unsatisfiable

    @property
    def implied_literal(self):
        return self.__implied_literal

    @property
    def isolated_variable(self):
        return self.__isolated_variable

    @property
    def empty_incidence_graph(self):
        return self.__empty_incidence_graph

    @property
    def generate_key_cache(self):
        return self.__generate_key_cache

    @property
    def cached(self):
        return self.__cached

    @property
    def disjoint(self):
        return self.__disjoint

    @property
    def decision_variable(self):
        return self.__decision_variable

    @property
    def recompute_cut_set(self):
        return self.__recompute_cut_set
    # endregion
