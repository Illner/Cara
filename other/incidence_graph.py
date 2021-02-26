# Import
import networkx as nx
from networkx.classes.graph import Graph
from typing import Set, Dict, List, Tuple, Union, TypeVar

# Import exception
import exception.formula.incidence_graph_exception as ig_exception

# Type
TIncidenceGraph = TypeVar("TIncidenceGraph", bound="IncidenceGraph")


class IncidenceGraph(Graph):
    """
    Incidence graph
    """

    """
    Private Dict<int, Set<str>> adjacency_literal_dictionary                # key: a literal, value: a set of clauses (nodes) where the literal appears
    
    Private Set<int> variable_backup_set
    Private List<int> literal_backup_list
    Private Dict<int, Set<str>> variable_node_backup_dictionary             # key: a variable, value: a set of clauses (nodes) that were incident with the variable node when the variable node was being deleted
    Private Dict<int, Dict<int, Set<str>> clause_node_backup_dictionary     # key: a variable, value: a dictionary, where a key is a clause node that was satisfied because of the variable, and the value is a set of variables (nodes) that were incident with the clause node when the clause node was being deleted
    """

    def __init__(self, number_of_variables: Union[int, None] = None, number_of_clauses: Union[int, None] = None):
        super().__init__()

        self.__adjacency_literal_dictionary: Dict[int, Set[int]] = dict()

        # Backup
        self.__variable_backup_set: Set[int] = set()
        self.__literal_backup_list: List[int] = []
        self.__variable_node_backup_dictionary: Dict[int, Set[str]] = dict()
        self.__clause_node_backup_dictionary: Dict[int, Dict[int, Set[str]]] = dict()

        # Create nodes
        if number_of_variables is not None:
            for variable in range(1, number_of_variables + 1):
                self.add_variable(variable)
        if number_of_clauses is not None:
            for clause_id in range(0, number_of_clauses):
                self.add_clause_id(clause_id)

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

    def __node_exist(self, node_hash: str) -> bool:
        """
        :return: True if the node exists in the incidence graph. Otherwise, False is returned.
        """

        if node_hash in self.nodes:
            return True

        return False

    def __is_node_variable(self, node_hash: str) -> Union[bool, None]:
        """
        :return: True if the node is a variable, otherwise False is returned.
        If the node does not exist in the incidence graph, None is returned.
        """

        # The node does not exist in the incidence graph
        if not self.__node_exist(node_hash):
            return None

        return self.nodes[node_hash]["bipartite"] == 0
    # endregion

    # region Public method
    def add_variable(self, variable: int) -> None:
        """
        Add a new variable to the incidence graph.
        If the variable already exists in the incidence graph, raise an exception (VariableAlreadyExistsException).
        :return: None
        """

        variable_hash = self.__variable_hash(variable)

        # The variable already exists in the incidence graph
        if self.__node_exist(variable_hash):
            raise ig_exception.VariableAlreadyExistsException(variable)

        self.add_node(variable_hash, value=variable, bipartite=0)

    def add_clause_id(self, clause_id: int) -> None:
        """
        Add a new clause to the incidence graph.
        If the clause already exists in the incidence graph, raise an exception (ClauseIdAlreadyExistsException).
        :return: None
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # The clause already exists in the incidence graph
        if self.__node_exist(clause_id_hash):
            raise ig_exception.ClauseIdAlreadyExistsException(clause_id)

        self.add_node(clause_id_hash, value=clause_id, bipartite=1)

    def add_edge(self, literal: int, clause_id: int, create_node: bool = False) -> None:
        """
        Add a new edge to the incidence graph (|literal| - clause_id).
        If the edge already exists in the incidence graph, nothing happens.
        If the variable (|literal|) does not exist in the incidence graph, raise an exception (VariableDoesNotExistException).
        If the clause's id does not exist in the incidence graph, raise an exception (ClauseIdDoesNotExistException).
        :param literal: the literal
        :param clause_id: the clause's id
        :param create_node: True - a node will be created if it does not exist in the incidence graph.
        False - if a node does not exist in the incidence graph, an exception will be raised.
        :return: None
        """

        variable = abs(literal)
        variable_hash = self.__variable_hash(variable)
        clause_id_hash = self.__clause_id_hash(clause_id)

        # The variable does not exist in the incidence graph
        if not self.__node_exist(variable_hash):
            if create_node:
                self.add_variable(variable)
            else:
                raise ig_exception.VariableDoesNotExistException(variable)

        # The clause's id does not exist in the incidence graph
        if not self.__node_exist(clause_id_hash):
            if create_node:
                self.add_clause_id(clause_id)
            else:
                raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        # The edge already exists in the incidence graph
        if self.has_edge(variable_hash, clause_id_hash):
            return

        # adjacency_literal_node_dictionary
        if literal not in self.__adjacency_literal_dictionary:
            self.__adjacency_literal_dictionary[literal] = set()
        if -literal not in self.__adjacency_literal_dictionary:
            self.__adjacency_literal_dictionary[-literal] = set()
        self.__adjacency_literal_dictionary[literal].add(clause_id)

        super().add_edge(variable_hash, clause_id_hash)

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

        variable_hash = self.__variable_hash(variable)

        # The variable does not exist in the incidence graph
        if not self.__node_exist(variable_hash):
            raise ig_exception.VariableDoesNotExistException(variable)

        return set(self.nodes[n]["value"] for n in self.neighbors(variable_hash))

    def clause_id_neighbour_set(self, clause_id: int) -> Set[int]:
        """
        Return a set of variables (nodes) that are incident with the clause.
        If the clause's id does not exist in the incidence graph, raise an exception (ClauseIdDoesNotExistException).
        :param clause_id: the clause's id
        :return: a set of neighbours (variables) of the clause
        """

        clause_id_hash = self.__clause_id_hash(clause_id)

        # The clause's id does not exist in the incidence graph
        if not self.__node_exist(clause_id_hash):
            raise ig_exception.ClauseIdDoesNotExistException(clause_id)

        return set(self.nodes[n]["value"] for n in self.neighbors(clause_id_hash))

    def clause_id_set(self) -> Set[int]:
        """
        :return: a set of clauses that are in the incidence graph
        """

        return set(self.nodes[n]["value"] for n, d in self.nodes(data=True) if d["bipartite"] == 1)

    def remove_literal(self, literal: int) -> None:
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
        variable_hash = self.__variable_hash(variable)

        # The variable does not exist in the incidence graph
        if not self.__node_exist(variable_hash):
            raise ig_exception.VariableDoesNotExistException(variable)

        # The variable has been already removed from the incidence graph
        if variable in self.__variable_backup_set:
            raise ig_exception.VariableHasBeenRemovedException(variable)

        # Ensure that the value exists
        if literal not in self.__adjacency_literal_dictionary:
            self.__adjacency_literal_dictionary[literal] = set()

        # Backup
        self.__variable_backup_set.add(variable)
        self.__literal_backup_list.append(literal)

        variable_node_neighbour_set = set(self.neighbors(variable_hash))
        self.__variable_node_backup_dictionary[variable] = variable_node_neighbour_set

        # Delete the variable node
        self.remove_node(variable_hash)

        clause_node_dictionary = dict()
        for clause_id in self.__adjacency_literal_dictionary[literal]:
            clause_id_hash = self.__clause_id_hash(clause_id)

            # The node has been already deleted
            if not self.__node_exist(clause_id_hash):
                continue

            clause_node_neighbour_set = set(self.neighbors(clause_id_hash))
            clause_node_dictionary[clause_id] = clause_node_neighbour_set

            # Delete the satisfied clause
            self.remove_node(clause_id_hash)

        self.__clause_node_backup_dictionary[variable] = clause_node_dictionary

    def restore_backup_literal(self, literal: int) -> None:
        """
        Restore all nodes and edges that are mention in the backup for the variable.
        The backup for the variable will be removed.
        If the variable does not exist in the incidence graph, raise an exception (VariableDoesNotExistException).
        If the variable has not been removed, raise an exception (TryingRestoreLiteralHasNotBeenRemovedException).
        If the literal is not the last one that was removed, raise an exception (TryingRestoreLiteralIsNotLastOneRemovedException).
        :param literal: the literal
        :return: None
        """

        variable = abs(literal)
        variable_hash = self.__variable_hash(variable)

        # The variable does not exist in the incidence graph
        if not self.__node_exist(variable_hash):
            raise ig_exception.VariableDoesNotExistException(variable)

        # The variable has not been removed from the incidence graph
        if variable not in self.__variable_backup_set:
            raise ig_exception.TryingRestoreLiteralHasNotBeenRemovedException(literal)

        # The literal is not the last one that was removed
        last_literal = self.__literal_backup_list[-1]
        if last_literal != literal:
            raise ig_exception.TryingRestoreLiteralIsNotLastOneRemovedException(literal, last_literal)

        self.__variable_backup_set.remove(variable)
        self.__literal_backup_list.pop()

        # Restore clauses
        clause_node_dictionary = self.__clause_node_backup_dictionary[variable]
        for clause_id in clause_node_dictionary:
            self.add_clause_id(clause_id)

            clause_id_hash = self.__clause_id_hash(clause_id)
            clause_node_neighbour_set = clause_node_dictionary[clause_id]
            for neighbour in clause_node_neighbour_set:
                super().add_edge(neighbour, clause_id_hash)

        del self.__clause_node_backup_dictionary[variable]

        # Restore the variable node
        self.add_variable(variable)
        variable_node_neighbour_set = self.__variable_node_backup_dictionary[variable]
        for neighbour in variable_node_neighbour_set:
            super().add_edge(variable_hash, neighbour)

        del self.__variable_node_backup_dictionary[variable]

    def create_incidence_graphs_for_components(self) -> Set[TIncidenceGraph]:
        """
        For each connected component will be created a new incidence graph
        :return: a set of incidence graphs (one for each component)
        """

        incidence_graph_set = set()

        for component in nx.connected_components(self):
            incidence_graph_temp = IncidenceGraph()

            for node_hash in component:
                # The node is not a variable
                if not self.__is_node_variable(node_hash):
                    continue

                for neighbour_hash in self.neighbors(node_hash):
                    variable = self.nodes[node_hash]["value"]
                    clause_id = self.nodes[neighbour_hash]["value"]

                    literal = variable  # Positive literal
                    if clause_id in self.__adjacency_literal_dictionary[-variable]:     # Negative literal
                        literal = -variable

                    incidence_graph_temp.add_edge(literal, clause_id, create_node=True)

                incidence_graph_set.add(incidence_graph_temp)

        return incidence_graph_set
    # endregion
