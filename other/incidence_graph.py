# Import
import networkx as nx
from networkx.classes.graph import Graph
from typing import Set, Dict, List, Tuple, Union

# Import exception
import exception.formula.incidence_graph_exception as ig_exception


class IncidenceGraph(Graph):
    """
    Incidence graph
    """

    """
    Private int number_of_variables
    Private int number_of_clauses
    
    Private Dict<int, Set<str>> adjacency_literal_node_dictionary           # key: a literal, value: a set of clauses (nodes) where the literal appears
    
    Private Set<int> variable_backup_set
    Private List<int> literal_backup_list
    Private Dict<int, Set<str>> variable_node_backup_dictionary             # key: a variable, value: a set of clauses (nodes) that were incident with the variable node when the variable node was being deleted
    Private Dict<int, Dict<str, Set<str>> clause_node_backup_dictionary     # key: a variable, value: a dictionary, where a key is a clause node that was satisfied because of the variable, and the value is a set of variables (nodes) that were incident with the clause node when the clause node was being deleted
    """

    def __init__(self, number_of_variables: int, number_of_clauses: int):
        super().__init__()

        self.__number_of_variables: int = number_of_variables
        self.__number_of_clauses: int = number_of_clauses

        self.__adjacency_literal_node_dictionary: Dict[int, Set[str]] = dict()

        # Backup
        self.__variable_backup_set: Set[int] = set()
        self.__literal_backup_list: List[int] = []
        self.__variable_node_backup_dictionary: Dict[int, Set[str]] = dict()
        self.__clause_node_backup_dictionary: Dict[int, Dict[str, Set[str]]] = dict()

        # Create nodes
        for variable in range(1, self.__number_of_variables + 1):
            self.__add_variable(variable)
        for clause_id in range(0, self.__number_of_clauses):
            self.__add_clause_id(clause_id)

    # region Private method
    def __variable_hash(self, variable: int) -> str:
        """
        :return: a hash key for the variable
        """

        return f"v{variable}"

    def __clause_id_hash(self, clause_id: int) -> str:
        """
        :return: a hash key for the clause's id
        """

        return f"c{clause_id}"

    def __add_variable(self, variable: int) -> None:
        self.add_node(self.__variable_hash(variable), value=variable, bipartite=0)

    def __add_clause_id(self, clause_id: int) -> None:
        self.add_node(self.__clause_id_hash(clause_id), value=clause_id, bipartite=1)

    def __variable_exist(self, variable: int) -> bool:
        """
        :return: True if the variable exists in the incidence graph. Otherwise, False is returned.
        """

        if (variable >= 1) and (variable <= self.__number_of_variables):
            return True

        return False

    def __clause_id_exist(self, clause_id: int) -> bool:
        """
        :return: True if the clause's id exists in the incidence graph. Otherwise, False is returned.
        """

        if (clause_id >= 0) and (clause_id < self.__number_of_clauses):
            return True

        return False

    def __node_exist(self, node_hash: str) -> bool:
        """
        :return: True if the node exists in the incidence graph. Otherwise, False is returned.
        """

        if node_hash in self.nodes:
            return True

        return False
    # endregion

    # region Public method
    def add_edge(self, literal: int, clause_id: int) -> None:
        """
        Add a new edge to the incidence graph (|literal| - clause_id).
        If the variable (|literal|) does not exist in the incidence graph, raise an exception (VariableDoesNotExistException).
        If the clause's id does not exist in the incidence graph, raise an exception (ClauseIdDoesNotExistException).
        :param literal: the literal
        :param clause_id: the clause's id
        :return: None
        """

        variable = abs(literal)
        # The variable does not exist in the incidence graph
        if not self.__variable_exist(variable):
            raise ig_exception.VariableDoesNotExistException(variable)

        # The clause's id does not exist in the incidence graph
        if not self.__clause_id_exist(clause_id):
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        # adjacency_literal_node_dictionary
        if literal not in self.__adjacency_literal_node_dictionary:
            self.__adjacency_literal_node_dictionary[literal] = set()
        self.__adjacency_literal_node_dictionary[literal].add(self.__clause_id_hash(clause_id))

        super().add_edge(self.__variable_hash(variable), self.__clause_id_hash(clause_id), literal=literal)

    def is_connected(self) -> bool:
        """
        :return: True if the incidence graph is connected. Otherwise, False is returned.
        """

        return nx.is_connected(self)

    def number_of_components(self) -> int:
        """
        :return: the number of connected components
        """

        return nx.number_connected_components(self)

    def variable_neighbour_set(self, variable: int) -> Set[int]:
        """
        Return a set of clauses (nodes) that are incident with the variable.
        If the variable does not exist in the incidence graph, raise an exception (VariableDoesNotExistException).
        :param variable: the variable
        :return: a set of neighbours (clauses) of the variable
        """

        # The variable does not exist in the incidence graph
        if not self.__variable_exist(variable):
            raise ig_exception.VariableDoesNotExistException(variable)

        return set(self.nodes[n]["value"] for n in self.neighbors(self.__variable_hash(variable)))

    def clause_id_neighbour_set(self, clause_id: int) -> Set[int]:
        """
        Return a set of variables (nodes) that are incident with the clause.
        If the clause's id does not exist in the incidence graph, raise an exception (ClauseIdDoesNotExistException).
        :param clause_id: the clause's id
        :return: a set of neighbours (variables) of the clause
        """

        # The clause's id does not exist in the incidence graph
        if not self.__clause_id_exist(clause_id):
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        return set(self.nodes[n]["value"] for n in self.neighbors(self.__clause_id_hash(clause_id)))

    def remove_variable(self, literal: int) -> None:
        """
        Remove the variable node |literal|.
        Remove all (satisfied) clauses (nodes), which are incident with the variable node and contain the literal.
        Everything that will be removed from the incidence graph is saved and can be restored from backups in the future.
        If the variable does not exist in the incidence graph, raise an exception (VariableDoesNotExistException).
        If the variable has been already removed, raise an exception (VariableHasBeenRemovedException).
        :param literal: the literal
        :return: None
        """

        variable = abs(literal)
        # The variable does not exist in the incidence graph
        if not self.__variable_exist(variable):
            raise ig_exception.VariableDoesNotExistException(variable)

        # The variable has been already removed from the incidence graph
        if variable in self.__variable_backup_set:
            raise ig_exception.VariableHasBeenRemovedException(variable)

        # Ensure that the value exists
        if literal not in self.__adjacency_literal_node_dictionary:
            self.__adjacency_literal_node_dictionary[literal] = set()

        # Backup
        self.__variable_backup_set.add(variable)
        self.__literal_backup_list.append(literal)

        variable_hash = self.__variable_hash(variable)
        variable_node_neighbour_set = set(self.neighbors(variable_hash))
        self.__variable_node_backup_dictionary[variable] = variable_node_neighbour_set

        # Delete the variable node
        self.remove_node(variable_hash)

        clause_node_dictionary = dict()
        for clause_id_hash in self.__adjacency_literal_node_dictionary[literal]:
            # The node has been already deleted
            if not self.__node_exist(clause_id_hash):
                continue

            clause_node_neighbour_set = set(self.neighbors(clause_id_hash))
            clause_node_dictionary[clause_id_hash] = clause_node_neighbour_set

            # Delete the satisfied clause
            self.remove_node(clause_id_hash)

        self.__clause_node_backup_dictionary[variable] = clause_node_dictionary
    # endregion
