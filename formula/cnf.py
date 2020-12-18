# Import


# Import exception
import exception.formula_exception as f_exception


class Cnf:
    """
    CNF formula representation
    """

    """
    private str comments
    private int number_of_clauses
    private int number_of_variables
    private int number_of_literals                      # 2 * number_of_variables
    private List<Set<int>> cnf
    private List<int> variable_list
    private Set<int> variable_set
    private List<int> literal_list
    private Set<int> literal_set

    private Dict<int, Set<int>> adjacency_dictionary    # key: literal, value: a set of clauses where the literal appears
    private Set<int> unit_clause_set                    # a set which contains all unit clauses
    private Set<int> unused_variable_set                # a set which contains all unused variables (variables which do not appear in any clause)
    private List<Set<int>> clause_size_list             # key: 1..|variables|, value: a set contains all clauses with size k
    """

    def __init__(self, dimacs_cnf_file_path: str):
        # Initialization
        # region
        self.__comments = ""
        self.__number_of_clauses = 0
        self.__number_of_variables = 0
        self.__number_of_literals = 0
        self.__cnf = []
        self.__variable_list = []
        self.__variable_set = set()
        self.__literal_list = []
        self.__literal_set = set()

        self.__adjacency_dictionary = {}
        self.__unit_clause_set = set()
        self.__unused_variable_set = set()
        self.__clause_size_list = []
        # endregion

        self.__create_cnf(dimacs_cnf_file_path)

    # Private methods
    # region
    def __create_cnf(self, dimacs_cnf_file_path: str):
        """
        Convert the formula from the file into our structure.
        :param dimacs_cnf_file_path: the file which is in the DIMACS CNF format
        """

        with open(dimacs_cnf_file_path, "r") as file:
            clause_id = 0

            for line_id, line in enumerate(file.readlines()):
                # Comment line
                if line.startswith("c"):
                    if not self.__comments:
                        self.__comments = "".join((self.__comments, line[1:].strip()))
                    else:
                        self.__comments = "\n".join((self.__comments, line[1:].strip()))
                    continue

                # End of file (optional)
                if line.startswith("%"):
                    break

                # P line
                if line.startswith("p"):
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
                        self.__adjacency_dictionary[lit] = set()

                    for v in range(self.__number_of_variables + 1):
                        self.__clause_size_list.append(set())   # initialization

                    continue

                # Clause line
                line_array_temp = line.split()
                # Invalid line
                if not line_array_temp or line_array_temp.pop() != "0":
                    raise f_exception.InvalidDimacsCnfFormatException(f"the clause ({line}) defined on line {line_id} doesn't end with 0")

                clause_set_temp = set()
                try:
                    for lit in line_array_temp:
                        lit = int(lit)
                        v = abs(lit)

                        # (lit v lit) in the clause
                        if lit in clause_set_temp:
                            continue

                        # (lit v -lit) in the clause
                        if -lit in clause_set_temp:
                            raise f_exception.InvalidDimacsCnfFormatException(f"the clause ({line}) defined on line {line_id} contains opposite literals")

                        clause_set_temp.add(lit)
                        self.__adjacency_dictionary[lit].add(clause_id)

                        # Remove the variable from the unused_variable_set
                        if v in self.__unused_variable_set:
                            self.__unused_variable_set.remove(v)
                except ValueError:
                    raise f_exception.InvalidDimacsCnfFormatException(f"invalid clause ({line}) defined on line {line_id}")

                # Check if the clause is unit
                self.__clause_size_list[len(clause_set_temp)].add(clause_id)

                self.__cnf.append(clause_set_temp)
                clause_id += 1

        self.__unit_clause_set = self.__clause_size_list[1].copy()  # get unit clauses

    def __get_clause(self, clause_id: int) -> set:
        """
        Return a clause with the given identifier. If the clause does not exist, raise an exception (ClauseDoesNotExistException).
        :param clause_id: the identifier of the clause
        :return: the clause
        """

        # The clause doesn't exist
        if clause_id >= self.__number_of_clauses:
            raise f_exception.ClauseDoesNotExistException(clause_id)

        return self.__cnf[clause_id]
    # endregion

    # Public methods
    # region
    def get_clause(self, clause_id: int) -> set:
        """
        Return a clause with the given identifier. If the clause does not exist, raise an exception (ClauseDoesNotExistException).
        Copy is used!
        :param clause_id: the identifier of the clause
        :return: the clause
        """

        return self.__get_clause(clause_id).copy()

    def __str__(self):
        string_temp = ""

        string_temp = "".join((string_temp, f"Number of clauses: {self.__number_of_clauses}"))
        string_temp = "\n".join((string_temp, f"Number of variables: {self.__number_of_variables}"))
        string_temp = "\n".join((string_temp, f"Unit clauses: {self.__unit_clause_set}"))
        string_temp = "\n".join((string_temp, f"Unused variables: {self.__unused_variable_set}"))
        string_temp = "\n".join((string_temp, "\nComments: ", self.__comments))

        return string_temp
    # endregion

    # Properties
    # region
    @property
    def number_of_clauses(self) -> int:
        return self.__number_of_clauses

    @property
    def number_of_variables(self) -> int:
        return self.__number_of_variables

    @property
    def unused_variable_set(self) -> set:
        """
        Copy is used!
        """

        return self.__unused_variable_set.copy()

    @property
    def unit_clause_set(self) -> set:
        """
        Copy is used!
        """

        return self.__unit_clause_set.copy()
    # endregion
