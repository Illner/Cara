# Import
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter
from compiler_statistics.statistics_template_abstract import StatisticsTemplateAbstract


class SolverStatistics(StatisticsTemplateAbstract):
    """
    Solver - statistics
    """

    """
    Private StatisticsComponentTimer initialize
    Private StatisticsComponentTimer first_implied_literals
    Private StatisticsComponentTimer is_satisfiable
    Private StatisticsComponentTimer unit_propagation
    Private StatisticsComponentTimer implicit_unit_propagation
    Private StatisticsComponentTimer iterative_implicit_unit_propagation
    Private StatisticsComponentCounter iterative_implicit_unit_propagation_iteration
    Private StatisticsComponentTimer backbone_literals
    """

    def __init__(self, active: bool):
        super().__init__("Solver")

        self.__initialize: StatisticsComponentTimer = StatisticsComponentTimer(name="initialize", active=active)
        self._component_list.append(self.__initialize)

        self.__first_implied_literals: StatisticsComponentTimer = StatisticsComponentTimer(name="first implied literals", active=active)
        self._component_list.append(self.__first_implied_literals)

        self.__is_satisfiable: StatisticsComponentTimer = StatisticsComponentTimer(name="is satisfiable", active=active)
        self._component_list.append(self.__is_satisfiable)

        self.__unit_propagation: StatisticsComponentTimer = StatisticsComponentTimer(name="unit propagation", active=active)
        self._component_list.append(self.__unit_propagation)

        self.__implicit_unit_propagation: StatisticsComponentTimer = StatisticsComponentTimer(name="implicit unit propagation", active=active)
        self._component_list.append(self.__implicit_unit_propagation)

        self.__iterative_implicit_unit_propagation: StatisticsComponentTimer = StatisticsComponentTimer(name="iterative implicit unit propagation", active=active)
        self._component_list.append(self.__iterative_implicit_unit_propagation)

        self.__iterative_implicit_unit_propagation_iteration: StatisticsComponentCounter = StatisticsComponentCounter(name="iterative implicit unit propagation - iteration", active=active)
        self._component_list.append(self.__iterative_implicit_unit_propagation_iteration)

        self.__backbone_literals: StatisticsComponentTimer = StatisticsComponentTimer(name="backbone literals", active=active)
        self._component_list.append(self.__backbone_literals)

    # region Property
    @property
    def initialize(self) -> StatisticsComponentTimer:
        return self.__initialize

    @property
    def first_implied_literals(self) -> StatisticsComponentTimer:
        return self.__first_implied_literals

    @property
    def is_satisfiable(self) -> StatisticsComponentTimer:
        return self.__is_satisfiable

    @property
    def unit_propagation(self) -> StatisticsComponentTimer:
        return self.__unit_propagation

    @property
    def implicit_unit_propagation(self) -> StatisticsComponentTimer:
        return self.__implicit_unit_propagation

    @property
    def iterative_implicit_unit_propagation(self) -> StatisticsComponentTimer:
        return self.__iterative_implicit_unit_propagation

    @property
    def iterative_implicit_unit_propagation_iteration(self) -> StatisticsComponentCounter:
        return self.__iterative_implicit_unit_propagation_iteration

    @property
    def backbone_literals(self) -> StatisticsComponentTimer:
        return self.__backbone_literals
    # endregion
