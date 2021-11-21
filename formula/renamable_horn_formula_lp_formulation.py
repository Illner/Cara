# Import
import pulp
from io import StringIO, FileIO
from typing import Dict, Union, TextIO, Set
from pulp import LpVariable, LpContinuous, LpInteger, lpSum, PULP_CBC_CMD
from compiler_statistics.formula.renamable_horn_formula_lp_formulation_statistics import RenamableHornFormulaLpFormulationStatistics

# Import exception
import exception.cara_exception as c_exception
import exception.formula.renamable_horn_formula_lp_formulation_exception as rhflpf_exception

# Import enum
import formula.enum.lp_formulation_type_enum as lpft_enum


class RenamableHornFormulaLpFormulation:
    """
    A linear programming formulation of problem MRH
    """

    """
    Private LpSolver lp_solver
    Private LpProblem lp_formulation
    Private Dict<int, LpVariable> lp_variable_clause_is_horn            # z_C
    Private Dict<int, LpVariable> lp_variable_variable_is_switched      # s_i
    
    Private bool is_exact
    Private Dict<int, int> clause_length_dictionary
    Private LpFormulationTypeEnum lp_formulation_type
    Private Set<int> clauses_with_variables_in_cut_set
    Private Dict<int, int> clause_number_of_variables_in_cut_set_dictionary
    
    Private RenamableHornFormulaLpFormulationStatistics statistics
    """

    def __init__(self, incidence_graph, number_of_threads: int = 8, is_exact: bool = False,
                 lp_formulation_type: lpft_enum.LpFormulationTypeEnum = lpft_enum.LpFormulationTypeEnum.HORN_FORMULA, cut_set: Union[Set[int], None] = None,
                 weight_for_variables_not_in_cut_set: int = 2, statistics: Union[RenamableHornFormulaLpFormulationStatistics, None] = None):
        # Statistics
        if statistics is None:
            self.__statistics: RenamableHornFormulaLpFormulationStatistics = RenamableHornFormulaLpFormulationStatistics(active=False)
        else:
            self.__statistics: RenamableHornFormulaLpFormulationStatistics = statistics

        self.__is_exact: bool = is_exact
        self.__clause_length_dictionary: Dict[int, int] = dict()
        self.__lp_formulation_type: lpft_enum.LpFormulationTypeEnum = lp_formulation_type

        self.__lp_solver = PULP_CBC_CMD(msg=False,
                                        threads=number_of_threads)

        self.__statistics.create_lp_formulation.start_stopwatch()   # timer (start)

        # Variables
        self.__lp_variable_clause_is_horn: Union[Dict[int, LpVariable], None] = None
        self.__lp_variable_variable_is_switched = LpVariable.dicts(name="s",
                                                                   indexs=incidence_graph.variable_set(copy=False),
                                                                   lowBound=0,
                                                                   upBound=1,
                                                                   cat=LpInteger if self.__is_exact else LpContinuous)

        # Clause length
        for clause_id in incidence_graph.clause_id_set(copy=False):
            self.__clause_length_dictionary[clause_id] = incidence_graph.get_clause_length(clause_id)

        # Cut set
        self.__clauses_with_variables_in_cut_set: Set[int] = set()
        self.__clause_number_of_variables_in_cut_set_dictionary: Dict[int, int] = dict()

        if self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_HORN_FORMULA:

            # Cut set is not defined
            if cut_set is None:
                raise rhflpf_exception.CutSetIsNotDefinedException(self.__lp_formulation_type)

            for variable in cut_set:
                temp = incidence_graph.variable_neighbour_set(variable)
                self.__clauses_with_variables_in_cut_set.update(temp)

                for clause_id in temp:
                    if clause_id not in self.__clause_number_of_variables_in_cut_set_dictionary:
                        self.__clause_number_of_variables_in_cut_set_dictionary[clause_id] = 0

                    self.__clause_number_of_variables_in_cut_set_dictionary[clause_id] += 1

        # Number of Horn formulae
        if (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.HORN_FORMULA) or \
           (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.LENGTH_WEIGHTED_HORN_FORMULA) or \
           (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.SQUARED_LENGTH_WEIGHTED_HORN_FORMULA) or \
           (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.INVERSE_LENGTH_WEIGHTED_HORN_FORMULA) or \
           (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.SQUARED_INVERSE_LENGTH_WEIGHTED_HORN_FORMULA) or \
           (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_HORN_FORMULA):

            self.__lp_formulation = pulp.LpProblem(name="Number_of_Horn_formulae",
                                                   sense=pulp.LpMaximize)
            self.__create_lp_formulation_number_of_horn_formulae(incidence_graph=incidence_graph,
                                                                 weight_for_variables_not_in_cut_set=weight_for_variables_not_in_cut_set)

        # Number of edges
        elif (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.NUMBER_OF_EDGES) or \
             (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_NUMBER_OF_EDGES):

            self.__lp_formulation = pulp.LpProblem(name="Number_of_edges",
                                                   sense=pulp.LpMinimize)
            self.__create_lp_formulation_number_edges(incidence_graph=incidence_graph,
                                                      weight_for_variables_not_in_cut_set=weight_for_variables_not_in_cut_set)

        # Number of vertices
        elif (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.NUMBER_OF_VERTICES) or \
             (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_NUMBER_OF_VERTICES):

            self.__lp_formulation = pulp.LpProblem(name="Number_of_vertices",
                                                   sense=pulp.LpMinimize)
            self.__create_lp_formulation_number_vertices(incidence_graph=incidence_graph,
                                                         weight_for_variables_not_in_cut_set=weight_for_variables_not_in_cut_set)

        # Vertex cover
        elif (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.VERTEX_COVER) or \
             (self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_VERTEX_COVER):

            self.__lp_formulation = pulp.LpProblem(name="Vertex_cover",
                                                   sense=pulp.LpMinimize)
            self.__create_lp_formulation_vertex_cover(incidence_graph=incidence_graph,
                                                      weight_for_variables_not_in_cut_set=weight_for_variables_not_in_cut_set)

        # Not implemented
        else:
            raise c_exception.FunctionNotImplementedException("renamable_horn_formula_lp_formulation",
                                                              f"this type of LP formulation ({self.__lp_formulation_type.name}) is not implemented")

        self.__statistics.create_lp_formulation.stop_stopwatch()    # timer (stop)

    # region Private method
    def __create_lp_formulation_number_of_horn_formulae(self, incidence_graph, weight_for_variables_not_in_cut_set: int) -> None:
        # Variables
        self.__lp_variable_clause_is_horn = LpVariable.dicts(name="z",
                                                             indexs=incidence_graph.clause_id_set(copy=False),
                                                             lowBound=0,
                                                             upBound=1,
                                                             cat=LpInteger if self.__is_exact else LpContinuous)

        # Constraints
        for clause_id in self.__lp_variable_clause_is_horn:
            clause = incidence_graph.get_clause(clause_id=clause_id, copy=False)
            clause_length = self.__clause_length_dictionary[clause_id]
            self.__lp_formulation.addConstraint(lpSum([self.__lp_variable_variable_is_switched[abs(lit)] if -lit > 0 else (1 - self.__lp_variable_variable_is_switched[abs(lit)]) for lit in clause]) <= clause_length - self.__lp_variable_clause_is_horn[clause_id] * (clause_length - 1), f"clause_{clause_id}")

        # Objective function
        # HORN_FORMULA
        if self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.HORN_FORMULA:
            self.__lp_formulation.setObjective(lpSum(self.__lp_variable_clause_is_horn))

        # LENGTH_WEIGHTED_HORN_FORMULA
        elif self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.LENGTH_WEIGHTED_HORN_FORMULA:
            self.__lp_formulation.setObjective(lpSum([self.__lp_variable_clause_is_horn[clause_id] * self.__clause_length_dictionary[clause_id] for clause_id in self.__lp_variable_clause_is_horn]))

        # SQUARED_LENGTH_WEIGHTED_HORN_FORMULA
        elif self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.SQUARED_LENGTH_WEIGHTED_HORN_FORMULA:
            self.__lp_formulation.setObjective(lpSum([self.__lp_variable_clause_is_horn[clause_id] * (self.__clause_length_dictionary[clause_id] ** 2) for clause_id in self.__lp_variable_clause_is_horn]))

        # INVERSE_LENGTH_WEIGHTED_HORN_FORMULA
        elif self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.INVERSE_LENGTH_WEIGHTED_HORN_FORMULA:
            self.__lp_formulation.setObjective(lpSum([self.__lp_variable_clause_is_horn[clause_id] * 1/self.__clause_length_dictionary[clause_id] for clause_id in self.__lp_variable_clause_is_horn]))

        # SQUARED_INVERSE_LENGTH_WEIGHTED_HORN_FORMULA
        elif self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.SQUARED_INVERSE_LENGTH_WEIGHTED_HORN_FORMULA:
            self.__lp_formulation.setObjective(lpSum([self.__lp_variable_clause_is_horn[clause_id] * ((1/self.__clause_length_dictionary[clause_id]) ** 2) for clause_id in self.__lp_variable_clause_is_horn]))

        # RESPECT_DECOMPOSITION_HORN_FORMULA
        elif self.__lp_formulation_type == lpft_enum.LpFormulationTypeEnum.RESPECT_DECOMPOSITION_HORN_FORMULA:
            self.__lp_formulation.setObjective(lpSum([self.__lp_variable_clause_is_horn[clause_id] * (1/self.__clause_number_of_variables_in_cut_set_dictionary[clause_id] if clause_id in self.__clauses_with_variables_in_cut_set else weight_for_variables_not_in_cut_set) for clause_id in self.__lp_variable_clause_is_horn]))

        # Not implemented
        else:
            raise c_exception.FunctionNotImplementedException("__create_lp_formulation_number_of_horn_formulae",
                                                              f"this type of LP formulation ({self.__lp_formulation_type.name}) is not implemented")

    def __create_lp_formulation_number_edges(self, incidence_graph, weight_for_variables_not_in_cut_set: int) -> None:
        pass

    def __create_lp_formulation_number_vertices(self, incidence_graph, weight_for_variables_not_in_cut_set: int) -> None:
        pass

    def __create_lp_formulation_vertex_cover(self, incidence_graph, weight_for_variables_not_in_cut_set: int) -> None:
        pass
    # endregion

    # region Public method
    def solve(self) -> Dict[int, float]:
        """
        Solve the LP problem
        :return: (variable, probability of switching)
        :raises SolutionDoesNotExistException: a solution does not exist
        """

        self.__statistics.solve_lp_problem.start_stopwatch()    # timer (start)

        self.__lp_formulation.solve(self.__lp_solver)

        status = self.__lp_formulation.status

        # A solution does not exist
        if status != pulp.LpStatusOptimal:
            raise rhflpf_exception.SolutionDoesNotExistException(status)

        switching_dictionary: Dict[int, float] = dict()

        # Switching
        switching_sum = 0
        for variable in self.__lp_variable_variable_is_switched:
            s_i = self.__lp_variable_variable_is_switched[variable].varValue
            switching_dictionary[variable] = s_i

            switching_sum += s_i

        self.__statistics.switching_average.add_count(switching_sum / len(self.__lp_variable_variable_is_switched))  # counter

        # Horn - statistics
        if self.__lp_variable_clause_is_horn is not None:
            horn_clauses_after_switching_sum = 0
            horn_clauses_after_switching_length = 0
            for clause_id in self.__lp_variable_clause_is_horn:
                z_i = self.__lp_variable_clause_is_horn[clause_id].varValue
                horn_clauses_after_switching_sum += z_i
                horn_clauses_after_switching_length += z_i * self.__clause_length_dictionary[clause_id]

            self.__statistics.horn_clauses_after_switching_average.add_count(horn_clauses_after_switching_sum / len(self.__lp_variable_clause_is_horn))     # counter
            self.__statistics.horn_clauses_after_switching_length.add_count(horn_clauses_after_switching_length / len(self.__lp_variable_clause_is_horn))   # counter

        self.__statistics.solve_lp_problem.stop_stopwatch()     # timer (stop)

        return switching_dictionary

    def save_to_io(self, source: Union[FileIO, StringIO, TextIO]) -> None:
        """
        Save the LP formulation to the IO
        :return: None
        """

        source.write("\\* " + self.__lp_formulation.name + " *\\\n")
        if self.__lp_formulation.sense == 1:
            source.write("Minimize\n")
        else:
            source.write("Maximize\n")

        was_none, objective_dummy_var = self.__lp_formulation.fixObjective()
        obj_name = self.__lp_formulation.objective.name
        if not obj_name:
            obj_name = "OBJ"

        source.write(self.__lp_formulation.objective.asCplexLpAffineExpression(obj_name, constant=0))
        source.write("Subject To\n")
        ks = list(self.__lp_formulation.constraints.keys())
        ks.sort()
        dummy_written = False
        for k in ks:
            constraint = self.__lp_formulation.constraints[k]
            if not list(constraint.keys()):
                # empty constraint add the dummy_var
                dummy_var = self.__lp_formulation.get_dummyVar()
                constraint += dummy_var
                # set this dummy_var to zero so infeasible problems are not made feasible
                if not dummy_written:
                    source.write((dummy_var == 0.0).asCplexLpConstraint("_dummy"))
                    dummy_written = True
            source.write(constraint.asCplexLpConstraint(k))

        vs = self.__lp_formulation.variables()
        # check for repeated names
        self.__lp_formulation.checkDuplicateVars()

        # Bounds on non-"positive" variables
        # explicit bounds
        vg = [v for v in vs if not (v.isPositive() and v.cat == LpContinuous) and not v.isBinary()]
        if vg:
            source.write("Bounds\n")
            for v in vg:
                source.write(" %s\n" % v.asCplexLpVariable())

        # Integer non-binary variables
        vg = [v for v in vs if v.cat == LpInteger and not v.isBinary()]
        if vg:
            source.write("Generals\n")
            for v in vg:
                source.write("%s\n" % v.name)

        # Binary variables
        vg = [v for v in vs if v.isBinary()]
        if vg:
            source.write("Binaries\n")
            for v in vg:
                source.write("%s\n" % v.name)

        # Special Ordered Sets
        if self.__lp_formulation.sos1 or self.__lp_formulation.sos2:
            source.write("SOS\n")
            if self.__lp_formulation.sos1:
                for sos in self.__lp_formulation.sos1.values():
                    source.write("S1:: \n")
                    for v, val in sos.items():
                        source.write(" %s: %.12g\n" % (v.name, val))
            if self.__lp_formulation.sos2:
                for sos in self.__lp_formulation.sos2.values():
                    source.write("S2:: \n")
                    for v, val in sos.items():
                        source.write(" %s: %.12g\n" % (v.name, val))

        source.write("End\n")
        self.__lp_formulation.restoreObjective(was_none, objective_dummy_var)
        return vs
    # endregion

    # region Magic method
    def __str__(self):
        temp = StringIO()
        self.save_to_io(temp)

        string_temp = temp.getvalue()
        temp.close()

        return string_temp
    # endregion
