# Import
from formula.cnf import Cnf
from typing import Set, Dict, List, Tuple


class Hypergraph:
    """
    Hypergraph representation
    """

    """
    Private Cnf cnf
    Private int number_of_nodes                         # number of clauses
    Private int number_of_hyperedges                    # number of variables
    Private Set<int> variable_set
    
    Private Dict<int, int> node_weight_dictionary       # key: node = clause's id, value: the weight of the clause
    Private Dict<int, int> hyperedge_weight_dictionary  # key: edge = variable, value: the weight of the variable
    
    Private Dict<int, Set<int>> hypergraph_dictionary   # key: variable, value: a set of clauses where the variable appears
    """

    # TODO Cache

    def __init__(self, cnf: Cnf):
        self.__cnf: Cnf = cnf
        self.__number_of_nodes: int = cnf.real_number_of_clauses
        self.__number_of_hyperedges: int = cnf.number_of_variables
        self.__variable_set: Set[int] = cnf._get_variable_set(copy=True)

        self.__node_weight_dictionary: Dict[int, int] = dict()
        self.__hyperedge_weight_dictionary: Dict[int, int] = dict()

        self.__hypergraph_dictionary: Dict[int, Set[int]] = dict()

        self.__create_hypergraph()
        self.__set_weights()

    # region Private method
    def __create_hypergraph(self):
        """
        Initialize the hypergraph
        Variable: hypergraph_dictionary
        """

        for variable in self.__variable_set:
            clause_temp = set()

            # Positive literal
            clause_temp.update(self.__cnf._get_clause_set(variable))
            # Negative literal
            clause_temp.update(self.__cnf._get_clause_set(-variable))

            self.__hypergraph_dictionary[variable] = clause_temp

    def __set_weights(self):
        """
        Initialize the weights
        Variable: node_weight_dictionary, hyperedge_weight_dictionary
        """

        # Node's weight
        for node in range(self.__number_of_nodes):
            self.__node_weight_dictionary[node] = 1

        # Hyperedge's weight
        for hyperedge in self.__variable_set:
            self.__hyperedge_weight_dictionary[hyperedge] = 1

    def __get_hypergraph(self, clause_id_set: Set[int], ignored_variable_set: Set[int]):
        # TODO
        pass
    # endregion

    # region Public method
    def get_cut_set(self, clause_id_set: Set[int], ignored_literal_list: List[int], use_caches: bool = True) -> Set[int]:
        """
        Create a hypergraph, where nodes (clauses) are restricted to the clause_id_set and
        hyperedges (variables) are restricted to all variables except those which are in the ignored_literal_list.
        Return a cut set of the hypergraph.
        """

        ignored_variable_set = set()
        for literal in ignored_literal_list:
            variable = abs(literal)
            if variable in self.__variable_set:
                ignored_variable_set.add(variable)

        # TODO

        return set()
    # endregion

    # region Magic method
    def __str__(self):
        string_temp = "".join(f"Number of nodes: {self.number_of_nodes}")
        string_temp = "\n".join((string_temp, f"Number of hyperedges: {self.number_of_hyperedges}"))

        return string_temp
    # endregion

    # region Property
    @property
    def number_of_nodes(self):
        return self.__number_of_nodes

    @property
    def number_of_hyperedges(self):
        return self.__number_of_hyperedges
    # endregion
