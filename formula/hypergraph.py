# Import
import os
from pathlib import Path
from formula.cnf import Cnf
import other.environment as env
from typing import Set, Dict, List, Tuple

# Import exception
import exception.formula.hypergraph_exception as h_exception

# Import enum
import formula.hypergraph_cache_enum as hc_enum
import formula.hypergraph_weight_enum as hw_enum
import formula.hypergraph_software_enum as hs_enum


class Hypergraph:
    """
    Hypergraph representation
    """

    """
    Private Cnf cnf
    Private int number_of_nodes                         # number of clauses
    Private int number_of_hyperedges                    # number of variables
    Private Set<int> variable_set
    Private HypergraphCacheEnum cache_enum
    Private HypergraphWeightEnum weight_enum
    Private HypergraphSoftwareEnum software_enum
    
    Private Dict<int, int> node_static_weight_dictionary       # key: node = clause's id, value: the weight of the clause
    Private Dict<int, int> hyperedge_static_weight_dictionary  # key: edge = variable, value: the weight of the variable
    
    Private Dict<int, Set<int>> hypergraph_dictionary   # key: variable, value: a set of clauses where the variable appears
    """

    # Static variable - Path
    TEMP_FOLDER_PATH = os.path.join(os.getcwd(), "temp")
    WIN_PROGRAM_HMETIS_PATH = os.path.join(os.getcwd(), "external", "hypergraph_partitioning", "hMETIS", "win", "hmetis.exe")

    # TODO Cache
    # TODO Cache enum
    # TODO Cut_set enum

    def __init__(self, cnf: Cnf, cache_enum: hc_enum.HypergraphCacheEnum = hc_enum.HypergraphCacheEnum.NONE,
                 weight_enum: hw_enum.HypergraphWeightEnum = hw_enum.HypergraphWeightEnum.NONE,
                 software_enum: hs_enum.HypergraphSoftwareEnum = hs_enum.HypergraphSoftwareEnum.HMETIS):
        self.__cnf: Cnf = cnf
        self.__cache_enum = cache_enum
        self.__weight_enum = weight_enum
        self.__software_enum = software_enum
        self.__number_of_nodes: int = cnf.real_number_of_clauses
        self.__number_of_hyperedges: int = cnf.number_of_variables
        self.__variable_set: Set[int] = cnf._get_variable_set(copy=True)

        self.__node_static_weight_dictionary: Dict[int, int] = dict()
        self.__hyperedge_static_weight_dictionary: Dict[int, int] = dict()

        self.__hypergraph_dictionary: Dict[int, Set[int]] = dict()

        self.__check_files_and_folders()
        self.__create_hypergraph()
        self.__set_static_weights()

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

    def __set_static_weights(self):
        """
        Initialize the static weights
        Variable: node_static_weight_dictionary, hyperedge_static_weight_dictionary
        """

        # Node's weight
        for node in range(self.__number_of_nodes):
            self.__node_static_weight_dictionary[node] = 1

        # Hyperedge's weight
        for hyperedge in self.__variable_set:
            self.__hyperedge_static_weight_dictionary[hyperedge] = 1

    def __check_files_and_folders(self) -> None:
        """
        Check if all necessary files and folders exist.
        If some file is missing, raise an exception (FileIsMissingException).
        If the chosen software is not supported on the system, raise an exception (SoftwareIsNotSupportedOnSystemException).
        """

        # Windows
        if env.is_windows():
            # hMETIS
            if self.__software_enum == hs_enum.HypergraphSoftwareEnum.HMETIS:
                Path(Hypergraph.TEMP_FOLDER_PATH).mkdir(exist_ok=True)

                file_temp = Path(Hypergraph.WIN_PROGRAM_HMETIS_PATH)
                if not file_temp.exists():
                    raise h_exception.FileIsMissingException(Hypergraph.WIN_PROGRAM_HMETIS_PATH)
                return

            raise h_exception.SoftwareIsNotSupportedOnSystemException(self.__software_enum.name)

        # Linux
        elif env.is_linux():
            pass    # TODO

        # Mac
        elif env.is_mac():
            pass    # TODO

        # Undefined
        raise h_exception.SomethingWrongException(f"The function (check_files_and_folders) is not implemented for this OS ({env.get_os().name})!")

    # region hMETIS
    def __get_hypergraph_hmetis_exe(self, clause_id_set: Set[int], ignored_literal_set: Set[int]) -> str:
        # TODO
        pass

    def __get_cut_set_hmetis_exe(self, clause_id_set: Set[int], ignored_literal_set: Set[int]) -> Set[int]:
        # TODO
        pass
    # endregion
    # endregion

    # region Public method
    def get_cut_set(self, clause_id_set: Set[int], ignored_literal_list: List[int]) -> Set[int]:
        """
        Create a hypergraph, where nodes (clauses) are restricted to the clause_id_set and
        hyperedges (variables) are restricted to all variables except those which are in the ignored_literal_list.
        Return a cut set of the hypergraph.
        """

        ignored_literal_set = set()
        for literal in ignored_literal_list:
            variable = abs(literal)
            if variable in self.__variable_set:
                ignored_literal_set.add(variable)
                ignored_literal_set.add(-variable)

        cut_set = set()

        # Windows -> hMETIS.exe
        if env.is_windows():
            cut_set = self.__get_cut_set_hmetis_exe(clause_id_set, ignored_literal_set)

        # TODO Cache

        return cut_set
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
