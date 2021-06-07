# Import
import ctypes
import numpy as np
from typing import List, Union
from compiler.hypergraph_partitioning.patoh_initialize_parameters import PatohInitializeParameters


class PatohData:
    """
    PaToH data representation
    """

    """
    Private int c                   # number of cells of the hypergraph
    Private int n                   # number of nets of the hypergraph
    Private int nconst              # number of constraints
    Private int useFixCells         # pre-assigned cells
    Private ndarray cwghts          # stores the weights of each cell
    Private ndarray nwghts          # stores the cost of each net
    Private ndarray xpins           # stores the beginning index of pins (cells) connected to nets
    Private ndarray pins            # stores the pin-lists of nets
    Private ndarray targetweights   # array with target part weights

    Private ndarray partvec         # stores the part number of each cell belong to
    Private ndarray partweights     # the total part weight of each part
    Private int cut                 # cut size of the solution

    Private PatohInitializeParameters parameters
    """

    def __init__(self, number_of_nodes: int, number_of_hyperedges: int,
                 node_weight_list: List[int], hyperedge_weight_list: List[int],
                 xpins: List[int], pins: List[int], epsilon: Union[float, None]):
        # Input
        self.__c: int = number_of_nodes
        self.__n: int = number_of_hyperedges
        self.__nconst: int = 1
        self.__useFixCells: int = 0  # no partitions assigned
        self.__cwghts: np.ndarray = np.array(node_weight_list, dtype=np.int32)
        self.__nwghts: np.ndarray = np.array(hyperedge_weight_list, dtype=np.int32)
        self.__xpins: np.ndarray = np.array(xpins, dtype=np.int32)
        self.__pins: np.ndarray = np.array(pins, dtype=np.int32)
        self.__targetweights: np.ndarray = np.array([0.5, 0.5], dtype=np.float32)

        # Output
        self.__partvec: np.ndarray = np.array([-1] * self.__c, dtype=np.int32)
        self.__partweights: np.ndarray = np.array([0, 0], dtype=np.int32)
        self.__cut: int = 0
        self.__cut_ctypes = ctypes.c_int(self.__cut)

        # Parameter
        self.__parameters: PatohInitializeParameters = PatohInitializeParameters()
        self.__parameters._k = 2
        self.__parameters.seed = -1  # random seed

        if epsilon is not None:
            self.__parameters.balance = 1
            # self.__parameters.init_imbal = epsilon * 2
            self.__parameters.final_imbal = epsilon

    # region Public method
    def cwghts_ctypes(self) -> ctypes:
        return self.__cwghts.ctypes

    def nwghts_ctypes(self) -> ctypes:
        return self.__nwghts.ctypes

    def xpins_ctypes(self) -> ctypes:
        return self.__xpins.ctypes

    def pins_ctypes(self) -> ctypes:
        return self.__pins.ctypes

    def targetweights_ctypes(self) -> ctypes:
        return self.__targetweights.ctypes

    def partvec_ctypes(self) -> ctypes:
        return self.__partvec.ctypes

    def partvec(self) -> List[int]:
        return self.__partvec.tolist()

    def partweights_ctypes(self) -> ctypes:
        return self.__partweights.ctypes

    def partweights(self) -> List[int]:
        return self.__partweights.tolist()

    def cut_addr(self) -> int:
        return ctypes.addressof(self.__cut_ctypes)

    def parameters_ref(self):
        return ctypes.byref(self.__parameters)
    # endregion

    # region Magic method
    def __str__(self):
        string_temp = "\n".join((f"Number of nodes: {self.__c}",
                                 f"Number of hyperedges: {self.__n}",
                                 f"Node weight list: {self.__cwghts}",
                                 f"Hyperedge weight list: {self.__nwghts}",
                                 f"Xpins: {self.__xpins}",
                                 f"Pins: {self.__pins}"))

        return string_temp
    # endregion

    # region Property
    @property
    def c(self) -> int:
        return self.__c

    @property
    def n(self) -> int:
        return self.__n

    @property
    def nconst(self) -> int:
        return self.__nconst

    @property
    def useFixCells(self) -> int:
        return self.__useFixCells

    @property
    def cut(self) -> int:
        return self.__cut_ctypes.value
    # endregion
