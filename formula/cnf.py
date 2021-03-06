# Import
from typing import Set, Dict, List, Union
from formula.incidence_graph import IncidenceGraph

# Import exception
import exception.formula.formula_exception as f_exception


class Cnf:
    """
    CNF formula representation
    """

    """
    Private str comments
    Private int number_of_clauses
    Private int real_number_of_clauses
    Private int number_of_variables
    Private int number_of_literals                      # 2 * number_of_variables
    Private List<Set<int>> cnf                          # key: 0, 1, .., |clauses|, value: a set of literals which appear in the clause
    Private List<Set<int>> cnf_variable                 # key: 0, 1, .., |clauses|, value: a set of variables which appear in the clause
    Private List<int> variable_list
    Private Set<int> variable_set
    Private List<int> literal_list
    Private Set<int> literal_set
    Private Dict<int, Set<int>> adjacency_literal_dictionary    # key: literal, value: a set of clauses where the literal appears
    Private Dict<int, Set<int>> adjacency_variable_dictionary   # key: variable, value: a set of clauses where the variable appears
    Private Set<int> unit_clause_set                    # a set which contains all unit clauses
    Private Set<int> unused_variable_set                # a set which contains all unused variables (variables which do not appear in any clause)
    Private List<Set<int>> clause_size_list             # key: 0, 1, .., |variables|, value: a set contains all clauses with the size k
    
    Private IncidenceGraph incidence_graph
    """

    def __init__(self, dimacs_cnf_file_path: str):
        # region Initialization
        self.__comments: str = ""
        self.__number_of_clauses: int = 0
        self.__real_number_of_clauses: int = 0
        self.__number_of_variables: int = 0
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
        self.__unused_variable_set: Set[int] = set()
        self.__clause_size_list: List[Set[int]] = []
        # endregion

        # Incidence graph
        self.__incidence_graph: Union[IncidenceGraph, None] = None

        self.__create_cnf(dimacs_cnf_file_path)

    # region Private method
    def __create_cnf(self, dimacs_cnf_file_path: str) -> None:
        """
        Convert the formula from the file into our structure
        :param dimacs_cnf_file_path: the file which is in the DIMACS CNF format
        :return: None
        """

        with open(dimacs_cnf_file_path, "r") as file:
            clause_id = 0
            is_p_line_defined = False

            for line_id, line in enumerate(file.readlines()):
                # The line is empty
                if not line.strip():
                    continue

                # Comment line
                if line.startswith("c"):
                    if not self.__comments:     # First comment
                        self.__comments = line[1:].strip()
                    else:
                        self.__comments = "\n".join((self.__comments, line[1:].strip()))
                    continue

                # End of file (optional)
                if line.startswith("%"):
                    break

                # P line
                if line.startswith("p"):
                    is_p_line_defined = True
                    line_array_temp = line.split()
                    # P line has an invalid format
                    if len(line_array_temp) != 4:   # p cnf number_of_variables number_of_clauses
                        raise f_exception.InvalidDimacsCnfFormatException("p line has an invalid format. Valid format is 'p cnf number_of_variables number_of_clauses'")

                    # Parse the parameters
                    try:
                        self.__number_of_variables = int(line_array_temp[2])
                        self.__number_of_clauses = int(line_array_temp[3])
                    except ValueError:
                        raise f_exception.InvalidDimacsCnfFormatException(f"the number of variables ({line_array_temp[2]}) or the number of clauses ({line_array_temp[3]}) is not an integer")

                    self.__number_of_literals = 2 * self.__number_of_variables
                    self.__variable_list = list(range(1, self.__number_of_variables + 1))
                    self.__variable_set = set(self.__variable_list)
                    self.__literal_list = list(self.__variable_list)
                    self.__literal_list.extend([-v for v in self.__variable_list])
                    self.__literal_set = set(self.__literal_list)
                    self.__unused_variable_set = self.__variable_set.copy()     # initialization

                    for lit in self.__literal_list:
                        self.__adjacency_literal_dictionary[lit] = set()
                    for var in self.__variable_list:
                        self.__adjacency_variable_dictionary[var] = set()

                    for _ in range(self.__number_of_variables + 1):
                        self.__clause_size_list.append(set())   # initialization

                    # Incidence graph
                    self.__incidence_graph = IncidenceGraph(self.__number_of_variables, self.__number_of_clauses)

                    continue

                # P line has not been mentioned
                if not is_p_line_defined:
                    raise f_exception.PLineIsNotMentionedException()

                # Clause line
                line_array_temp = line.split()
                # Invalid line
                if not line_array_temp or line_array_temp.pop() != "0":
                    raise f_exception.InvalidDimacsCnfFormatException(f"the clause ({line}) defined on line {line_id + 1} doesn't end with 0")

                clause_set_temp = set()
                try:
                    for lit in line_array_temp:
                        lit = int(lit)
                        v = abs(lit)

                        # Variable does not exist
                        if v not in self.__variable_list:
                            raise f_exception.VariableDoesNotExistException(v)

                        # (lit v lit) in the clause
                        if lit in clause_set_temp:
                            continue

                        # (lit v -lit) in the clause
                        if -lit in clause_set_temp:
                            clause_set_temp = set()
                            break

                        clause_set_temp.add(lit)
                except ValueError:
                    raise f_exception.InvalidDimacsCnfFormatException(f"invalid clause ({line}) defined on line {line_id + 1}")

                # The clause is empty or contains two opposite literals
                if not clause_set_temp:
                    continue

                clause_variable_set_temp = set()
                for lit in clause_set_temp:
                    self.__adjacency_literal_dictionary[lit].add(clause_id)

                    v = abs(lit)
                    clause_variable_set_temp.add(v)
                    self.__adjacency_variable_dictionary[v].add(clause_id)
                    # Remove the variable from the unused_variable_set
                    if v in self.__unused_variable_set:
                        self.__unused_variable_set.remove(v)

                    # Incidence graph
                    self.__incidence_graph.add_edge(lit, clause_id)

                self.__clause_size_list[len(clause_set_temp)].add(clause_id)
                self.__cnf.append(clause_set_temp)
                self.__cnf_variable.append(clause_variable_set_temp)
                self.__real_number_of_clauses += 1
                clause_id += 1

        # The file does not contain any clause
        if not len(self.__cnf):
            raise f_exception.InvalidDimacsCnfFormatException("file does not contain any clause")

        self.__unit_clause_set = self.__clause_size_list[1].copy()  # get unit clauses
    # endregion

    # region Protected method
    def _get_variable_set(self, copy: bool = False) -> Set[int]:
        """
        :return: a set of variables
        """

        if copy:
            return self.__variable_set.copy()

        return self.__variable_set

    def _get_clause_set_literal(self, literal: int) -> Set[int]:
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

    def _get_clause_set_variable(self, variable: int) -> Set[int]:
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

    def _get_clause(self, clause_id: int) -> Set[int]:
        """
        Return a clause with the given identifier.
        If the clause does not exist, raise an exception (ClauseDoesNotExistException).
        :param clause_id: the identifier of the clause
        :return: the clause (a set of literals)
        """

        # The clause doesn't exist
        if clause_id >= self.__real_number_of_clauses:
            raise f_exception.ClauseDoesNotExistException(clause_id)

        return self.__cnf[clause_id]

    def _get_variable_in_clause(self, clause_id: int, copy: bool = False) -> Set[int]:
        """
        Return a set of variables which appear in the clause.
        If the clause does not exist, raise an exception (ClauseDoesNotExistException).
        :param clause_id: the identifier of the clause
        :param copy: True if a copy is returned
        :return: a set of variables
        """

        try:
            variable_set = self.__cnf_variable[clause_id]
        except IndexError:
            raise f_exception.ClauseDoesNotExistException(clause_id)

        if copy:
            return variable_set.copy()

        return variable_set
    # endregion

    # region Public method
    def get_size_clause(self, clause_id: int) -> int:
        """
        Return the size of the clause with the given identifier.
        If the clause does not exist, raise an exception (ClauseDoesNotExistException).
        :param clause_id: the identifier of the clause
        :return: the size of the clause
        """

        return len(self._get_clause(clause_id))

    def get_clause(self, clause_id: int) -> Set[int]:
        """
        Return a clause with the given identifier.
        If the clause does not exist, raise an exception (ClauseDoesNotExistException).
        Copy is used!
        :param clause_id: the identifier of the clause
        :return: the clause (a set of literals)
        """

        return self._get_clause(clause_id).copy()

    def get_variable_in_clauses(self, clause_id_set: Set[int]) -> Set[int]:
        """
        Return a set of variables which appear in the clauses from the clause_id_set.
        If any clause does not exist, raise an exception (ClauseDoesNotExistException).
        :param clause_id_set: the subset of clauses
        :return: a set of variables
        """

        variable_set = set()

        for clause_id in clause_id_set:
            try:
                variable_set.update(self.__cnf_variable[clause_id])
            except IndexError:
                raise f_exception.ClauseDoesNotExistException(clause_id)

        return variable_set

    def get_incidence_graph(self, copy: bool = False) -> IncidenceGraph:
        """
        Return the incidence graph
        :param copy: True if a copy is returned
        :return: the incidence graph
        """

        if copy:
            return self.__incidence_graph.copy()

        return self.__incidence_graph
    # endregion

    # region Magic method
    def __str__(self):
        string_temp = "".join(f"Number of clauses: {self.__number_of_clauses}")
        string_temp = "\n".join((string_temp, f"Real number of clauses: {self.real_number_of_clauses}"))
        string_temp = "\n".join((string_temp, f"Number of variables: {self.number_of_variables}"))
        string_temp = "\n".join((string_temp, f"Unit clauses: {self.__unit_clause_set}"))
        string_temp = "\n".join((string_temp, f"Unused variables: {self.__unused_variable_set}"))
        string_temp = "\n".join((string_temp, "\nComments: ", self.__comments))

        return string_temp
    # endregion

    # region Properties
    @property
    def real_number_of_clauses(self) -> int:
        return self.__real_number_of_clauses

    @property
    def number_of_variables(self) -> int:
        return self.__number_of_variables

    @property
    def unused_variable_set(self) -> Set[int]:
        """
        Copy is used!
        """

        return self.__unused_variable_set.copy()

    @property
    def unit_clause_set(self) -> Set[int]:
        """
        Copy is used!
        """

        return self.__unit_clause_set.copy()

    @property
    def comments(self):
        return self.__comments
    # endregion
