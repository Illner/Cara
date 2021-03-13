# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract


class HypergraphPartitioningStatistics(StatisticsTemplateAbstract):
    """
    Hypergraph partitioning - statistics
    """

    """
    Private StatisticsComponentTimer subsumption
    Private StatisticsComponentTimer variable_simplification
    Private StatisticsComponentTimer set_static_weights
    Private StatisticsComponentTimer set_dynamic_weights
    Private StatisticsComponentTimer generate_key_cache
    Private StatisticsComponentTimer get_cut_set
    Private StatisticsComponentCounter cache
    """

    def __init__(self):
        super().__init__("Hypergraph partitioning")

        self.__subsumption: StatisticsComponentTimer = StatisticsComponentTimer("subsumption")
        self._component_list.append(self.__subsumption)

        self.__variable_simplification: StatisticsComponentTimer = StatisticsComponentTimer("variable simplification")
        self._component_list.append(self.__variable_simplification)

        self.__set_static_weights: StatisticsComponentTimer = StatisticsComponentTimer("set static weights")
        self._component_list.append(self.__set_static_weights)

        self.__set_dynamic_weights: StatisticsComponentTimer = StatisticsComponentTimer("set dynamic weights")
        self._component_list.append(self.__set_dynamic_weights)

        self.__generate_key_cache: StatisticsComponentTimer = StatisticsComponentTimer("generate key cache")
        self._component_list.append(self.__generate_key_cache)

        self.__get_cut_set: StatisticsComponentTimer = StatisticsComponentTimer("get cut set")
        self._component_list.append(self.__get_cut_set)

        self.__cache: StatisticsComponentCounter = StatisticsComponentCounter("cache")
        self._component_list.append(self.__cache)

    # region Property
    @property
    def subsumption(self):
        return self.__subsumption

    @property
    def variable_simplification(self):
        return self.__variable_simplification

    @property
    def set_static_weights(self):
        return self.__set_static_weights

    @property
    def set_dynamic_weights(self):
        return self.__set_dynamic_weights

    @property
    def generate_key_cache(self):
        return self.__generate_key_cache

    @property
    def get_cut_set(self):
        return self.__get_cut_set

    @property
    def cache(self):
        return self.__cache
    # endregion
