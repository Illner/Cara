# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract


class HypergraphPartitioningStatistics(StatisticsTemplateAbstract):
    """
    Hypergraph partitioning - statistics
    """

    """
    Private StatisticsComponentTimer variable_simplification
    Private StatisticsComponentTimer set_static_weights
    Private StatisticsComponentTimer set_dynamic_weights
    Private StatisticsComponentTimer generate_key_cache
    Private StatisticsComponentTimer get_cut_set
    
    Private StatisticsComponentCounter cache_hit
    Private StatisticsComponentCounter cache_multi_occurrent_clauses
    Private StatisticsComponentCounter cut_set_size
    Private StatisticsComponentCounter empty_cut_set
    Private StatisticsComponentCounter hypergraph_number_of_nodes
    Private StatisticsComponentCounter hypergraph_number_of_hyperedges
    Private StatisticsComponentCounter ratio_log_cut_set_size_and_log_number_of_hyperedges
    """

    def __init__(self, active: bool):
        super().__init__("Hypergraph partitioning")

        self.__variable_simplification: StatisticsComponentTimer = StatisticsComponentTimer(name="variable simplification", active=active)
        self._component_list.append(self.__variable_simplification)

        self.__set_static_weights: StatisticsComponentTimer = StatisticsComponentTimer(name="set static weights",
                                                                                       active=active,
                                                                                       show_only_sum_time=True)
        self._component_list.append(self.__set_static_weights)

        self.__set_dynamic_weights: StatisticsComponentTimer = StatisticsComponentTimer(name="set dynamic weights", active=active)
        self._component_list.append(self.__set_dynamic_weights)

        self.__generate_key_cache: StatisticsComponentTimer = StatisticsComponentTimer(name="generate key cache", active=active)
        self._component_list.append(self.__generate_key_cache)

        self.__get_cut_set: StatisticsComponentTimer = StatisticsComponentTimer(name="get cut set", active=active)
        self._component_list.append(self.__get_cut_set)

        self.__cache_hit: StatisticsComponentCounter = StatisticsComponentCounter(name="cache - hit", active=active)
        self._component_list.append(self.__cache_hit)

        self.__cache_multi_occurrent_clauses: StatisticsComponentCounter = StatisticsComponentCounter(name="cache - number of multi-occurrent clauses", active=active)
        self._component_list.append(self.__cache_multi_occurrent_clauses)

        self.__cut_set_size: StatisticsComponentCounter = StatisticsComponentCounter(name="cut set - size", active=active)
        self._component_list.append(self.__cut_set_size)

        self.__empty_cut_set: StatisticsComponentCounter = StatisticsComponentCounter(name="empty cut set",
                                                                                      active=active,
                                                                                      show_only_number_of_calls=True)
        self._component_list.append(self.__empty_cut_set)

        self.__hypergraph_number_of_nodes: StatisticsComponentCounter = StatisticsComponentCounter(name="hypergraph - number of nodes", active=active)
        self._component_list.append(self.__hypergraph_number_of_nodes)

        self.__hypergraph_number_of_hyperedges: StatisticsComponentCounter = StatisticsComponentCounter(name="hypergraph - number of hyperedges", active=active)
        self._component_list.append(self.__hypergraph_number_of_hyperedges)

        self.__ratio_log_cut_set_size_and_log_number_of_hyperedges: StatisticsComponentCounter = StatisticsComponentCounter(name="log(cut set size) / log(number of hyperedges)", active=active)
        self._component_list.append(self.__ratio_log_cut_set_size_and_log_number_of_hyperedges)

    # region Property
    @property
    def variable_simplification(self) -> StatisticsComponentTimer:
        return self.__variable_simplification

    @property
    def set_static_weights(self) -> StatisticsComponentTimer:
        return self.__set_static_weights

    @property
    def set_dynamic_weights(self) -> StatisticsComponentTimer:
        return self.__set_dynamic_weights

    @property
    def generate_key_cache(self) -> StatisticsComponentTimer:
        return self.__generate_key_cache

    @property
    def get_cut_set(self) -> StatisticsComponentTimer:
        return self.__get_cut_set

    @property
    def cache_hit(self) -> StatisticsComponentCounter:
        return self.__cache_hit

    @property
    def cache_multi_occurrent_clauses(self) -> StatisticsComponentCounter:
        return self.__cache_multi_occurrent_clauses

    @property
    def cut_set_size(self) -> StatisticsComponentCounter:
        return self.__cut_set_size

    @property
    def empty_cut_set(self) -> StatisticsComponentCounter:
        return self.__empty_cut_set

    @property
    def hypergraph_number_of_nodes(self) -> StatisticsComponentCounter:
        return self.__hypergraph_number_of_nodes

    @property
    def hypergraph_number_of_hyperedges(self) -> StatisticsComponentCounter:
        return self.__hypergraph_number_of_hyperedges

    @property
    def ratio_log_cut_set_size_and_log_number_of_hyperedges(self) -> StatisticsComponentCounter:
        return self.__ratio_log_cut_set_size_and_log_number_of_hyperedges
    # endregion
