# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract


class SolverStatistics(StatisticsTemplateAbstract):
    """
    Solver - statistics
    """

    """
    Private StatisticsComponentTime initialize
    Private StatisticsComponentTime first_implied_literals
    Private StatisticsComponentTime is_satisfiable
    Private StatisticsComponentTime unit_propagation
    Private StatisticsComponentTime implicit_unit_propagation
    Private StatisticsComponentTime iterative_implicit_unit_propagation
    Private StatisticsComponentTime backbone_literals
    """

    def __init__(self, name: str):
        super().__init__(name)

        self.__initialize = StatisticsComponentTimer("initialize")
        self._component_list.append(self.__initialize)

        self.__first_implied_literals = StatisticsComponentTimer("first implied literals")
        self._component_list.append(self.__first_implied_literals)

        self.__is_satisfiable = StatisticsComponentTimer("is satisfiable")
        self._component_list.append(self.__is_satisfiable)

        self.__unit_propagation = StatisticsComponentTimer("unit propagation")
        self._component_list.append(self.__unit_propagation)

        self.__implicit_unit_propagation = StatisticsComponentTimer("implicit unit propagation")
        self._component_list.append(self.__implicit_unit_propagation)

        self.__iterative_implicit_unit_propagation = StatisticsComponentTimer("iterative implicit unit propagation")
        self._component_list.append(self.__iterative_implicit_unit_propagation)

        self.__backbone_literals = StatisticsComponentTimer("backbone literals")
        self._component_list.append(self.__backbone_literals)

    # region Property
    @property
    def initialize(self):
        return self.__initialize

    @property
    def first_implied_literals(self):
        return self.__first_implied_literals

    @property
    def is_satisfiable(self):
        return self.__is_satisfiable

    @property
    def unit_propagation(self):
        return self.__unit_propagation

    @property
    def implicit_unit_propagation(self):
        return self.__implicit_unit_propagation

    @property
    def iterative_implicit_unit_propagation(self):
        return self.__iterative_implicit_unit_propagation

    @property
    def backbone_literals(self):
        return self.__backbone_literals
    # endregion
