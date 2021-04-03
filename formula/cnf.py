# Import
import warnings
from io import StringIO
from typing import Set, Dict, List, Union
from formula.incidence_graph import IncidenceGraph
from compiler_statistics.formula.cnf_statistics import CnfStatistics
from compiler_statistics.formula.incidence_graph_statistics import IncidenceGraphStatistics

# Import exception
import exception.formula.formula_exception as f_exception


class Cnf:
    """
    CNF representation
    """

    """
    Private str comments
    Private int number_of_clauses
    Private int real_number_of_clauses
    Private int number_of_variables
    Private int real_number_of_variables
    Private int number_of_literals                              # 2 * number_of_variables
    Private List<Set<int>> cnf                                  # key: 0, 1, .., number_of_clauses - 1, value: a set of literals which appear in the clause
    Private List<Set<int>> cnf_variable                         # key: 0, 1, .., number_of_clauses - 1, value: a set of variables which appear in the clause
    Private List<int> variable_list
    Private Set<int> variable_set
    Private List<int> literal_list
    Private Set<int> literal_set
    Private Dict<int, Set<int>> adjacency_literal_dictionary    # key: literal, value: a set of clauses where the literal appears
    Private Dict<int, Set<int>> adjacency_variable_dictionary   # key: variable, value: a set of clauses where the variable appears
    Private Set<int> unit_clause_set                            # a set which contains all unit clauses
    Private List<Set<int>> clause_size_list                     # key: 0, 1, .., number_of_variables, value: a set contains all clauses with the size k
    
    Private CnfStatistics cnf_statistics
    Private IncidenceGraphStatistics incidence_graph_statistics
    
    Private IncidenceGraph incidence_graph
    """

    def __init__(self, dimacs_cnf_source: Union[str, StringIO], starting_line_id: int = 0,
                 cnf_statistics: Union[CnfStatistics, None] = None,
                 incidence_graph_statistics: Union[IncidenceGraphStatistics, None] = None):
        # region Initialization
        self.__comments: str = ""
        self.__number_of_clauses: int = 0
        self.__real_number_of_clauses: int = 0
        self.__number_of_variables: int = 0
        self.__real_number_of_variables: int = 0
        self.__number_of_literals: int = 0
        self.__cnf: List[Set[int]] = []
        self.__cnf_variable: List[Set[int]] = []
        self.__variable_list: List[int] = []
        self.__variable_set: Set[int] = set()
        self.__literal_list: List[int] = []
        self.__literal_set: Set[int] = set()

        self.__adjacency_literal_dictionary: Dict[int, Set[int]] = dict()
        self.__adjacency_variable_dictionary: Dict[int, Set[int]] = dict()
        self.__unit_clause_set: Set[int] = set()
        self.__clause_size_list: List[Set[int]] = []
        # endregion

        # Statistics - CNF
        if cnf_statistics is None:
            self.__cnf_statistics: CnfStatistics = CnfStatistics()
        else:
            self.__cnf_statistics: CnfStatistics = cnf_statistics
        # Statistics - incidence graph
        self.__incidence_graph_statistics: Union[IncidenceGraphStatistics, None] = incidence_graph_statistics

        # Incidence graph
        self.__incidence_graph: Union[IncidenceGraph, None] = None

        self.__create_cnf(dimacs_cnf_source, starting_line_id)

    # region Private method
    def __create_cnf(self, dimacs_cnf_source: Union[str, StringIO], starting_line_id: int) -> None:
        """
        Convert the formula from the file/IO into our structure
        :param dimacs_cnf_source: the file/IO, which is in the DIMACS CNF format
        :param starting_line_id: the starting line ID
        :return: None
        :raises InvalidDimacsCnfFormatException, PLineIsNotMentionedException: if the DIMACS CNF format in the file/IO is invalid
        """

        self.__cnf_statistics.create.start_stopwatch()      # timer (start)

        io = dimacs_cnf_source
        if isinstance(dimacs_cnf_source, str):
            io = open(dimacs_cnf_source, "r", encoding="utf-8")

        try:
            line_id = starting_line_id

            clause_id = 0
            is_p_line_defined = False

            while True:
                line = io.readline()
                line_id += 1

                # End of the file
                if not line:
                    break

                line = line.strip()

                # The line is empty
                if not line:
                    continue

                # Comment line
                if line.startswith("C") or line.startswith("c"):
                    if not self.__comments:     # First comment
                        self.__comments = line[1:].strip()
                    else:
                        self.__comments = "\n".join((self.__comments, line[1:].strip()))
                    continue

                # End of the file (optional)
                if line.startswith("%"):
                    break

                # P line
                if line.startswith("P") or line.startswith("p"):
                    is_p_line_defined = True
                    line_array_temp = line.split()

                    # P line has an invalid format
                    if len(line_array_temp) != 4:   # p cnf number_of_variables number_of_clauses
                        raise f_exception.InvalidDimacsCnfFormatException("p line has an invalid format. The valid format is 'p cnf number_of_variables number_of_clauses'")

                    # Parse the parameters
                    try:
                        self.__number_of_variables = int(line_array_temp[2])
                        self.__number_of_clauses = int(line_array_temp[3])
                    except ValueError:
                        raise f_exception.InvalidDimacsCnfFormatException(f"the number of variables ({line_array_temp[2]}) or the number of clauses ({line_array_temp[3]}) is not an integer")

                    self.__number_of_literals = 2 * self.__number_of_variables

                    for _ in range(self.__number_of_variables + 1):
                        self.__clause_size_list.append(set())   # initialization

                    # Incidence graph
                    self.__incidence_graph = IncidenceGraph(statistics=self.__incidence_graph_statistics)

                    continue

                # P line has not been mentioned
                if not is_p_line_defined:
                    raise f_exception.PLineIsNotMentionedException()

                # Clause line
                line_array_temp = line.split()

                # Invalid line
                if line_array_temp.pop() != "0":
                    raise f_exception.InvalidDimacsCnfFormatException(f"the clause ({line}) defined on line {line_id} doesn't end with 0")

                clause_set_temp = set()
                try:
                    for lit in line_array_temp:
                        lit = int(lit)

                        # (lit v lit) in the clause
                        if lit in clause_set_temp:
                            continue

                        # (lit v -lit) in the clause
                        if -lit in clause_set_temp:
                            clause_set_temp = set()
                            break

                        clause_set_temp.add(lit)
                except ValueError:
                    raise f_exception.InvalidDimacsCnfFormatException(f"invalid clause ({line}) defined on line {line_id}")

                # The clause is empty or contains two opposite literals
                if not clause_set_temp:
                    continue

                clause_variable_set_temp = set()
                for lit in clause_set_temp:
                    var = abs(lit)
                    clause_variable_set_temp.add(var)

                    # The variable does not exist
                    if var not in self.__variable_set:
                        if len(self.__variable_set) >= self.__number_of_variables:
                            warning_temp = f"The number of variables in DIMACS CNF ({len(self.__variable_set) + 1}) differs from the v value ({self.__number_of_variables})!"
                            warnings.warn(warning_temp)

                        self.__variable_list.append(var)
                        self.__variable_set.add(var)
                        self.__literal_list.extend([-var, var])
                        self.__literal_set.update([-var, var])

                        self.__adjacency_literal_dictionary[var] = set()
                        self.__adjacency_literal_dictionary[-var] = set()
                        self.__adjacency_variable_dictionary[var] = set()

                    self.__adjacency_literal_dictionary[lit].add(clause_id)
                    self.__adjacency_variable_dictionary[var].add(clause_id)

                    # Incidence graph
                    self.__incidence_graph.add_edge(lit, clause_id)

                self.__clause_size_list[len(clause_set_temp)].add(clause_id)
                self.__cnf.append(clause_set_temp)
                self.__cnf_variable.append(clause_variable_set_temp)

                self.__real_number_of_clauses += 1
                clause_id += 1
        finally:
            io.close()

        # The file does not contain any clause
        if not len(self.__cnf):
            raise f_exception.InvalidDimacsCnfFormatException("the file does not contain any clause")

        self.__unit_clause_set = self.__clause_size_list[1].copy()  # get unit clauses
        self.__real_number_of_variables = len(self.__variable_set)

        self.__cnf_statistics.create.stop_stopwatch()   # timer (stop)

    def __get_clause_set_literal(self, literal: int) -> Set[int]:
        """
        Return a set of clause's id, where the literal appears.
        If the literal does not exist in the formula, an empty set is returned.
        :param literal: the literal
        :return: a set of clause's id, where the literal appears
        """

        # The literal does not appear in any clause
        if literal not in self.__adjacency_literal_dictionary:
            return set()

        return self.__adjacency_literal_dictionary[literal]

    def __get_clause_set_variable(self, variable: int) -> Set[int]:
        """
        Return a set of clause's id, where the variable appears.
        If the variable does not exist in the formula, an empty set is returned.
        :param variable: the variable
        :return: a set of clause's id, where the variable appears
        """

        # The variable does not appear in any clause
        if variable not in self.__adjacency_variable_dictionary:
            return set()

        return self.__adjacency_variable_dictionary[variable]
    # endregion

    # region Public method
    def get_variable_set(self, copy: bool) -> Set[int]:
        """
        :param copy: True if a copy is returned
        :return: a set of variables
        """

        if copy:
            return self.__variable_set.copy()

        return self.__variable_set

    def get_size_clause(self, clause_id: int) -> int:
        """
        Return the size of the clause with the given identifier
        :param clause_id: the identifier of the clause
        :return: the size of the clause
        :raises ClauseDoesNotExistException: if the clause does not exist
        """

        return len(self.get_clause(clause_id, copy=False))

    def get_clause(self, clause_id: int, copy: bool) -> Set[int]:
        """
        Return a clause with the given identifier
        :param clause_id: the identifier of the clause
        :param copy: True if a copy is returned
        :return: the clause (a set of literals)
        :raises ClauseDoesNotExistException: if the clause does not exist
        """

        # The clause doesn't exist
        if (clause_id < 0) or (clause_id >= self.__real_number_of_clauses):
            raise f_exception.ClauseDoesNotExistException(clause_id)

        if copy:
            return self.__cnf[clause_id].copy()

        return self.__cnf[clause_id]

    def get_variable_in_clause(self, clause_id: int, copy: bool) -> Set[int]:
        """
        Return a set of variables that appear in the clause
        :param clause_id: the identifier of the clause
        :param copy: True if a copy is returned
        :return: a set of variables
        :raises ClauseDoesNotExistException: if the clause does not exist
        """

        try:
            variable_set = self.__cnf_variable[clause_id]
        except IndexError:
            raise f_exception.ClauseDoesNotExistException(clause_id)

        if copy:
            return variable_set.copy()

        return variable_set

    def get_variable_in_clauses(self, clause_id_set: Set[int]) -> Set[int]:
        """
        Return a set of variables that appear in the clauses from the clause_id_set
        :param clause_id_set: the subset of clauses
        :return: a set of variables
        :raises ClauseDoesNotExistException: if any clause does not exist
        """

        variable_set = set()

        for clause_id in clause_id_set:
            variable_set.update(self.get_variable_in_clause(clause_id, copy=False))

        return variable_set

    def get_incidence_graph(self, copy: bool = False) -> IncidenceGraph:
        """
        Return the incidence graph
        :param copy: True if a copy is returned
        :return: the incidence graph
        """

        if copy:
            return self.__incidence_graph.copy_incidence_graph()

        return self.__incidence_graph

    def get_unit_clause_set(self, copy: bool) -> Set[int]:
        """
        Return the unit clause set
        :param copy: True if a copy is returned
        :return: the unit clause set
        """

        if copy:
            return self.__unit_clause_set.copy()

        return self.__unit_clause_set
    # endregion

    # region Magic method
    def __str__(self):
        string_temp = "\n".join((f"Number of clauses: {self.number_of_clauses}",
                                 f"Real number of clauses: {self.real_number_of_clauses}",
                                 f"Number of variables: {self.number_of_variables}",
                                 f"Real number of variables: {self.real_number_of_variables}",
                                 f"Unit clauses: {self.__unit_clause_set}",
                                 "\nComments: ", self.comments))

        return string_temp
    # endregion

    # region Properties
    @property
    def number_of_clauses(self) -> int:
        return self.__number_of_clauses

    @property
    def real_number_of_clauses(self) -> int:
        return self.__real_number_of_clauses

    @property
    def number_of_variables(self) -> int:
        return self.__number_of_variables

    @property
    def real_number_of_variables(self) -> int:
        return self.__real_number_of_variables

    @property
    def comments(self) -> str:
        return self.__comments

    @property
    def cnf_statistics(self) -> CnfStatistics:
        return self.__cnf_statistics

    @property
    def incidence_graph_statistics(self) -> IncidenceGraphStatistics:
        return self.get_incidence_graph().statistics
    # endregion
