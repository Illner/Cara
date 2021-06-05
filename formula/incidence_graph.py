# Import
import random
import networkx as nx
from networkx.classes.graph import Graph
from typing import Set, Dict, List, Union, TypeVar, Tuple
from formula.renamable_horn_formula_recognition import RenamableHornFormulaRecognition
from compiler_statistics.formula.incidence_graph_statistics import IncidenceGraphStatistics

from formula.pysat_cnf import PySatCnf
from formula.pysat_2_cnf import PySat2Cnf
from formula.pysat_horn_cnf import PySatHornCnf

# Import exception
import exception.cara_exception as c_exception
import exception.formula.incidence_graph_exception as ig_exception

# Import enum
import formula.enum.pysat_cnf_enum as psc_enum
import formula.enum.eliminating_redundant_clauses_enum as erc_enum

# Type
TIncidenceGraph = TypeVar("TIncidenceGraph", bound="IncidenceGraph")


class IncidenceGraph(Graph):
    """
    Incidence graph
    """

    """
    Protected Set<int> variable_set
    Protected Set<int> clause_id_set
    Private Set<int> satisfied_clause_set
    Private Dict<int, Set<int>> clause_dictionary                           # key: a clause, value: a set of literals that appear in the clause
    Private Dict<int, List<int>> sorted_clause_cache                        # key: a clause, value: a sorted list of literals that appear in the clause
    Private Dict<int, Set<int>> adjacency_literal_static_dictionary         # key: a literal, value: a set of clauses (nodes) where the literal appears
    Private Dict<int, Set<int>> adjacency_literal_dynamic_dictionary        # key: a literal, value: a set of clauses (nodes) where the literal appears
    Private bool update_adjacency_literal_dynamic_dictionary
    
    Private Dict<str, int> unhash_dictionary
    Private Dict<int, str> variable_hash_dictionary
    Private Dict<int, str> clause_id_hash_dictionary
    
    Private IncidenceGraphStatistics statistics
    
    # Clause length
    Private Dict<int, int> clause_length_dictionary                         # key: a clause, value: the length of the clause
    Private Dict<int, Set<int>> length_set_clauses_dictionary               # key: a length, value: a set of clauses with that length
    
    # Renamable Horn formula recognition
    Private Set<int> neg_assigned_literal_set
    Private Set<int> ignored_literal_set_renamable_horn_formula_recognition
    Private RenamableHornFormulaRecognition renamable_horn_formula_recognition
    
    # Assignment
    Private Set<int> assigned_variable_set
    Private List<int> assigned_literal_list
    Private Dict<int, Set<str>> variable_node_backup_dictionary                             # key: a variable, value: a set of clauses (nodes) that were incident with the variable node when the variable node was being deleted
    Private Dict<int, Dict<int, Set<int>> clause_node_backup_dictionary                     # key: a variable, value: a dictionary, where a key is a clause node that was satisfied because of the variable, and the value is a set of variables (nodes) that were incident with the clause node when the clause node was being deleted
    Private Dict<int, Dict<int, Set<int>> eliminated_redundant_clauses_backup_dictionary    # key: a variable, value: a dictionary, where a key is a clause node that was eliminated, and the value is a set of variables (nodes) that were incident with the clause node when the clause node was being deleted
    
    # Variable simplification
    Private Dict<int, Set<str>> removed_edge_backup_dictionary              # key: a variable, value: a set of neighbours of the variable that were deleted because of variable simplification
    Private Dict<str, Set<str>> added_edge_backup_dictionary                # key: a variable, value: a set of neighbours of the variable that were added because of variable simplification
    
    # Subsumption - variable
    Private Dict<int, Set<str>> subsumption_variable_backup_dictionary      # key: a clause, value: a set of variables (nodes) that were incident with the clause node when the clause node was being deleted
    """

    def __init__(self, statistics: Union[IncidenceGraphStatistics, None] = None,
                 renamable_horn_formula_recognition: Union[RenamableHornFormulaRecognition, None] = None,
                 ignored_literal_set_renamable_horn_formula_recognition: Union[Set[int], None] = None):
        super().__init__()

        self._variable_set: Set[int] = set()
        self._clause_id_set: Set[int] = set()
        self.__satisfied_clause_set: Set[int] = set()
        self.__clause_dictionary: Dict[int, Set[int]] = dict()
        self.__sorted_clause_cache: Dict[int, List[int]] = dict()
        self.__adjacency_literal_static_dictionary: Dict[int, Set[int]] = dict()
        self.__adjacency_literal_dynamic_dictionary: Dict[int, Set[int]] = dict()
        self.__update_adjacency_literal_dynamic_dictionary: bool = True             # because of variable simplification

        self.__unhash_dictionary: Dict[str, int] = dict()
        self.__variable_hash_dictionary: Dict[int, str] = dict()
        self.__clause_id_hash_dictionary: Dict[int, str] = dict()

        # Clause length
        self.__clause_length_dictionary: Dict[int, int] = dict()
        self.__length_set_clauses_dictionary: Dict[int, Set[int]] = {0: set(), 1: set(), 2: set()}

        # Renamable Horn formula recognition
        self.__neg_assigned_literal_set: Set[int] = set()
        self.__ignored_literal_set_renamable_horn_formula_recognition: Set[int] = set()
        if ignored_literal_set_renamable_horn_formula_recognition is not None:
            self.__ignored_literal_set_renamable_horn_formula_recognition = ignored_literal_set_renamable_horn_formula_recognition
        self.__renamable_horn_formula_recognition: Union[RenamableHornFormulaRecognition, None] = renamable_horn_formula_recognition

        # Statistics
        if statistics is None:
            self.__statistics: IncidenceGraphStatistics = IncidenceGraphStatistics(active=False)
        else:
            self.__statistics: IncidenceGraphStatistics = statistics

        # Backup - assignment
        self.__assigned_variable_set: Set[int] = set()
        self.__assigned_literal_list: List[int] = []
        self.__variable_node_backup_dictionary: Dict[int, Set[str]] = dict()
        self.__clause_node_backup_dictionary: Dict[int, Dict[int, Set[int]]] = dict()
        self.__eliminated_redundant_clauses_backup_dictionary: Dict[int, Dict[int, Set[int]]] = dict()

        # Backup - variable simplification
        self.__removed_edge_backup_dictionary: Dict[int, Set[str]] = dict()
        self.__added_edge_backup_dictionary: Dict[str, Set[str]] = dict()

        # Backup - subsumption - variable
        self.__subsumption_variable_backup_dictionary: Dict[int, Set[str]] = dict()

    # region Private method
    def __variable_hash(self, variable: int) -> str:
        """
        :param variable: the variable
        :return: a hash key for the variable
        """

        if variable in self.__variable_hash_dictionary:
            return self.__variable_hash_dictionary[variable]

        result = f"v{variable}"
        self.__variable_hash_dictionary[variable] = result

        return result

    def __clause_id_hash(self, clause_id: int) -> str:
        """
        :param clause_id: the identifier of the clause
        :return: a hash key for the clause's id
        """

        if clause_id in self.__clause_id_hash_dictionary:
            return self.__clause_id_hash_dictionary[clause_id]

        result = f"c{clause_id}"
        self.__clause_id_hash_dictionary[clause_id] = result

        return result

    def __unhash(self, id_hash: str) -> int:
        """
        Unhash the hash
        :param id_hash: the hash
        :return: the identifier (of variable or clause)
        :raises SomethingWrongException: if the hash is invalid
        """

        if id_hash in self.__unhash_dictionary:
            return self.__unhash_dictionary[id_hash]

        try:
            id = int(id_hash[1:])
        except ValueError:
            raise c_exception.SomethingWrongException(f"invalid hash ({id_hash})")

        self.__unhash_dictionary[id_hash] = id
        return id

    def __update_clause_length(self, clause_id: int, increment_by_one: bool) -> None:
        """
        Increment or decrement the length of the clause by one
        :param clause_id: the identifier of the clause
        :param increment_by_one: True for incrementing the length by one, False for decrementing the length by one
        :return: None
        :raises SomethingWrongException: if the length of the clause will be negative
        """

        value_before = self.__clause_length_dictionary[clause_id]

        # Increment
        if increment_by_one:
            self.__clause_length_dictionary[clause_id] += 1
        # Decrement
        else:
            self.__clause_length_dictionary[clause_id] -= 1

        value_after = self.__clause_length_dictionary[clause_id]
        if value_after < 0:
            raise c_exception.SomethingWrongException(f"the length of the clause ({clause_id}) is negative ({value_after})")

        self.__length_set_clauses_dictionary[value_before].remove(clause_id)
        if value_after not in self.__length_set_clauses_dictionary:
            self.__length_set_clauses_dictionary[value_after] = set()
        self.__length_set_clauses_dictionary[value_after].add(clause_id)

    def __node_exist(self, node_hash: str) -> bool:
        """
        :param node_hash: the hash representing a node
        :return: True if the node exists in the incidence graph. Otherwise, False is returned.
        """

        if node_hash in self:
            return True

        return False

    def __variable_exist(self, variable: int) -> bool:
        """
        :param variable: a variable
        :return: True if the variable exists in the incidence graph. Otherwise, False is returned.
        """

        if variable in self._variable_set:
            return True

        return False

    def __clause_id_exist(self, clause_id: int) -> bool:
        """
        :param clause_id: the identifier of the clause
        :return: True if the clause exists in the incidence graph. Otherwise, False is returned.
        """

        if clause_id in self._clause_id_set:
            return True

        return False

    def __is_node_variable(self, node_hash: str) -> Union[bool, None]:
        """
        :param node_hash: the hash representing a node
        :return: True if the node is a variable, otherwise False is returned.
        If the node does not exist in the incidence graph, None is returned.
        """

        # The node does not exist in the incidence graph
        if node_hash not in self:
            return None

        return self.nodes[node_hash]["bipartite"] == 0

    def __temporarily_remove_variable(self, variable: int, neighbour_set: Union[Set[int], Set[str], None] = None) -> None:
        """
        Temporarily remove the variable
        :param variable: the variable
        :param neighbour_set: the neighbour set of the variable (optional)
        :return: None
        :raises VariableDoesNotExistException: if the variable does not exist in the incidence graph
        """

        variable_hash = self.__variable_hash(variable)

        # Check if the variable exists in the incidence graph
        if variable_hash not in self:
            raise ig_exception.VariableDoesNotExistException(variable)

        neighbour_set = set(self.neighbors(variable_hash)) if neighbour_set is None else neighbour_set

        # Remove edges
        for neighbour in neighbour_set:
            clause_id = neighbour if isinstance(neighbour, int) else self.__unhash(neighbour)

            # adjacency_literal_dynamic_dictionary
            if self.__update_adjacency_literal_dynamic_dictionary:
                literal = self.__get_literal_from_clause(variable, clause_id)

                self.__adjacency_literal_dynamic_dictionary[literal].remove(clause_id)
                self.__clause_dictionary[clause_id].remove(literal)

                if clause_id in self.__sorted_clause_cache:
                    del self.__sorted_clause_cache[clause_id]

            self.__update_clause_length(clause_id, increment_by_one=False)  # update the length

        self._variable_set.remove(variable)
        self.remove_node(variable_hash)

    def __temporarily_remove_clause_id(self, clause_id: int, neighbour_set: Union[Set[int], Set[str], None] = None) -> None:
        """
        Temporarily remove the clause
        :param clause_id: the identifier of the clause
        :param neighbour_set: the neighbour set of the clause (optional)
        :return: None
        :raises ClauseIdDoesNotExistException: if the clause does not exist in the incidence graph
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # Check if the clause exists in the incidence graph
        if clause_id_hash not in self:
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        neighbour_set = set(self.neighbors(clause_id_hash)) if neighbour_set is None else neighbour_set

        # adjacency_literal_dynamic_dictionary
        if self.__update_adjacency_literal_dynamic_dictionary:
            for neighbour in neighbour_set:
                variable = neighbour if isinstance(neighbour, int) else self.__unhash(neighbour)

                literal = self.__get_literal_from_clause(variable, clause_id)

                self.__adjacency_literal_dynamic_dictionary[literal].remove(clause_id)
                self.__clause_dictionary[clause_id].remove(literal)

            if clause_id in self.__sorted_clause_cache:
                del self.__sorted_clause_cache[clause_id]

        # Clause length
        clause_len = self.__clause_length_dictionary[clause_id]
        del self.__clause_length_dictionary[clause_id]
        self.__length_set_clauses_dictionary[clause_len].remove(clause_id)

        self._clause_id_set.remove(clause_id)
        self.remove_node(clause_id_hash)

    def __temporarily_remove_edge(self, variable: Union[int, str], clause_id: Union[int, str]) -> None:
        """
        Temporarily remove the edge (variable - clause_id)
        :param variable: the identifier/hash of the variable
        :param clause_id: the identifier/hash of the clause
        :return: None
        :raises VariableDoesNotExistException: if the variable does not exist in the incidence graph
        :raises ClauseIdDoesNotExistException: if the clause does not exist in the incidence graph
        :raises TryingRemoveEdgeDoesNotExistException: if the edge does not exist in the incidence graph
        """

        # Variable
        # Hash
        if isinstance(variable, str):
            variable_hash = variable
            variable = self.__unhash(variable_hash)
        # ID
        else:
            variable_hash = self.__variable_hash(variable)

        # Clause
        # Hash
        if isinstance(clause_id, str):
            clause_id_hash = clause_id
            clause_id = self.__unhash(clause_id_hash)
        # ID
        else:
            clause_id_hash = self.__clause_id_hash(clause_id)

        # The variable does not exist in the incidence graph
        if variable_hash not in self:
            raise ig_exception.VariableDoesNotExistException(variable)

        # The clause does not exist in the incidence graph
        if clause_id_hash not in self:
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        # The edge does not exist in the incidence graph
        if not self.has_edge(variable_hash, clause_id_hash):
            raise ig_exception.TryingRemoveEdgeDoesNotExistException(variable, clause_id)

        # adjacency_literal_dynamic_dictionary
        if self.__update_adjacency_literal_dynamic_dictionary:
            literal = self.__get_literal_from_clause(variable, clause_id)

            self.__adjacency_literal_dynamic_dictionary[literal].remove(clause_id)
            self.__clause_dictionary[clause_id].remove(literal)

            if clause_id in self.__sorted_clause_cache:
                del self.__sorted_clause_cache[clause_id]

        self.__update_clause_length(clause_id, increment_by_one=False)  # update the length
        super().remove_edge(variable_hash, clause_id_hash)

    def __add_edge(self, variable_hash: str, clause_id_hash: str) -> None:
        """
        Add an edge to the incidence graph
        :param variable_hash: the hash of the variable
        :param clause_id_hash: the hash of the clause
        :return: None
        """

        clause_id = self.__unhash(clause_id_hash)

        # adjacency_literal_dynamic_dictionary
        if self.__update_adjacency_literal_dynamic_dictionary:
            variable = self.__unhash(variable_hash)
            literal = self.__get_literal_from_clause(variable, clause_id)

            self.__adjacency_literal_dynamic_dictionary[literal].add(clause_id)
            self.__clause_dictionary[clause_id].add(literal)

            if clause_id in self.__sorted_clause_cache:
                del self.__sorted_clause_cache[clause_id]

        self.__update_clause_length(clause_id, increment_by_one=True)   # update the length
        super().add_edge(variable_hash, clause_id_hash)

    def __convert_to_cnf(self, pysat_cnf_enum: psc_enum.PySatCnfEnum, renaming_function: Union[Set[int], None] = None) -> Union[PySatCnf, PySat2Cnf, PySatHornCnf]:
        """
        Convert the formula represented by the incidence graph to CNF / 2-CNF / HornCNF
        :param pysat_cnf_enum: a type of CNF (standard, 2-CNF, HornCNF)
        :param renaming_function: a set of variables that will be renamed (for HornCNF)
        :return: PySAT (CNF / 2-CNF / HornCNF)
        """

        # CNF
        if pysat_cnf_enum == psc_enum.PySatCnfEnum.CNF:
            cnf: PySatCnf = PySatCnf()
        # 2-CNF
        elif pysat_cnf_enum == psc_enum.PySatCnfEnum.TWO_CNF:
            cnf: PySat2Cnf = PySat2Cnf()
        # HornCNF
        elif pysat_cnf_enum == psc_enum.PySatCnfEnum.HORN_CNF:
            cnf: PySatHornCnf = PySatHornCnf()
        # Not supported
        else:
            raise c_exception.FunctionNotImplementedException("convert_to_cnf",
                                                              f"this type of CNF ({pysat_cnf_enum.name}) is not implemented")

        for clause_id in self.clause_id_set(copy=False, multi_occurrence=False):
            # No renaming function
            if renaming_function is None:
                cnf.append(self.__clause_dictionary[clause_id])

            # Renaming function exists
            else:
                clause_temp = []

                for lit in self.__clause_dictionary[clause_id]:
                    if abs(lit) in renaming_function:
                        clause_temp.append(-lit)
                    else:
                        clause_temp.append(lit)

                cnf.append(clause_temp)

        return cnf

    def __get_literal_from_clause(self, variable: int, clause_id: int) -> int:
        """
        Return a sign of variable which occurs in the clause
        :param variable: the variable
        :param clause_id: the identifier of the clause
        :return: a literal which appears in the clause
        :raises VariableDoesNotExistInClauseException: if the variable does not exist in the clause
        """

        # Positive literal
        if clause_id in self.__adjacency_literal_static_dictionary[variable]:
            return variable

        # Negative literal
        if clause_id in self.__adjacency_literal_static_dictionary[(-variable)]:
            return -variable

        # The variable does not exist in the clause
        raise ig_exception.VariableDoesNotExistInClauseException(variable, clause_id)

    # region Eliminating redundant clauses
    def __get_redundant_clauses_subsumption(self) -> Set[int]:
        subsumed_clause_set = set()
        clause_id_list = self.clause_id_list()

        for i, clause_a_id in enumerate(clause_id_list):
            clause_a = self.__clause_dictionary[clause_a_id]

            for j in range(i + 1, len(clause_id_list)):
                clause_b_id = clause_id_list[j]

                if clause_b_id in subsumed_clause_set:
                    continue

                clause_b = self.__clause_dictionary[clause_b_id]

                a_subset_b = clause_a.issubset(clause_b)
                b_subset_a = clause_b.issubset(clause_a)

                # Clauses are the same
                if a_subset_b and b_subset_a:
                    if clause_a_id < clause_b_id:
                        subsumed_clause_set.add(clause_a_id)
                    else:
                        subsumed_clause_set.add(clause_b_id)

                    continue

                # Clause A is subsumed
                if a_subset_b:
                    subsumed_clause_set.add(clause_b_id)

                    continue

                # Clause B is subsumed
                if b_subset_a:
                    subsumed_clause_set.add(clause_a_id)

                    continue

        return subsumed_clause_set

    def __get_redundant_clauses_up_redundancy(self) -> Set[int]:
        return set()    # TODO
        # raise NotImplementedError()
    # endregion
    # endregion

    # region Public method
    def add_variable(self, variable: int) -> None:
        """
        Add a new variable to the incidence graph
        :param variable: the variable
        :return: None
        :raises VariableAlreadyExistsException: if the variable already exists in the incidence graph
        """

        variable_hash = self.__variable_hash(variable)

        # The variable already exists in the incidence graph
        if variable_hash in self:
            raise ig_exception.VariableAlreadyExistsException(variable)

        # adjacency_literal_dictionary
        if variable not in self.__adjacency_literal_static_dictionary:
            self.__adjacency_literal_static_dictionary[variable] = set()
            self.__adjacency_literal_static_dictionary[-variable] = set()
            self.__adjacency_literal_dynamic_dictionary[variable] = set()
            self.__adjacency_literal_dynamic_dictionary[-variable] = set()

        self._variable_set.add(variable)
        self.add_node(variable_hash, value=variable, bipartite=0)

    def add_clause_id(self, clause_id: int) -> None:
        """
        Add a new clause to the incidence graph
        :param clause_id: the identifier of the clause
        :return: None
        :raises ClauseIdAlreadyExistsException: if the clause already exists in the incidence graph
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # The clause already exists in the incidence graph
        if clause_id_hash in self:
            raise ig_exception.ClauseIdAlreadyExistsException(clause_id)

        # Clause length
        self.__clause_length_dictionary[clause_id] = 0
        self.__length_set_clauses_dictionary[0].add(clause_id)

        if self.__update_adjacency_literal_dynamic_dictionary:
            self.__clause_dictionary[clause_id] = set()

        self._clause_id_set.add(clause_id)
        self.add_node(clause_id_hash, value=clause_id, bipartite=1)

    def add_edge(self, literal: int, clause_id: int) -> None:
        """
        Add a new edge to the incidence graph (|literal| - clause_id).
        If the edge already exists in the incidence graph, nothing happens.
        :param literal: the literal
        :param clause_id: the identifier of the clause
        :return: None
        :raises VariableDoesNotExistException: if the variable (|literal|) does not exist in the incidence graph
        :raises ClauseIdDoesNotExistException: if the clause does not exist in the incidence graph
        """

        variable = abs(literal)
        variable_hash = self.__variable_hash(variable)
        clause_id_hash = self.__clause_id_hash(clause_id)

        # The variable does not exist in the incidence graph
        if variable_hash not in self:
            self.add_variable(variable)

        # The clause does not exist in the incidence graph
        if clause_id_hash not in self:
            self.add_clause_id(clause_id)

        # The edge already exists in the incidence graph
        if self.has_edge(variable_hash, clause_id_hash):
            return

        # adjacency_literal_static_dictionary
        self.__adjacency_literal_static_dictionary[literal].add(clause_id)

        self.__add_edge(variable_hash, clause_id_hash)

    def add_clause(self, clause_id: int, clause_set: Set[int]) -> None:
        """
        Add a new clause to the incidence graph
        :param clause_id: the identifier of the clause
        :param clause_set: the clause
        :return: None
        :raises ClauseIdAlreadyExistsException: if the clause already exists in the incidence graph
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # The clause already exists in the incidence graph
        if clause_id_hash in self:
            raise ig_exception.ClauseIdAlreadyExistsException(clause_id)

        self.add_clause_id(clause_id)

        for literal in clause_set:
            variable = abs(literal)
            variable_hash = self.__variable_hash(variable)

            # The variable does not exist in the incidence graph
            if variable_hash not in self:
                self.add_variable(variable)

            # adjacency_literal_static_dictionary
            self.__adjacency_literal_static_dictionary[literal].add(clause_id)

            # adjacency_literal_dynamic_dictionary
            if self.__update_adjacency_literal_dynamic_dictionary:
                self.__adjacency_literal_dynamic_dictionary[literal].add(clause_id)
                self.__clause_dictionary[clause_id].add(literal)

            super().add_edge(variable_hash, clause_id_hash)

        clause_len = len(clause_set)

        self.__clause_length_dictionary[clause_id] = clause_len

        if clause_len not in self.__length_set_clauses_dictionary:
            self.__length_set_clauses_dictionary[clause_len] = set()
        self.__length_set_clauses_dictionary[clause_len].add(clause_id)

    def is_connected(self) -> bool:
        """
        :return: True if the incidence graph is connected. Otherwise, False is returned.
        """

        self.__statistics.is_connected.start_stopwatch()    # timer (start)

        is_connected = nx.is_connected(self)

        self.__statistics.is_connected.stop_stopwatch()     # timer (stop)
        return is_connected

    def number_of_components(self) -> int:
        """
        :return: the number of connected components
        """

        self.__statistics.number_of_components.start_stopwatch()    # timer (start)

        number_of_components = nx.number_connected_components(self)

        self.__statistics.number_of_components.stop_stopwatch()     # timer (stop)
        return number_of_components

    def variable_neighbour_set(self, variable: int) -> Set[int]:
        """
        Return a set of clauses (nodes) that are incident with the variable node
        :param variable: the variable
        :return: a set of neighbours (clauses) of the variable
        :raises VariableDoesNotExistException: if the variable does not exist in the incidence graph
        """

        variable_hash = self.__variable_hash(variable)

        # The variable does not exist in the incidence graph
        if variable_hash not in self:
            raise ig_exception.VariableDoesNotExistException(variable)

        return set(self.nodes[n]["value"] for n in self.neighbors(variable_hash))

    def number_of_neighbours_variable(self, variable: int) -> int:
        """
        Return the number of neighbours (clauses) of the variable
        :param variable: the variable
        :return: the number of neighbours
        :raises VariableDoesNotExistException: if the variable does not exist in the incidence graph
        """

        variable_hash = self.__variable_hash(variable)

        # The variable does not exist in the incidence graph
        if variable_hash not in self:
            raise ig_exception.VariableDoesNotExistException(variable)

        return len(self[variable_hash])

    def clause_id_neighbour_set(self, clause_id: int) -> Set[int]:
        """
        Return a set of variables (nodes) that are incident with the clause node
        :param clause_id: the identifier of the clause
        :return: a set of neighbours (variables) of the clause
        :raises ClauseIdDoesNotExistException: if the clause does not exist in the incidence graph
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # The clause does not exist in the incidence graph
        if clause_id_hash not in self:
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        return set(self.nodes[n]["value"] for n in self.neighbors(clause_id_hash))

    def number_of_neighbours_clause_id(self, clause_id: int) -> int:
        """
        Return the number of neighbours (variables) of the clause
        :param clause_id: the identifier of the clause
        :return: the number of neighbours
        :raises ClauseIdDoesNotExistException: if the clause does not exist in the incidence graph
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # The clause does not exist in the incidence graph
        if clause_id_hash not in self:
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        return len(self[clause_id_hash])

    def get_clause(self, clause_id: int, copy: bool) -> Set[int]:
        """
        Return a clause with the given identifier
        :param clause_id: the clause's id
        :param copy: True if a copy is returned
        :return: the clause (a set of literals)
        :raises ClauseIdDoesNotExistException: if the clause does not exist in the incidence graph
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # The clause does not exist in the incidence graph
        if clause_id_hash not in self:
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        clause = self.__clause_dictionary[clause_id]

        return clause.copy() if copy else clause

    def get_sorted_clause(self, clause_id: int, copy: bool) -> List[int]:
        """
        Return a sorted clause with the given identifier
        :param clause_id: the clause's id
        :param copy: True if a copy is returned
        :return: the sorted clause (a list of literals)
        :raises ClauseIdDoesNotExistException: if the clause does not exist in the incidence graph
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # The clause does not exist in the incidence graph
        if clause_id_hash not in self:
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        # Cache
        if clause_id in self.__sorted_clause_cache:
            return self.__sorted_clause_cache[clause_id].copy() if copy else self.__sorted_clause_cache[clause_id]

        clause_sorted_list = sorted(self.__clause_dictionary[clause_id])
        self.__sorted_clause_cache[clause_id] = clause_sorted_list

        return clause_sorted_list.copy() if copy else clause_sorted_list

    def number_of_nodes(self) -> int:
        """
        :return: the number of nodes
        """

        return super().number_of_nodes()

    def clause_id_set(self, copy: bool, multi_occurrence: bool = True, multi_occurrence_literal: bool = True) -> Set[int]:
        """
        :param copy: True if a copy is returned
        :param multi_occurrence: should be multi-occurrent clauses kept (a copy is returned)
        :param multi_occurrence_literal: True if multi-occurrence is with respect to the literals. False for variables.
        :return: a set of clauses that are in the incidence graph
        """

        if multi_occurrence:
            return self._clause_id_set.copy() if copy else self._clause_id_set

        # Multi-occurrent clauses are not kept
        cache: Dict[str, int] = dict()
        clause_id_set_without_multi_occurrence = set()

        for clause_id in self._clause_id_set:
            if multi_occurrence_literal:
                clause_sorted_list = self.get_sorted_clause(clause_id, copy=False)
            else:
                clause_sorted_list = sorted(self.clause_id_neighbour_set(clause_id))

            clause_key_string = ",".join([str(lit) for lit in clause_sorted_list])

            if clause_key_string not in cache:
                cache[clause_key_string] = clause_id
                clause_id_set_without_multi_occurrence.add(clause_id)
            else:
                value = cache[clause_key_string]

                # determinism
                if value < clause_id:
                    continue

                clause_id_set_without_multi_occurrence.remove(value)
                clause_id_set_without_multi_occurrence.add(clause_id)
                cache[clause_key_string] = clause_id

        return clause_id_set_without_multi_occurrence

    def clause_id_list(self, multi_occurrence: bool = True) -> List[int]:
        """
        :param multi_occurrence: should be multi-occurrent clauses kept (a copy is returned)
        :return: a list of clauses that are in the incidence graph
        """

        return list(self.clause_id_set(copy=False, multi_occurrence=multi_occurrence))

    def number_of_clauses(self) -> int:
        """
        :return: the number of clauses in the incidence graph
        """

        return len(self._clause_id_set)

    def variable_set(self, copy: bool) -> Set[int]:
        """
        :param copy: True if a copy is returned
        :return: a set of variables that are in the incidence graph
        """

        variable_set = self._variable_set.copy() if copy else self._variable_set

        return variable_set

    def variable_list(self) -> List[int]:
        """
        :return: a list of variables that are in the incidence graph
        """

        return list(self._variable_set)

    def number_of_variables(self) -> int:
        """
        :return: the number of variables in the incidence graph
        """

        return len(self._variable_set)

    def get_redundant_clauses(self, eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum) -> Set[int]:
        """
        Get redundant clauses
        :param eliminating_redundant_clauses_enum: a procedure that will be applied for determining redundant clauses
        :return: a set of redundant clauses
        """

        self.__statistics.get_redundant_clauses.start_stopwatch()   # timer (start)

        redundant_clause_set: Union[Set[int], None] = None

        # NONE
        if eliminating_redundant_clauses_enum == erc_enum.EliminatingRedundantClausesEnum.NONE:
            redundant_clause_set = set()

        # SUBSUMPTION
        elif eliminating_redundant_clauses_enum == erc_enum.EliminatingRedundantClausesEnum.SUBSUMPTION:
            redundant_clause_set = self.__get_redundant_clauses_subsumption()

        # UP_REDUNDANCY
        # elif eliminating_redundant_clauses_enum == erc_enum.EliminatingRedundantClausesEnum.UP_REDUNDANCY:
        #     redundant_clause_set = self.__get_redundant_clauses_up_redundancy()

        if redundant_clause_set is not None:
            self.__statistics.get_redundant_clauses_size.add_count(len(redundant_clause_set))   # counter
            self.__statistics.get_redundant_clauses.stop_stopwatch()    # timer (stop)

            return redundant_clause_set

        raise c_exception.FunctionNotImplementedException("get_redundant_clauses",
                                                          f"this procedure for determining redundant clauses ({eliminating_redundant_clauses_enum.name}) is not implemented")

    # region Assignment
    def remove_literal(self, literal: int, eliminating_redundant_clauses_enum: Union[erc_enum.EliminatingRedundantClausesEnum, None]) -> Set[int]:
        """
        Remove the variable node (|literal|).
        Remove all (satisfied) clauses (nodes) that contain the literal.
        Everything removed from the incidence graph is saved and can be restored from the backup in future.
        :param literal: the literal
        :param eliminating_redundant_clauses_enum: a procedure that will be applied for determining redundant clauses
        :return: a set of isolated variables that have been deleted
        :raises VariableDoesNotExistException: if the variable does not exist in the incidence graph
        :raises VariableHasBeenRemovedException: if the variable has been already removed
        """

        variable = abs(literal)
        variable_hash = self.__variable_hash(variable)

        # The variable has been already removed from the incidence graph
        if variable in self.__assigned_variable_set:
            raise ig_exception.VariableHasBeenRemovedException(variable)

        # The variable does not exist in the incidence graph
        if variable_hash not in self:
            raise ig_exception.VariableDoesNotExistException(variable)

        isolated_variable_set = set()

        # Backup
        self.__assigned_variable_set.add(variable)
        self.__neg_assigned_literal_set.add(-literal)
        self.__assigned_literal_list.append(literal)

        variable_node_neighbour_set = set(self.neighbors(variable_hash))
        self.__variable_node_backup_dictionary[variable] = variable_node_neighbour_set

        # Delete the variable node
        self.__temporarily_remove_variable(variable=variable,
                                           neighbour_set=variable_node_neighbour_set)

        clause_node_dictionary = dict()
        for clause_id in self.__adjacency_literal_static_dictionary[literal]:
            clause_id_hash = self.__clause_id_hash(clause_id)

            # The clause node has been already deleted
            if clause_id_hash not in self:
                continue

            clause_node_neighbour_set = self.clause_id_neighbour_set(clause_id)
            clause_node_dictionary[clause_id] = clause_node_neighbour_set

            # Delete the (satisfied) clause
            self.__satisfied_clause_set.add(clause_id)
            self.__temporarily_remove_clause_id(clause_id=clause_id,
                                                neighbour_set=clause_node_neighbour_set)

            # Check if any neighbour is not an isolated node
            for clause_node_neighbour in clause_node_neighbour_set:
                if not self.number_of_neighbours_variable(clause_node_neighbour):
                    self.__temporarily_remove_variable(variable=clause_node_neighbour,
                                                       neighbour_set=set())
                    isolated_variable_set.add(clause_node_neighbour)

        self.__clause_node_backup_dictionary[variable] = clause_node_dictionary

        # Eliminating redundant clauses
        if eliminating_redundant_clauses_enum is not None:
            eliminated_redundant_clause_set = self.get_redundant_clauses(eliminating_redundant_clauses_enum)
        else:
            eliminated_redundant_clause_set = set()
        eliminated_clause_node_dictionary = dict()

        for clause_id in eliminated_redundant_clause_set:
            clause_id_hash = self.__clause_id_hash(clause_id)

            # The clause does not exist in the incidence graph
            if clause_id_hash not in self:
                raise ig_exception.ClauseHasBeenRemovedException(clause_id)

            clause_node_neighbour_set = self.clause_id_neighbour_set(clause_id)
            eliminated_clause_node_dictionary[clause_id] = clause_node_neighbour_set

            # Delete the redundant clause
            self.__satisfied_clause_set.add(clause_id)
            self.__temporarily_remove_clause_id(clause_id=clause_id,
                                                neighbour_set=clause_node_neighbour_set)

            # Check if any neighbour is not an isolated node
            for clause_node_neighbour in clause_node_neighbour_set:
                if not self.number_of_neighbours_variable(clause_node_neighbour):
                    self.__temporarily_remove_variable(variable=clause_node_neighbour,
                                                       neighbour_set=set())
                    isolated_variable_set.add(clause_node_neighbour)

        self.__eliminated_redundant_clauses_backup_dictionary[variable] = eliminated_clause_node_dictionary

        return isolated_variable_set

    def remove_literal_list(self, literal_list: List[int], eliminating_redundant_clauses_enum: Union[erc_enum.EliminatingRedundantClausesEnum, None]) -> Set[int]:
        isolated_variable_set = set()

        for i, literal in enumerate(literal_list):
            if abs(literal) in isolated_variable_set:
                continue

            erc_enum_temp = None if i < len(literal_list) - 1 else eliminating_redundant_clauses_enum
            isolated_variable_set.update(self.remove_literal(literal, erc_enum_temp))

        return isolated_variable_set

    def restore_backup_literal(self, literal: int) -> None:
        """
        Restore all nodes and edges that are mention in the backup for the variable.
        The backup for the variable will be cleared.
        :param literal: the literal
        :return: None
        :raises TryingRestoreLiteralHasNotBeenRemovedException: if the variable has not been removed
        :raises TryingRestoreLiteralIsNotLastOneRemovedException: if the literal is not the last one that was removed
        """

        variable = abs(literal)
        variable_hash = self.__variable_hash(variable)

        # The variable has not been removed from the incidence graph
        if variable not in self.__assigned_variable_set:
            raise ig_exception.TryingRestoreLiteralHasNotBeenRemovedException(literal)

        # The literal is not the last one that was removed
        last_literal = self.__assigned_literal_list[-1]
        if last_literal != literal:
            raise ig_exception.TryingRestoreLiteralIsNotLastOneRemovedException(literal, last_literal)

        # Eliminated redundant clauses
        eliminated_clause_node_dictionary = self.__eliminated_redundant_clauses_backup_dictionary[variable]
        for clause_id in eliminated_clause_node_dictionary:
            self.__satisfied_clause_set.remove(clause_id)
            self.add_clause_id(clause_id)

            clause_id_hash = self.__clause_id_hash(clause_id)
            eliminated_clause_node_neighbour_set = eliminated_clause_node_dictionary[clause_id]
            for neighbour_id in eliminated_clause_node_neighbour_set:
                neighbour_hash = self.__variable_hash(neighbour_id)

                # The neighbour does not exist (isolated node)
                if neighbour_hash not in self:
                    self.add_variable(neighbour_id)

                self.__add_edge(neighbour_hash, clause_id_hash)

        del self.__eliminated_redundant_clauses_backup_dictionary[variable]

        self.__assigned_variable_set.remove(variable)
        self.__neg_assigned_literal_set.remove(-literal)
        self.__assigned_literal_list.pop()

        # Restore clauses (the clauses are not satisfied anymore)
        clause_node_dictionary = self.__clause_node_backup_dictionary[variable]
        for clause_id in clause_node_dictionary:
            self.__satisfied_clause_set.remove(clause_id)
            self.add_clause_id(clause_id)

            clause_id_hash = self.__clause_id_hash(clause_id)
            clause_node_neighbour_set = clause_node_dictionary[clause_id]
            for neighbour_id in clause_node_neighbour_set:
                neighbour_hash = self.__variable_hash(neighbour_id)

                # The neighbour does not exist (isolated node)
                if neighbour_hash not in self:
                    self.add_variable(neighbour_id)

                self.__add_edge(neighbour_hash, clause_id_hash)

        del self.__clause_node_backup_dictionary[variable]

        # Restore the variable node
        self.add_variable(variable)
        variable_node_neighbour_set = self.__variable_node_backup_dictionary[variable]
        for neighbour_hash in variable_node_neighbour_set:
            self.__add_edge(variable_hash, neighbour_hash)

        del self.__variable_node_backup_dictionary[variable]

    def restore_backup_literal_set(self, literal_set: Set[int]) -> None:
        while len(literal_set):
            last_literal = self.__assigned_literal_list[-1]

            # The last literal in the backup does not exist in the set => choose any element in the set and cause an exception
            if last_literal not in literal_set:
                literal_temp = (random.sample(literal_set, 1))[0]
                self.restore_backup_literal(literal_temp)
            else:
                literal_set.remove(last_literal)
                self.restore_backup_literal(last_literal)
    # endregion

    # region Variable simplification
    def merge_variable_simplification(self, variable_simplification_dictionary: Dict[int, Set[int]]) -> None:
        """
        Merge variables based on the variable simplification dictionary.
        Everything changed in the incidence graph is saved and can be restored from the backup in future.
        :return: None
        """

        self.__update_adjacency_literal_dynamic_dictionary = False

        variable_to_delete_set = set()

        for representant in variable_simplification_dictionary:
            representant_hash = self.__variable_hash(representant)
            equivalence_set = variable_simplification_dictionary[representant]
            neighbour_hash_set = set()

            # Delete edges
            for variable in equivalence_set:
                variable_hash = self.__variable_hash(variable)
                neighbour_set_temp = set(self.neighbors(variable_hash))

                self.__removed_edge_backup_dictionary[variable] = neighbour_set_temp
                neighbour_hash_set.update(neighbour_set_temp)

                variable_to_delete_set.add(variable)

            if representant_hash not in self.__added_edge_backup_dictionary:
                self.__added_edge_backup_dictionary[representant_hash] = set()

            # Add edges
            for neighbour_hash in neighbour_hash_set:
                # The edge does not exist
                if not self.has_edge(representant_hash, neighbour_hash):
                    self.__added_edge_backup_dictionary[representant_hash].add(neighbour_hash)
                    self.__add_edge(representant_hash, neighbour_hash)

        # Delete nodes
        for variable in variable_to_delete_set:
            self.__temporarily_remove_variable(variable=variable,
                                               neighbour_set=self.__removed_edge_backup_dictionary[variable])

    def restore_backup_variable_simplification(self) -> None:
        """
        Restore all nodes and edges that are mention in the backup.
        The backup will be cleared.
        :return: None
        """

        # Add nodes and edges
        for variable in self.__removed_edge_backup_dictionary:
            variable_hash = self.__variable_hash(variable)
            neighbour_hash_set = self.__removed_edge_backup_dictionary[variable]

            self.add_variable(variable)
            for neighbour_hash in neighbour_hash_set:
                self.__add_edge(variable_hash, neighbour_hash)

        self.__removed_edge_backup_dictionary = dict()

        # Remove edges
        for variable_hash in self.__added_edge_backup_dictionary:
            neighbour_hash_set = self.__added_edge_backup_dictionary[variable_hash]

            for neighbour_hash in neighbour_hash_set:
                self.__temporarily_remove_edge(variable_hash, neighbour_hash)

        self.__added_edge_backup_dictionary = dict()

        self.__update_adjacency_literal_dynamic_dictionary = True
    # endregion

    # region Subsumption - variable
    def subsumption_variable(self) -> Set[int]:
        """
        Return a set of subsumed clauses concerning only variables
        :return: a set of subsumed clauses
        """

        self.__statistics.subsumption_variable.start_stopwatch()     # timer (start)

        subsumed_clause_set = set()
        neighbour_dictionary: [int, Set[int]] = dict()   # key: clause, value: a set of variables that occur in the clause
        clause_id_list = self.clause_id_list()

        for i, clause_a in enumerate(clause_id_list):
            # Neighbours
            if clause_a in neighbour_dictionary:
                variable_set_a = neighbour_dictionary[clause_a]
            else:
                variable_set_a = self.clause_id_neighbour_set(clause_a)
                neighbour_dictionary[clause_a] = variable_set_a

            for j in range(i + 1, len(clause_id_list)):
                clause_b = clause_id_list[j]

                if clause_b in subsumed_clause_set:
                    continue

                # Neighbours
                if clause_b in neighbour_dictionary:
                    variable_set_b = neighbour_dictionary[clause_b]
                else:
                    variable_set_b = self.clause_id_neighbour_set(clause_b)
                    neighbour_dictionary[clause_b] = variable_set_b

                a_subset_b = variable_set_a.issubset(variable_set_b)
                b_subset_a = variable_set_b.issubset(variable_set_a)

                # Clauses are the same
                if a_subset_b and b_subset_a:
                    if clause_a < clause_b:
                        subsumed_clause_set.add(clause_a)
                    else:
                        subsumed_clause_set.add(clause_b)

                    continue

                # Clause A is subsumed
                if a_subset_b:
                    subsumed_clause_set.add(clause_a)

                    continue

                # Clause B is subsumed
                if b_subset_a:
                    subsumed_clause_set.add(clause_b)

                    continue

        self.__statistics.subsumption_variable.stop_stopwatch()      # timer (stop)
        return subsumed_clause_set

    def remove_subsumed_clause_variable(self, clause_id: int) -> None:
        """
        Remove the clause from the incidence graph.
        Everything removed from the incidence graph is saved and can be restored from the backup in future.
        :param clause_id: the identifier of the clause
        :return: None
        :raises ClauseIdDoesNotExistException: if the clause does not exist in the incidence graph
        :raises ClauseHasBeenRemovedException: if the clause has been already removed
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # The clause has been already removed from the incidence graph
        if clause_id in self.__subsumption_variable_backup_dictionary:
            raise ig_exception.ClauseHasBeenRemovedException(clause_id)

        # The clause does not exist in the incidence graph
        if clause_id_hash not in self:
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        clause_neighbour_set = set(self.neighbors(clause_id_hash))
        self.__subsumption_variable_backup_dictionary[clause_id] = clause_neighbour_set

        # Delete the clause node
        self.__temporarily_remove_clause_id(clause_id=clause_id,
                                            neighbour_set=clause_neighbour_set)

    def remove_subsumed_clause_variable_set(self, clause_id_set: Set[int]) -> None:
        for clause_id in clause_id_set:
            self.remove_subsumed_clause_variable(clause_id)

    def restore_backup_subsumption_variable(self) -> None:
        """
        Restore all nodes and edges that are mention in the backup.
        The backup will be cleared.
        :return: None
        """

        for clause_id in self.__subsumption_variable_backup_dictionary:
            clause_id_hash = self.__clause_id_hash(clause_id)
            neighbour_hash_set = self.__subsumption_variable_backup_dictionary[clause_id]

            self.add_clause_id(clause_id)
            for neighbour_hash in neighbour_hash_set:
                self.__add_edge(neighbour_hash, clause_id_hash)

        self.__subsumption_variable_backup_dictionary = dict()
    # endregion

    # region TwoCnf, HornCnf
    def convert_to_cnf(self) -> PySatCnf:
        """
        Convert the formula represented by the incidence graph to CNF
        :return: PySAT CNF
        """

        self.__statistics.convert_to_cnf.start_stopwatch()  # timer (start)

        result = self.__convert_to_cnf(psc_enum.PySatCnfEnum.CNF)

        self.__statistics.convert_to_cnf.stop_stopwatch()   # timer (stop)
        return result

    def convert_to_2_cnf(self) -> PySat2Cnf:
        """
        Convert the formula represented by the incidence graph to 2-CNF
        :return: PySAT 2CNF
        :raises FormulaIsNot2CnfException: if the formula is not 2-CNF
        """

        self.__statistics.convert_to_2_cnf.start_stopwatch()    # timer (start)

        result = self.__convert_to_cnf(psc_enum.PySatCnfEnum.TWO_CNF)

        self.__statistics.convert_to_2_cnf.stop_stopwatch()     # timer (stop)
        return result

    def convert_to_horn_cnf(self, renaming_function: Union[Set[int], None] = None) -> PySatHornCnf:
        """
        Convert the formula represented by the incidence graph to HornCNF
        :param renaming_function: a set of variables that will be renamed
        :return: PySAT HornCNF
        :raises FormulaIsNotHornException: if the formula is not Horn
        """

        self.__statistics.convert_to_horn_cnf.start_stopwatch()     # timer (start)

        result = self.__convert_to_cnf(psc_enum.PySatCnfEnum.HORN_CNF, renaming_function)

        self.__statistics.convert_to_horn_cnf.stop_stopwatch()      # timer (stop)
        return result

    def is_2_cnf(self) -> bool:
        """
        :return: True if the incidence graph represents a 2-CNF. Otherwise, False is returned.
        """

        number_of_unit_clauses = len(self.__length_set_clauses_dictionary[1])
        number_of_not_unit_clauses = self.number_of_clauses() - number_of_unit_clauses

        if number_of_not_unit_clauses == 0:
            self.__statistics.two_cnf_ratio.add_count(1)  # counter
            return True

        ratio = (self.number_of_edges() - number_of_unit_clauses) / number_of_not_unit_clauses

        if ratio < 2:
            raise c_exception.SomethingWrongException(f"preconditions for the function is_2_cnf are not satisfied (ratio ({ratio}) < 2)")

        if ratio == 2:
            self.__statistics.two_cnf_ratio.add_count(1)    # counter
            return True

        self.__statistics.two_cnf_ratio.add_count(0)    # counter
        return False

    def initialize_renamable_horn_formula_recognition(self) -> None:
        """
        Initialize the recognition algorithm for renamable Horn formulae
        :return: None
        """

        self.__statistics.renamable_horn_formula_recognition_initialization.start_stopwatch()   # timer (start)

        self.__ignored_literal_set_renamable_horn_formula_recognition = set()
        self.__renamable_horn_formula_recognition = RenamableHornFormulaRecognition(self)

        self.__statistics.renamable_horn_formula_recognition_initialization.stop_stopwatch()    # timer (stop)

    def is_renamable_horn_formula(self) -> Union[Set[int], None]:
        """
        :return: If the incidence graph represents (renamable) Horn formula, a renaming function (a set of variables) is returned. Otherwise, None is returned.
        :raises RenamableHornFormulaRecognitionHasNotBeenInitializedException: if the renamable Horn formula recognition has not been initialized
        """

        # The renamable Horn formula recognition has not been initialized
        if self.__renamable_horn_formula_recognition is None:
            raise ig_exception.RenamableHornFormulaRecognitionHasNotBeenInitializedException()

        self.__statistics.renamable_horn_formula_recognition_check.start_stopwatch()    # timer (start)

        neg_assigned_literal_set = self.__ignored_literal_set_renamable_horn_formula_recognition.union(self.__neg_assigned_literal_set)
        result = self.__renamable_horn_formula_recognition.is_renamable_horn_formula(satisfied_clause_set=self.__satisfied_clause_set,
                                                                                     unresolved_clause_set=self._clause_id_set,
                                                                                     neg_assigned_literal_set=neg_assigned_literal_set,
                                                                                     variable_restriction_set=self._variable_set)

        if result is not None:
            self.__statistics.renamable_horn_formula_ratio.add_count(1)     # counter
        else:
            self.__statistics.renamable_horn_formula_ratio.add_count(0)     # counter

        self.__statistics.renamable_horn_formula_recognition_check.stop_stopwatch()     # timer (stop)
        return result
    # endregion

    # region Decision heuristics
    def get_literals_in_binary_clauses(self) -> Set[int]:
        """
        :return: a set of literals that occur in binary clauses
        """

        binary_clause_set = self.__length_set_clauses_dictionary[2]
        literal_set = set()

        for binary_clause_id in binary_clause_set:
            clause = self.__clause_dictionary[binary_clause_id]
            literal_set.update(clause)

        return literal_set

    def literal_number_of_occurrences(self, literal: int, ignore_binary_clauses: bool = False) -> Union[int, Tuple[int, int]]:
        """
        Return the number of occurrences of the literal
        :param literal: a literal
        :param ignore_binary_clauses: True if the binary clauses are ignored
        :return: the number of occurrences
        :raises VariableDoesNotExistException: if the variable (|literal|) does not exist in the incidence graph
        """

        variable = abs(literal)
        variable_hash = self.__variable_hash(variable)

        # The variable does not exist in the incidence graph
        if variable_hash not in self:
            raise ig_exception.VariableDoesNotExistException(variable)

        clause_set = self.__adjacency_literal_dynamic_dictionary[literal]

        if not ignore_binary_clauses:
            return len(clause_set)

        return len(clause_set.difference(self.__length_set_clauses_dictionary[2])), len(clause_set)

    def literal_set_number_of_occurrences(self, literal_set: Set[int]) -> int:
        sum_temp = 0
        for literal in literal_set:
            sum_temp += self.literal_number_of_occurrences(literal, ignore_binary_clauses=False)

        return sum_temp

    def literal_number_of_occurrences_dictionary(self, literal: int) -> Dict[int, int]:
        """
        Return the number of occurrences of the literal for each clause size
        :param literal: a literal
        :return: the number of occurrences for each clause size
        :raises VariableDoesNotExistException: if the variable (|literal|) does not exist in the incidence graph
        """

        variable = abs(literal)
        variable_hash = self.__variable_hash(variable)

        # The variable does not exist in the incidence graph
        if variable_hash not in self:
            raise ig_exception.VariableDoesNotExistException(variable)

        number_of_occurrences_dictionary: Dict[int, int] = dict()
        clause_set = self.__adjacency_literal_dynamic_dictionary[literal]

        for clause_id in clause_set:
            clause_length = self.__clause_length_dictionary[clause_id]

            if clause_length not in number_of_occurrences_dictionary:
                number_of_occurrences_dictionary[clause_length] = 1
            else:
                number_of_occurrences_dictionary[clause_length] += 1

        return number_of_occurrences_dictionary

    def variable_number_of_occurrences(self, variable: int) -> int:
        """
        Return the number of occurrences of the variable
        :param variable: a variable
        :return: the number of occurrences
        :raises VariableDoesNotExistException: if the variable does not exist in the incidence graph
        """

        return self.literal_number_of_occurrences(variable) + self.literal_number_of_occurrences(-variable)

    def variable_with_most_occurrences(self, variable_restriction_set: Union[Set[int], None] = None) -> Union[int, None]:
        """
        :param variable_restriction_set: a set of variables that will be taken into account (None for all variables)
        :return: a variable with the most occurrences
        :raises VariableDoesNotExistException: if any variable does not exist in the incidence graph
        """

        max_occurrences = 0
        max_variable = None

        if variable_restriction_set is None:
            variable_set_temp = self._variable_set
        else:
            variable_set_temp = variable_restriction_set

        for variable in variable_set_temp:
            temp = self.variable_number_of_occurrences(variable)

            if temp > max_occurrences:
                max_occurrences = temp
                max_variable = variable

        return max_variable

    def literal_sum_lengths_clauses(self, literal: int, jeroslow_wang: bool = False, ignore_binary_clauses: bool = False) -> Union[int, Tuple[int, int]]:
        """
        Return the sum of lengths of clauses where the literal occurs
        :param literal: a literal
        :param jeroslow_wang: False for sum(|w|). True for sum(2^-|w|).
        :param ignore_binary_clauses: True if the binary clauses are ignored
        :return: the sum of lengths of clauses
        :raises VariableDoesNotExistException: if the variable (|literal|) does not exist in the incidence graph
        """

        variable = abs(literal)
        variable_hash = self.__variable_hash(variable)

        # The variable does not exist in the incidence graph
        if variable_hash not in self:
            raise ig_exception.VariableDoesNotExistException(variable)

        sum_temp = 0
        sum_ignore_binary_temp = 0

        for clause_id in self.__adjacency_literal_dynamic_dictionary[literal]:
            clause_len = self.__clause_length_dictionary[clause_id]

            # sum(2^-|w|)
            if jeroslow_wang:
                sum_temp += 2**(-clause_len)

                if ignore_binary_clauses and (clause_len > 2):
                    sum_ignore_binary_temp += 2**(-clause_len)
            # sum(|w|)
            else:
                sum_temp += clause_len

                if ignore_binary_clauses and (clause_len > 2):
                    sum_ignore_binary_temp += clause_len

        if ignore_binary_clauses:
            return sum_ignore_binary_temp, sum_temp

        return sum_temp

    def literal_set_sum_lengths_clauses(self, literal_set: Set[int]) -> int:
        sum_temp = 0
        for literal in literal_set:
            sum_temp += self.literal_sum_lengths_clauses(literal)

        return sum_temp

    def variable_sum_lengths_clauses(self, variable: int) -> int:
        """
        Return the sum of lengths of clauses where the variable occurs
        :param variable: a variable
        :return: the sum of length of clauses
        :raises VariableDoesNotExistException: if the variable does not exist in the incidence graph
        """

        return self.literal_sum_lengths_clauses(variable) + self.literal_sum_lengths_clauses(-variable)

    def get_binary_clause_set(self, copy: bool):
        """
        Return a set of binary clauses in the incidence graph
        :param copy: True if a copy is returned
        :return: a set of binary clauses
        """

        if copy:
            return self.__length_set_clauses_dictionary[2].copy()

        return self.__length_set_clauses_dictionary[2]
    # endregion

    def create_incidence_graphs_for_components(self) -> Set[TIncidenceGraph]:
        """
        For each connected component will be created a new incidence graph
        :return: a set of incidence graphs (one for each component)
        """

        self.__statistics.create_incidence_graphs_for_components.start_stopwatch()  # timer (start)

        incidence_graph_set = set()

        # Renamable Horn formula recognition
        ignored_literal_set_temp = None
        if self.__renamable_horn_formula_recognition is not None:
            ignored_literal_set_temp = self.__ignored_literal_set_renamable_horn_formula_recognition.union(self.__neg_assigned_literal_set)

        for component in nx.connected_components(self):
            incidence_graph_temp = IncidenceGraph(statistics=self.__statistics,
                                                  renamable_horn_formula_recognition=self.__renamable_horn_formula_recognition,
                                                  ignored_literal_set_renamable_horn_formula_recognition=ignored_literal_set_temp)

            for node_hash in component:
                # The node is not a clause
                if self.__is_node_variable(node_hash):
                    continue

                clause_id = self.__unhash(node_hash)
                clause_set = self.__clause_dictionary[clause_id]
                incidence_graph_temp.add_clause(clause_id, clause_set)

            incidence_graph_set.add(incidence_graph_temp)

        self.__statistics.create_incidence_graphs_for_components.stop_stopwatch()   # timer (stop)
        return incidence_graph_set

    def get_connected_components(self) -> List[Set[int]]:
        """
        :return: a list of connected components where a set of variables represents a connected component
        """

        self.__statistics.get_connected_components.start_stopwatch()    # timer (start)

        # The incidence graph is connected => one component
        if self.is_connected():
            self.__statistics.get_connected_components.stop_stopwatch()     # timer (stop)
            return [self._variable_set]

        connected_component_list = []

        for component in nx.connected_components(self):
            connected_component_list.append(set(map(lambda variable_hash: self.__unhash(variable_hash),
                                                    filter(lambda node_hash: self.__is_node_variable(node_hash), component))))

        self.__statistics.get_connected_components.stop_stopwatch()     # timer (stop)
        return connected_component_list

    def copy_incidence_graph(self) -> TIncidenceGraph:
        """
        :return: a copy of the incidence graph
        """

        self.__statistics.copy_incidence_graph.start_stopwatch()    # timer (start)

        copy = IncidenceGraph(statistics=self.__statistics)

        for node_hash in self.nodes:
            # The node is not a clause
            if self.__is_node_variable(node_hash):
                continue

            clause_id = self.__unhash(node_hash)
            clause_set = self.__clause_dictionary[clause_id]
            copy.add_clause(clause_id, clause_set)

        # Renamable Horn formula recognition
        if self.__renamable_horn_formula_recognition is not None:
            copy.initialize_renamable_horn_formula_recognition()

        self.__statistics.copy_incidence_graph.stop_stopwatch()     # timer (stop)
        return copy
    # endregion

    # region Magic method
    def __str__(self):
        string_temp = ""
        clause_id_sorted_list = sorted(self._clause_id_set)

        for clause_id in clause_id_sorted_list:
            clause = self.get_sorted_clause(clause_id, copy=False)
            string_temp = "\n".join((string_temp, f"Clause {clause_id}: {clause}"))

        return string_temp
    # endregion

    # region Property
    @property
    def statistics(self) -> IncidenceGraphStatistics:
        return self.__statistics
    # endregion
