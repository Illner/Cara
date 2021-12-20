# Import
import os
import sys
import pickle
from pathlib import Path
from enum import Enum, unique, IntEnum
from typing import Dict, Tuple, List, Set, Union
from compiler_statistics.statistics import Statistics
from visualization.plot import scatter, boxplot, histogram

# Import enum
import circuit.node.node_type_enum as nt_enum

# Import exception
import exception.cara_exception as ca_exception


root_path = sys.argv[1]
plot_path = sys.argv[2]
file_path = sys.argv[2]


# region Enum
@unique
class RootPathEnum(str, Enum):
    BDMC = fr"{root_path}\BDMC"
    BDMC_RH = fr"{root_path}\BDMC RH"
    BDMC_RH_SD = fr"{root_path}\BDMC RH SD"
    BDMC_MRH = fr"{root_path}\BDMC MRH"
    HP_CACHE = fr"{root_path}\HP cache"
    CARA_CIRCUIT = fr"{root_path}\CaraCircuit"
    IMBALANCE_FACTOR = fr"{root_path}\Imbalance factor"
    DNNF = fr"{root_path}\DNNF"
    TEMP = fr"C:\Users\illner\Desktop\Temp2"


@unique
class DirectorySetEnum(str, Enum):
    all = None
    bmc = "bmc"
    BN = "BN"
    circuit = "circuit"
    Configuration = "Configuration"
    Handmade = "Handmade"
    Planning = "Planning"
    qif = "qif"
    random = "random"


@unique
class ExperimentEnum(str, Enum):
    # BDMC
    BDMC_LIMIT_250 = "250"
    BDMC_LIMIT_500 = "500"
    BDMC_LIMIT_1000 = "1000"
    BDMC_LIMIT_1500 = "1500"
    BDMC_D4 = "D4"
    BDMC_JW_TS_1_EXTENDED = "JW-TS, extended, 0.1"
    BDMC_JW_TS_25_EXTENDED = "JW-TS, extended, 0.25"
    BDMC_JW_TS_25 = "JW-TS, 0.25"
    BDMC_DLCS_DLIS_1_EXTENDED = "DLCS-DLIS, extended, 0.1"
    BDMC_DLCS_DLIS_25_EXTENDED = "DLCS-DLIS, extended, 0.25"
    BDMC_DLCS_DLIS_25 = "DLCS-DLIS, 0.25"
    BDMC_VSADS_1_EXTENDED = "VSADS, d4, extended, 0.1"
    BDMC_VSADS_25_EXTENDED = "VSADS, d4, extended, 0.25"
    BDMC_VSADS_25 = "VSADS, d4, 0.25"
    BDMC_CLAUSE_REDUCTION_1 = "Clause reduction, 0.1"
    BDMC_CLAUSE_REDUCTION_25 = "Clause reduction, 0.25"
    BDMC_CLAUSE_REDUCTION_25_WITHOUT_GAMMA_0 = "Clause reduction, 0.25, without gamma_0"
    BDMC_WEIGHTED_BINARIES_1 = "Weighted binaries, 0.1"
    BDMC_WEIGHTED_BINARIES_25 = "Weighted binaries, 0.25"
    BDMC_WEIGHTED_BINARIES_25_WITHOUT_GAMMA_0 = "Weighted binaries, 0.25, without gamma_0"

    # BDMC RH
    BDMC_RH_D4 = "D4 (BDMC RH)"
    BDMC_RH_VSADS = "VSADS"
    BDMC_RH_DLCS_DLIS_A_T_C_P = "DLCS-DLIS (a, t, c, p)"
    BDMC_RH_DLCS_DLIS_A_T_C_nP = "DLCS-DLIS (a, t, c, -p)"
    BDMC_RH_DLCS_DLIS_A_T_nC_P = "DLCS-DLIS (a, t, -c, p)"
    BDMC_RH_DLCS_DLIS_A_T_nC_nP = "DLCS-DLIS (a, t, -c, -p)"
    BDMC_RH_DLCS_DLIS_A_nT_C_P = "DLCS-DLIS (a, -t, c, p)"
    BDMC_RH_DLCS_DLIS_A_nT_C_nP = "DLCS-DLIS (a, -t, c, -p)"
    BDMC_RH_DLCS_DLIS_nA_C_P = "DLCS-DLIS (-a, c, p)"
    BDMC_RH_DLCS_DLIS_nA_C_P_nD = "DLCS-DLIS (-a, c, p, d_d)"
    BDMC_RH_VSADS_A_T_C_P = "VSADS (a, t, c, p)"
    BDMC_RH_JW_TS_nA_C_P = "JW-TS (-a, c, p)"
    BDMC_RH_VSADS_nA_C_P = "VSADS (-a, c, p)"
    BDMC_RH_DLCS_DLIS_nA_nC_P = "DLCS-DLIS (-a, -c, p)"
    BDMC_RH_VSADS_nA_nC_P = "VSADS (-a, -c, p)"
    BDMC_RH_JW_TS_nA_nC_P = "JW-TS (-a, -c, p)"
    BDMC_RH_DLCS_DLIS_nA_C_P_nEXT = "DLCS-DLIS (-a, c, p, -ext)"
    BDMC_RH_DLCS_DLIS_nA_nC_P_nEXT = "DLCS-DLIS (-a, -c, p, -ext)"
    BDMC_RH_VSADS_nA_C_P_nEXT = "VSADS (-a, c, p, -ext)"
    BDMC_RH_VSADS_nA_nC_P_nEXT = "VSADS (-a, -c, p, -ext)"
    BDMC_RH_JW_TS_nA_C_P_nEXT = "JW-TS (-a, c, p, -ext)"
    BDMC_RH_JW_TS_nA_nC_P_nEXT = "JW-TS (-a, -c, p, -ext)"

    # BDMC RH SD
    BDMC_RH_SD_D4 = "D4 (BDMC RH SD)"
    BDMC_RH_SD_DLCS_DLIS_nA_C_P_nEXT = "SD DLCS-DLIS (-a, c, p, -ext)"
    BDMC_RH_SD_DLCS_DLIS_nA_nC_P_nEXT = "SD DLCS-DLIS (-a, -c, p, -ext)"

    # BDMC MRH
    BDMC_MRH_D4 = "D4 (BDMC MRH)"
    BDMC_MRH_VSADS_nA_C_P = "VSADS (-a, c, p) (BDMC MRH)"
    BDMC_MRH_DLCS_DLIS_nA_C_P = "DLCS-DLIS (-a, c, p) (BDMC MRH)"
    BDMC_MRH_VSADS_E_C_P_HF = "VSADS (e, c, p, HF)"
    BDMC_MRH_VSADS_E_C_P_RDHF_2 = "VSADS (e, c, p, RDHF_2)"
    BDMC_MRH_VSADS_E_C_P_SLWHF = "VSADS (e, c, p, SLWHF)"
    BDMC_MRH_VSADS_E_C_P_SILWHF = "VSADS (e, c, p, SILWHF)"
    BDMC_MRH_DLCS_DLIS_E_C_P_RDHF_2 = "DLCS-DLIS (e, c, p, RDHF_2)"
    BDMC_MRH_DLCS_DLIS_E_C_P_RDHF_4 = "DLCS-DLIS (e, c, p, RDHF_4)"
    BDMC_MRH_DLCS_DLIS_E_C_P_LWHF = "DLCS-DLIS (e, c, p, LWHF)"
    BDMC_MRH_DLCS_DLIS_E_C_P_SLWHF = "DLCS-DLIS (e, c, p, SLWHF)"
    BDMC_MRH_DLCS_DLIS_E_C_P_ILWHF = "DLCS-DLIS (e, c, p, ILWHF)"
    BDMC_MRH_DLCS_DLIS_E_C_P_SILWHF = "DLCS-DLIS (e, c, p, SILWHF)"
    BDMC_MRH_DLCS_DLIS_E_C_P_HF = "DLCS-DLIS (e, c, p, HF)"
    BDMC_MRH_DLCS_DLIS_E_C_P_VC = "DLCS-DLIS (e, c, p, VC)"
    BDMC_MRH_DLCS_DLIS_E_C_P_RDVC_2 = "DLCS-DLIS (e, c, p, RDVC_2)"

    # HP cache
    HP_CACHE_NONE = "NONE"
    HP_CACHE_ISOMORFISM_250 = "ISOMORFISM 250"
    HP_CACHE_ISOMORFISM_250_NO_MOC = "ISOMORFISM 250 (no moc)"
    HP_CACHE_ISOMORFISM_500 = "ISOMORFISM 500"
    HP_CACHE_ISOMORFISM_500_NO_MOC = "ISOMORFISM 500 (no moc)"
    HP_CACHE_ISOMORFISM_1000 = "ISOMORFISM 1000"
    HP_CACHE_ISOMORFISM_1000_NO_MOC = "ISOMORFISM 1000 (no moc)"
    HP_CACHE_ISOMORFISM_1500 = "ISOMORFISM 1500"
    HP_CACHE_ISOMORFISM_1500_NO_MOC = "ISOMORFISM 1500 (no moc)"
    HP_CACHE_ISOMORFISM_VARIANCE_250 = "ISOMORFISM_VARIANCE 250"
    HP_CACHE_ISOMORFISM_VARIANCE_250_NO_MOC = "ISOMORFISM_VARIANCE 250 (no moc)"
    HP_CACHE_ISOMORFISM_VARIANCE_500 = "ISOMORFISM_VARIANCE 500"
    HP_CACHE_ISOMORFISM_VARIANCE_500_NO_MOC = "ISOMORFISM_VARIANCE 500 (no moc)"
    HP_CACHE_ISOMORFISM_VARIANCE_1000 = "ISOMORFISM_VARIANCE 1000"
    HP_CACHE_ISOMORFISM_VARIANCE_1000_NO_MOC = "ISOMORFISM_VARIANCE 1000 (no moc)"
    HP_CACHE_ISOMORFISM_VARIANCE_1500 = "ISOMORFISM_VARIANCE 1500"
    HP_CACHE_ISOMORFISM_VARIANCE_1500_NO_MOC = "ISOMORFISM_VARIANCE 1500 (no moc)"

    # CaraCircuit
    CARA_CIRCUIT_D4 = "D4 (CaraCircuit)"
    CARA_CIRCUIT_LIMIT_0 = "Limit 0"
    CARA_CIRCUIT_LIMIT_0_MOC = "Limit 0 (moc)"
    CARA_CIRCUIT_LIMIT_25 = "Limit 25"
    CARA_CIRCUIT_LIMIT_50 = "Limit 50"
    CARA_CIRCUIT_LIMIT_100 = "Limit 100"
    CARA_CIRCUIT_LIMIT_250 = "Limit 250"
    CARA_CIRCUIT_LIMIT_500 = "Limit 500"
    CARA_CIRCUIT_LIMIT_0_1 = "Limit 0 (0.1)"
    CARA_CIRCUIT_LIMIT_0_MOC_1 = "Limit 0 (moc) (0.1)"

    # Imbalance factor
    IMBALANCE_FACTOR_1 = "0.1"
    IMBALANCE_FACTOR_1_QUALITY = "0.1 PaToH quality"
    IMBALANCE_FACTOR_1_SPEED = "0.1 PaToH speed"
    IMBALANCE_FACTOR_25 = "0.25"
    IMBALANCE_FACTOR_25_QUALITY = "0.25 PaToH quality"
    IMBALANCE_FACTOR_25_SPEED = "0.25 PaToH speed"
    IMBALANCE_FACTOR_4 = "0.4"
    IMBALANCE_FACTOR_4_QUALITY = "0.4 PaToH quality"
    IMBALANCE_FACTOR_4_SPEED = "0.4 PaToH speed"

    # DNNF
    DNNF_D4 = "D4 (DNNF)"
    DNNF_COPY = "CaraCircuit (copy)"
    DNNF_CLAUSE_REDUCTION = "Clause reduction"
    DNNF_CLAUSE_REDUCTION_EXT = "Clause reduction (ext)"
    DNNF_WEIGHTED_BINARIES = "Weighted binaries"
    DNNF_WEIGHTED_BINARIES_EXT = "Weighted binaries (ext)"

    # Temp
    TEMP_D4 = "D4 (Temp)"
    TEMP_LIMIT_0 = "Temp limit 0"
    TEMP_LIMIT_50 = "Temp limit 50"
    TEMP_LIMIT_100 = "Temp limit 100"
    TEMP = "Temp"


@unique
class PlotEnum(IntEnum):
    BOXPLOT = 1
    SCATTER = 2
    HISTOGRAM = 3


@unique
class FunctionEnum(str, Enum):
    MANUAL = ""

    # Circuit
    CIRCUIT_SIZE = "Circuit size"
    CIRCUIT_NUMBER_OF_EDGES = "Number of edges"
    CIRCUIT_NUMBER_OF_NODES = "Number of nodes"
    CIRCUIT_NUMBER_OF_VARIABLES = "Number of variables"
    CIRCUIT_NUMBER_OF_RH_LEAVES = "Number of renamable Horn formulae/leaves"
    CIRCUIT_NUMBER_OF_TWO_CNF_LEAVES = "Number of 2-CNF formulae/leaves"
    CIRCUIT_NUMBER_OF_RH_AND_TWO_CNF_LEAVES = "Number of nontrivial leaves (renamable Horn + 2-CNF)"
    COMPILATION_TIME = "Compilation time [ms]"

    # Renamable Horn formulae, 2-CNF formulae and implication graph
    RH_RECOGNITION = "Recognition of renamable Horn formulae [%]"
    TWO_CNF_RECOGNITION = "Recognition of 2-CNF formulae [%]"
    TOTAL_FORMULA_LENGTH_RH = "Total length of all renamable Horn formulae"
    AVERAGE_FORMULA_LENGTH_RH = "Average length of a renamable Horn formula"
    TOTAL_FORMULA_LENGTH_TWO_CNF = "Total length of all 2-CNF formulae"
    AVERAGE_FORMULA_LENGTH_TWO_CNF = "Average length of a 2-CNF formula"
    TOTAL_FORMULA_LENGTH_RH_AND_TWO_CNF = "Total length of all renamable Horn formulae and 2-CNF formulae"
    AVERAGE_FORMULA_LENGTH_RH_AND_TWO_CNF = "Average length of a renamable Horn formula and 2-CNF formula"
    TOTAL_TIME_CREATE_IMPLICATION_GRAPH = "Total time spent on creating all implication graphs [ms]"
    AVERAGE_TIME_CREATE_IMPLICATION_GRAPH = "Average time spent on creating an implication graph [ms]"
    TOTAL_NUMBER_OF_CONFLICT_VARIABLES_IMPLICATION_GRAPH = "Total number of conflict variables in all implication graphs"
    AVERAGE_NUMBER_OF_CONFLICT_VARIABLES_IMPLICATION_GRAPH = "Average number of conflict variables in an implication graph"

    # Hypergraph and cut set
    TOTAL_CUT_SET_SIZE = "Total size of all cut sets"
    AVERAGE_CUT_SET_SIZE = "Average size of a cut set"
    HYPERGRAPH_CACHING_HIT = "Hypergraph caching hit [%]"
    TOTAL_TIME_GET_CUT_SET = "Total time spent on getting all cut sets [ms]"
    AVERAGE_TIME_GET_CUT_SET = "Average time spent on getting a cut set [ms]"
    TOTAL_NUMBER_OF_HYPEREDGES_HYPERGRAPH = "Total number of hyperedges in all hypergraphs"
    AVERAGE_NUMBER_OF_HYPEREDGES_HYPERGRAPH = "Average number of hyperedges in a hypergraph"
    TOTAL_NUMBER_OF_NODES_HYPERGRAPH = "Total number of nodes in all hypergraphs"
    AVERAGE_NUMBER_OF_NODES_HYPERGRAPH = "Average number of nodes in a hypergraph"
    RATIO_LOG_CUT_SET_SIZE_AND_LOG_NUMBER_OF_HYPEREDGES_HYPERGRAPH = "log(size of a cut set) / log(number of hyperedges)"

    # Component caching
    TOTAL_TIME_GENERATE_KEY_COMPONENT_CACHING = "Total time spent on generating all keys for component caching [ms]"
    AVERAGE_TIME_GENERATE_KEY_COMPONENT_CACHING = "Average time spent on generating a key for component caching [ms]"
    COMPONENT_CACHING_HIT = "Component caching hit [%]"
    TOTAL_FORMULA_LENGTH_COMPONENT_CACHING = "Total length of all formulae that were cached"
    AVERAGE_FORMULA_LENGTH_COMPONENT_CACHING = "Average length of a formula that was cached"
    TOTAL_FORMULA_LENGTH_MAPPING_COMPONENT_CACHING = "Total length of all formulae that were cached \n using a mapping function"
    AVERAGE_FORMULA_LENGTH_MAPPING_COMPONENT_CACHING = "Average length of a formula that was cached \n using a mapping function"

    # Copy
    RATIO_COPY_CIRCUIT_AND_COMPILATION_TIME = "Total time spent on copying circuits / compilation time [%]"
    TOTAL_COPIED_CIRCUIT_SIZE = "Total size of copied circuits"
    AVERAGE_COPIED_CIRCUIT_SIZE = "Average size of a copied circuit"
    TOTAL_FORMULA_LENGTH_COPIED_CIRCUIT = "Total length of all formulae for which copying was used"
    AVERAGE_FORMULA_LENGTH_COPIED_CIRCUIT = "Average length of a formula for which copying was used"

    # LP formulation
    TOTAL_TIME_CREATE_LP_FORMULATION = "Total time spent on creating all LP formulations [ms] \n (LP formulation)"
    AVERAGE_TIME_CREATE_LP_FORMULATION = "Average time spent on creating an LP formulation [ms] \n (LP formulation)"
    TOTAL_TIME_SOLVE_LP_FORMULATION = "Total time spent on solving all LP formulations [ms] \n (LP formulation)"
    AVERAGE_TIME_SOLVE_LP_FORMULATION = "Average time spent on solving an LP formulation [ms] \n (LP formulation)"
    HORN_CLAUSE_LENGTH_LP_FORMULATION = "Average length of a Horn clause after switching \n (LP formulation)"
    RATIO_NUMBER_OF_HORN_CLAUSES_AND_NUMBER_OF_CLAUSES_LP_FORMULATION = "Number of Horn clauses after switching / number of clauses [%] \n (LP formulation)"
    RATIO_NUMBER_OF_SWITCHED_VARIABLES_AND_NUMBER_OF_VARIABLES_LP_FORMULATION = "Number of switched variables / number of variables [%] \n (LP formulation)"

    # Others
    TOTAL_NUMBER_OF_IMPLIED_LITERALS = "Total number of implied literals"
    AVERAGE_NUMBER_OF_IMPLIED_LITERALS = "Average number of implied literals"
    NUMBER_OF_SPLITS = "Number of splits"
    TOTAL_NUMBER_OF_DECISION_VARIABLES = "Total number of decision variables"
    AVERAGE_NUMBER_OF_DECISION_VARIABLES = "Average size of a set with decision variables"
    MAX_NUMBER_OF_DECISION_VARIABLES = "Max size of a set with decision variables"
    NUMBER_OF_DECISION_NODES = "Number of decision nodes"
    NUMBER_OF_EXTENDED_DECISION_NODES = "Number of extended decision nodes"
    RATIO_EXTENDED_DECISION_NODES_AND_ALL_DECISION_NODES = "Number of extended decision nodes / all decision nodes [%]"
    RECOMPUTATION_CUT_SET = "Recomputation of cut sets [%]"
    RATIO_GENERATE_KEY_COMPONENT_CACHING_TIME_AND_COMPILATION_TIME = "Total time spent on generating all keys for component \n caching / compilation time [%]"
    RATIO_IMPLICATION_GRAPH_TIME_AND_COMPILATION_TIME = "Total time spent on creating all implication \n graphs / compilation time [%]"
# endregion

#########################
##### Configuration #####
#########################

experiment_path: RootPathEnum = RootPathEnum.BDMC_RH_SD

title: str = ""
plot: PlotEnum = PlotEnum.SCATTER
function: FunctionEnum = FunctionEnum.COMPILATION_TIME
directory_set: DirectorySetEnum = DirectorySetEnum.all

none_value: float = 0   # 10**10
use_uncompiled: bool = False

plot_name: Union[str, None] = None
file_name: Union[str, None] = None

###################
##### SCATTER #####
###################

directory_name_1: ExperimentEnum = ExperimentEnum.BDMC_RH_SD_D4
directory_name_2: ExperimentEnum = ExperimentEnum.BDMC_RH_SD_DLCS_DLIS_nA_nC_P_nEXT

x_label: str = f""
y_label: str = f""

log_scale: bool = False
set_together: bool = False
use_point_label: bool = False

##############################
##### BOXPLOT, HISTOGRAM #####
##############################

directory_name_list: List[ExperimentEnum] = [ExperimentEnum.BDMC_RH_SD_DLCS_DLIS_nA_nC_P_nEXT,
                                             ExperimentEnum.BDMC_RH_SD_DLCS_DLIS_nA_C_P_nEXT]

label_prefix: str = ""
label_list: Union[List[List[str]], None] = [["d-BDMC RH SD \n DLCS-DLIS \n (-a, -c, p, -ext)"],
                                            ["d-BDMC RH SD \n DLCS-DLIS \n (-a, c, p, -ext)"]]
# BOXPLOT
showfliers: bool = False

# HISTOGRAM
number_of_bins: int = 10

################################
##### End of configuration #####
################################

# region function
def get_value_temp(statistics: Statistics) -> Union[float, None]:
    # MANUAL
    if function == FunctionEnum.MANUAL:
        raise NotImplementedError()

    # CIRCUIT_SIZE
    if function == FunctionEnum.CIRCUIT_SIZE:
        return statistics.size

    # CIRCUIT_NUMBER_OF_EDGES
    if function == FunctionEnum.CIRCUIT_NUMBER_OF_EDGES:
        try:
            return statistics.number_of_edges
        except AttributeError:
            return statistics.size

    # CIRCUIT_NUMBER_OF_NODES
    if function == FunctionEnum.CIRCUIT_NUMBER_OF_NODES:
        return statistics.number_of_nodes

    # CIRCUIT_NUMBER_OF_VARIABLES
    if function == FunctionEnum.CIRCUIT_NUMBER_OF_VARIABLES:
        return statistics.number_of_variables

    # NUMBER_OF_SPLITS
    if function == FunctionEnum.NUMBER_OF_SPLITS:
        return statistics.component_statistics.split.sum_count

    # TOTAL_CUT_SET_SIZE
    if function == FunctionEnum.TOTAL_CUT_SET_SIZE:
        return statistics.hypergraph_partitioning_statistics.cut_set_size.sum_count

    # AVERAGE_CUT_SET_SIZE
    if function == FunctionEnum.AVERAGE_CUT_SET_SIZE:
        return statistics.hypergraph_partitioning_statistics.cut_set_size.average_count

    # COMPILATION_TIME
    if function == FunctionEnum.COMPILATION_TIME:
        return statistics.compiler_statistics.create_circuit.average_time

    # CIRCUIT_NUMBER_OF_RH_LEAVES
    if function == FunctionEnum.CIRCUIT_NUMBER_OF_RH_LEAVES:
        return statistics.get_node_type_counter(nt_enum.NodeTypeEnum.RENAMABLE_HORN_CNF)

    # CIRCUIT_NUMBER_OF_TWO_CNF_LEAVES
    if function == FunctionEnum.CIRCUIT_NUMBER_OF_TWO_CNF_LEAVES:
        return statistics.get_node_type_counter(nt_enum.NodeTypeEnum.TWO_CNF)

    # CIRCUIT_NUMBER_OF_RH_AND_TWO_CNF_LEAVES
    if function == FunctionEnum.CIRCUIT_NUMBER_OF_RH_AND_TWO_CNF_LEAVES:
        return statistics.get_node_type_counter(nt_enum.NodeTypeEnum.RENAMABLE_HORN_CNF) + statistics.get_node_type_counter(nt_enum.NodeTypeEnum.TWO_CNF)

    # RH_RECOGNITION
    if function == FunctionEnum.RH_RECOGNITION:
        return statistics.incidence_graph_statistics.renamable_horn_formula_ratio.average_count

    # TWO_CNF_RECOGNITION
    if function == FunctionEnum.TWO_CNF_RECOGNITION:
        return statistics.incidence_graph_statistics.two_cnf_ratio.average_count

    # TOTAL_TIME_CREATE_IMPLICATION_GRAPH
    if function == FunctionEnum.TOTAL_TIME_CREATE_IMPLICATION_GRAPH:
        return statistics.incidence_graph_statistics.renamable_horn_formula_recognition_implication_graph_check.sum_time

    # AVERAGE_TIME_CREATE_IMPLICATION_GRAPH
    if function == FunctionEnum.AVERAGE_TIME_CREATE_IMPLICATION_GRAPH:
        return statistics.incidence_graph_statistics.renamable_horn_formula_recognition_implication_graph_check.average_time

    # TOTAL_NUMBER_OF_CONFLICT_VARIABLES_IMPLICATION_GRAPH
    if function == FunctionEnum.TOTAL_NUMBER_OF_CONFLICT_VARIABLES_IMPLICATION_GRAPH:
        return statistics.incidence_graph_statistics.implication_graph_conflict_variables.sum_count

    # AVERAGE_NUMBER_OF_CONFLICT_VARIABLES_IMPLICATION_GRAPH
    if function == FunctionEnum.AVERAGE_NUMBER_OF_CONFLICT_VARIABLES_IMPLICATION_GRAPH:
        return statistics.incidence_graph_statistics.implication_graph_conflict_variables.average_count

    # HYPERGRAPH_CACHING_HIT
    if function == FunctionEnum.HYPERGRAPH_CACHING_HIT:
        return statistics.hypergraph_partitioning_statistics.cache_hit.average_count

    # TOTAL_TIME_GET_CUT_SET
    if function == FunctionEnum.TOTAL_TIME_GET_CUT_SET:
        return statistics.hypergraph_partitioning_statistics.get_cut_set.sum_time

    # AVERAGE_TIME_GET_CUT_SET
    if function == FunctionEnum.AVERAGE_TIME_GET_CUT_SET:
        return statistics.hypergraph_partitioning_statistics.get_cut_set.average_time

    # TOTAL_TIME_GENERATE_KEY_COMPONENT_CACHING
    if function == FunctionEnum.TOTAL_TIME_GENERATE_KEY_COMPONENT_CACHING:
        return statistics.hypergraph_partitioning_statistics.generate_key_cache.sum_time

    # AVERAGE_TIME_GENERATE_KEY_COMPONENT_CACHING
    if function == FunctionEnum.AVERAGE_TIME_GENERATE_KEY_COMPONENT_CACHING:
        return statistics.hypergraph_partitioning_statistics.generate_key_cache.average_time

    # TOTAL_NUMBER_OF_IMPLIED_LITERALS
    if function == FunctionEnum.TOTAL_NUMBER_OF_IMPLIED_LITERALS:
        return statistics.component_statistics.implied_literal.sum_count

    # AVERAGE_NUMBER_OF_IMPLIED_LITERALS
    if function == FunctionEnum.AVERAGE_NUMBER_OF_IMPLIED_LITERALS:
        return statistics.component_statistics.implied_literal.average_count

    # COMPONENT_CACHING_HIT
    if function == FunctionEnum.COMPONENT_CACHING_HIT:
        return statistics.component_statistics.component_caching_after_hit.average_count

    # TOTAL_FORMULA_LENGTH_COMPONENT_CACHING
    if function == FunctionEnum.TOTAL_FORMULA_LENGTH_COMPONENT_CACHING:
        return statistics.component_statistics.component_caching_after_formula_length.sum_count

    # AVERAGE_FORMULA_LENGTH_COMPONENT_CACHING
    if function == FunctionEnum.AVERAGE_FORMULA_LENGTH_COMPONENT_CACHING:
        return statistics.component_statistics.component_caching_after_formula_length.average_count

    # TOTAL_FORMULA_LENGTH_MAPPING_COMPONENT_CACHING
    if function == FunctionEnum.TOTAL_FORMULA_LENGTH_MAPPING_COMPONENT_CACHING:
        return statistics.component_statistics.component_caching_after_cara_mapping_length.sum_count

    # AVERAGE_FORMULA_LENGTH_MAPPING_COMPONENT_CACHING
    if function == FunctionEnum.AVERAGE_FORMULA_LENGTH_MAPPING_COMPONENT_CACHING:
        return statistics.component_statistics.component_caching_after_cara_mapping_length.average_count

    # TOTAL_NUMBER_OF_DECISION_VARIABLES
    if function == FunctionEnum.TOTAL_NUMBER_OF_DECISION_VARIABLES:
        return statistics.component_statistics.decision_variable_size.sum_count

    # AVERAGE_NUMBER_OF_DECISION_VARIABLES
    if function == FunctionEnum.AVERAGE_NUMBER_OF_DECISION_VARIABLES:
        return statistics.component_statistics.decision_variable_size.average_count

    # MAX_NUMBER_OF_DECISION_VARIABLES
    if function == FunctionEnum.MAX_NUMBER_OF_DECISION_VARIABLES:
        return statistics.component_statistics.decision_variable_size.max_count

    # NUMBER_OF_DECISION_NODES
    if function == FunctionEnum.NUMBER_OF_DECISION_NODES:
        return statistics.component_statistics.decision_node.sum_count

    # NUMBER_OF_EXTENDED_DECISION_NODES
    if function == FunctionEnum.NUMBER_OF_EXTENDED_DECISION_NODES:
        return statistics.component_statistics.extended_decision_node.sum_count

    # RATIO_EXTENDED_DECISION_NODES_AND_ALL_DECISION_NODES
    if function == FunctionEnum.RATIO_EXTENDED_DECISION_NODES_AND_ALL_DECISION_NODES:
        decision_nodes = statistics.component_statistics.decision_node.sum_count
        extended_decision_nodes = statistics.component_statistics.extended_decision_node.sum_count

        if (decision_nodes + extended_decision_nodes) == 0:
            return 0

        return extended_decision_nodes / (extended_decision_nodes + decision_nodes)

    # RECOMPUTATION_CUT_SET
    if function == FunctionEnum.RECOMPUTATION_CUT_SET:
        return statistics.component_statistics.recompute_cut_set.average_count

    # TOTAL_FORMULA_LENGTH_RH
    if function == FunctionEnum.TOTAL_FORMULA_LENGTH_RH:
        return statistics.component_statistics.renamable_horn_cnf_formula_length.sum_count

    # AVERAGE_FORMULA_LENGTH_RH
    if function == FunctionEnum.AVERAGE_FORMULA_LENGTH_RH:
        return statistics.component_statistics.renamable_horn_cnf_formula_length.average_count

    # TOTAL_FORMULA_LENGTH_TWO_CNF
    if function == FunctionEnum.TOTAL_FORMULA_LENGTH_TWO_CNF:
        return statistics.component_statistics.two_cnf_formula_length.sum_count

    # AVERAGE_FORMULA_LENGTH_TWO_CNF
    if function == FunctionEnum.AVERAGE_FORMULA_LENGTH_TWO_CNF:
        return statistics.component_statistics.two_cnf_formula_length.average_count

    # TOTAL_FORMULA_LENGTH_RH_AND_TWO_CNF
    if function == FunctionEnum.TOTAL_FORMULA_LENGTH_RH_AND_TWO_CNF:
        return statistics.component_statistics.renamable_horn_cnf_formula_length.sum_count + statistics.component_statistics.two_cnf_formula_length.sum_count

    # AVERAGE_FORMULA_LENGTH_RH_AND_TWO_CNF
    if function == FunctionEnum.AVERAGE_FORMULA_LENGTH_RH_AND_TWO_CNF:
        two_cnf_number = statistics.component_statistics.two_cnf_formula_length.number_of_calls
        two_cnf_length = statistics.component_statistics.two_cnf_formula_length.sum_count
        two_cnf_length = 0 if two_cnf_length is None else two_cnf_length

        horn_cnf_number = statistics.component_statistics.renamable_horn_cnf_formula_length.number_of_calls
        horn_cnf_length = statistics.component_statistics.renamable_horn_cnf_formula_length.sum_count
        horn_cnf_length = 0 if horn_cnf_length is None else horn_cnf_length

        if (two_cnf_number + horn_cnf_number) == 0:
            return 0

        return (two_cnf_length + horn_cnf_length) / (two_cnf_number + horn_cnf_number)

    # RATIO_GENERATE_KEY_COMPONENT_CACHING_TIME_AND_COMPILATION_TIME
    if function == FunctionEnum.RATIO_GENERATE_KEY_COMPONENT_CACHING_TIME_AND_COMPILATION_TIME:
        return statistics.component_statistics.component_caching_after_generate_key.sum_time / statistics.compiler_statistics.create_circuit.sum_time

    # RATIO_IMPLICATION_GRAPH_TIME_AND_COMPILATION_TIME
    if function == FunctionEnum.RATIO_IMPLICATION_GRAPH_TIME_AND_COMPILATION_TIME:
        return statistics.incidence_graph_statistics.renamable_horn_formula_recognition_implication_graph_check.sum_time / statistics.compiler_statistics.create_circuit.sum_time

    # TOTAL_NUMBER_OF_HYPEREDGES_HYPERGRAPH
    if function == FunctionEnum.TOTAL_NUMBER_OF_HYPEREDGES_HYPERGRAPH:
        return statistics.hypergraph_partitioning_statistics.hypergraph_number_of_hyperedges.sum_count

    # AVERAGE_NUMBER_OF_HYPEREDGES_HYPERGRAPH
    if function == FunctionEnum.AVERAGE_NUMBER_OF_HYPEREDGES_HYPERGRAPH:
        return statistics.hypergraph_partitioning_statistics.hypergraph_number_of_hyperedges.average_count

    # TOTAL_NUMBER_OF_NODES_HYPERGRAPH
    if function == FunctionEnum.TOTAL_NUMBER_OF_NODES_HYPERGRAPH:
        return statistics.hypergraph_partitioning_statistics.hypergraph_number_of_nodes.sum_count

    # AVERAGE_NUMBER_OF_NODES_HYPERGRAPH
    if function == FunctionEnum.AVERAGE_NUMBER_OF_NODES_HYPERGRAPH:
        return statistics.hypergraph_partitioning_statistics.hypergraph_number_of_nodes.average_count

    # RATIO_LOG_CUT_SET_SIZE_AND_LOG_NUMBER_OF_HYPEREDGES_HYPERGRAPH
    if function == FunctionEnum.RATIO_LOG_CUT_SET_SIZE_AND_LOG_NUMBER_OF_HYPEREDGES_HYPERGRAPH:
        return statistics.hypergraph_partitioning_statistics.ratio_log_cut_set_size_and_log_number_of_hyperedges.average_count

    # RATIO_COPY_CIRCUIT_AND_COMPILATION_TIME
    if function == FunctionEnum.RATIO_COPY_CIRCUIT_AND_COMPILATION_TIME:
        return statistics.component_statistics.copying_circuits_after.sum_time / statistics.compiler_statistics.create_circuit.sum_time

    # TOTAL_COPIED_CIRCUIT_SIZE
    if function == FunctionEnum.TOTAL_COPIED_CIRCUIT_SIZE:
        return statistics.component_statistics.copying_circuits_after_size.sum_count

    # AVERAGE_COPIED_CIRCUIT_SIZE
    if function == FunctionEnum.AVERAGE_COPIED_CIRCUIT_SIZE:
        return statistics.component_statistics.copying_circuits_after_size.average_count

    # TOTAL_FORMULA_LENGTH_COPIED_CIRCUIT
    if function == FunctionEnum.TOTAL_FORMULA_LENGTH_COPIED_CIRCUIT:
        return statistics.component_statistics.copying_circuits_after_formula_length.sum_count

    # AVERAGE_FORMULA_LENGTH_COPIED_CIRCUIT
    if function == FunctionEnum.AVERAGE_FORMULA_LENGTH_COPIED_CIRCUIT:
        return statistics.component_statistics.copying_circuits_after_formula_length.average_count

    # TOTAL_TIME_CREATE_LP_FORMULATION
    if function == FunctionEnum.TOTAL_TIME_CREATE_LP_FORMULATION:
        return statistics.renamable_horn_formula_lp_formulation_statistics.create_lp_formulation.sum_time

    # AVERAGE_TIME_CREATE_LP_FORMULATION
    if function == FunctionEnum.AVERAGE_TIME_CREATE_LP_FORMULATION:
        return statistics.renamable_horn_formula_lp_formulation_statistics.create_lp_formulation.average_time

    # TOTAL_TIME_SOLVE_LP_FORMULATION
    if function == FunctionEnum.TOTAL_TIME_SOLVE_LP_FORMULATION:
        return statistics.renamable_horn_formula_lp_formulation_statistics.solve_lp_problem.sum_time

    # AVERAGE_TIME_SOLVE_LP_FORMULATION
    if function == FunctionEnum.AVERAGE_TIME_SOLVE_LP_FORMULATION:
        return statistics.renamable_horn_formula_lp_formulation_statistics.solve_lp_problem.average_time

    # HORN_CLAUSE_LENGTH_LP_FORMULATION
    if function == FunctionEnum.HORN_CLAUSE_LENGTH_LP_FORMULATION:
        return statistics.renamable_horn_formula_lp_formulation_statistics.horn_clauses_after_switching_length.average_count

    # RATIO_NUMBER_OF_SWITCHED_VARIABLES_AND_NUMBER_OF_VARIABLES_LP_FORMULATION
    if function == FunctionEnum.RATIO_NUMBER_OF_SWITCHED_VARIABLES_AND_NUMBER_OF_VARIABLES_LP_FORMULATION:
        return statistics.renamable_horn_formula_lp_formulation_statistics.switching_average.average_count

    # RATIO_NUMBER_OF_HORN_CLAUSES_AND_NUMBER_OF_CLAUSES_LP_FORMULATION
    if function == FunctionEnum.RATIO_NUMBER_OF_HORN_CLAUSES_AND_NUMBER_OF_CLAUSES_LP_FORMULATION:
        return statistics.renamable_horn_formula_lp_formulation_statistics.horn_clauses_after_switching_average.average_count

    raise ca_exception.FunctionNotImplementedException("get_value_temp",
                                                       f"this type of function ({function.name}) is not implemented")


def get_statistics(directory_name: str) -> Tuple[Dict[str, Dict[str, Statistics]], Dict[str, Set[str]], Set[str]]:
    path = Path(os.path.join(experiment_path, directory_name))

    uncompiled_set: Set[str] = set()
    uncompiled_dictionary: Dict[str, Set[str]] = dict()
    experiment_dictionary: Dict[str, Dict[str, Statistics]] = dict()

    for set_directory in os.listdir(path):
        path_temp = Path(os.path.join(path, set_directory))

        uncompiled_dictionary[set_directory] = set()
        experiment_dictionary[set_directory] = dict()

        for experiment_directory in os.listdir(path_temp):
            statistics_path_temp = Path(os.path.join(path_temp, experiment_directory, "statistics.pkl"))

            with open(statistics_path_temp, 'rb') as file:
                statistics = pickle.load(file)

            if not statistics.compiled:
                uncompiled_set.add(experiment_directory)
                uncompiled_dictionary[set_directory].add(experiment_directory)

            experiment_dictionary[set_directory][experiment_directory] = statistics

    return experiment_dictionary, uncompiled_dictionary, uncompiled_set


def get_value(statistics: Statistics):
    value = get_value_temp(statistics)

    if value is None:
        return none_value

    if percent:
        return 100 * value

    return value


def generate_data(dictionary_1: Dict[str, Dict[str, Statistics]], dictionary_2: Dict[str, Dict[str, Statistics]]) -> \
        Tuple[List[List[float]], List[float], List[List[float]], List[float], List[List[str]], List[str], Union[List[str], None]]:
    label_list: Union[List[str], None] = None
    if not set_together:
        label_list = []

    list_1: List[List[float]] = []
    list_1_together: List[float] = []
    list_2: List[List[float]] = []
    list_2_together: List[float] = []
    point_labels: List[List[str]] = []
    point_labels_together: List[str] = []

    set_key = set(dictionary_1.keys()).intersection(set(dictionary_2.keys()))

    for set_name in sorted(set_key):
        if (directory_set != DirectorySetEnum.all) and (directory_set.value != set_name):
            continue

        dictionary_1_experiment = dictionary_1[set_name]
        dictionary_2_experiment = dictionary_2[set_name]

        if not set_together:
            label_list.append(set_name)

        list_1.append([])
        list_2.append([])
        point_labels.append([])

        experiment_key = set(dictionary_1_experiment.keys()).intersection(set(dictionary_2_experiment.keys()))

        if not use_uncompiled:
            experiment_key_temp = set()

            for experiment_name in experiment_key:
                if dictionary_1_experiment[experiment_name].compiled and dictionary_2_experiment[experiment_name].compiled:
                    experiment_key_temp.add(experiment_name)

            experiment_key = experiment_key_temp

        for experiment_name in experiment_key:
            value_1 = get_value(dictionary_1_experiment[experiment_name])
            value_2 = get_value(dictionary_2_experiment[experiment_name])

            list_1[-1].append(value_1)
            list_2[-1].append(value_2)
            point_labels[-1].append(experiment_name)

            list_1_together.append(value_1)
            list_2_together.append(value_2)
            point_labels_together.append(experiment_name)

    return list_1, list_1_together, list_2, list_2_together, point_labels, point_labels_together, label_list


def generate_more_data(data_list: List[Dict[str, Dict[str, Statistics]]]) -> Tuple[List[List[float]], List[str]]:
    result_list = []
    point_labels: List[str] = []

    for _ in data_list:
        result_list.append([])

    data_list_temp: List[Dict[str, Statistics]] = []

    for data in data_list:
        dictionary_temp: Dict[str, Statistics] = dict()

        for set_name in data:
            if (directory_set != DirectorySetEnum.all) and (directory_set.value != set_name):
                continue

            dictionary_temp.update(data[set_name])

        data_list_temp.append(dictionary_temp)

    experiment_key = set() if not len(data_list_temp) else set(data_list_temp[0].keys())
    for data in data_list_temp:
        experiment_key.intersection_update(data.keys())

    if not use_uncompiled:
        experiment_key_temp = set()

        for experiment_name in experiment_key:
            compiled = True

            for data in data_list_temp:
                if not data[experiment_name].compiled:
                    compiled = False
                    break

            if compiled:
                experiment_key_temp.add(experiment_name)

        experiment_key = experiment_key_temp

    for experiment_name in experiment_key:
        for i, temp in enumerate(data_list_temp):
            value = get_value(temp[experiment_name])
            result_list[i].append(value)

        point_labels.append(experiment_name)

    return result_list, point_labels


def my_print(directory_name: str, z: Dict[str, Dict[str, Statistics]], uncompiled_z: Dict[str, Set[str]]) -> None:
    print(f"---{'-' * len(directory_name)}---")
    print(f"-- {directory_name} --")
    print(f"---{'-' * len(directory_name)}---")

    total_number = sum(len(z[i]) for i in z)
    uncompiled = sum(len(uncompiled_z[i]) for i in uncompiled_z)
    print(f"Total number: {total_number}")
    print(f"Compiled: {total_number - uncompiled}")
    print(f"Uncompiled: {uncompiled}")
    print()

    for set_name in z:
        total_number = len(z[set_name])
        uncompiled = len(uncompiled_z[set_name])
        print(f"\t{set_name} (total number): {total_number}")
        print(f"\t{set_name} (compiled): {total_number - uncompiled}")
        print(f"\t{set_name} (uncompiled): {uncompiled}")

        print()
    print()

def create_file(data: List[List[float]], labels: List[List[str]], point_labels: List[str]) -> None:
    if file_name is None:
        return

    path_temp = Path(os.path.join(file_path, f"{file_name}.csv"))

    with open(path_temp, "w", encoding="utf-8") as file:
        line = "Name"

        # Head
        for label in labels:
            label_temp = label[0].replace(" ", "_").replace("\n", "_").replace("\t", "_")
            line = f"{line};{label_temp}"

        file.write(f"{line}\n")

        for r in range(len(point_labels)):
            point_label = point_labels[r]
            point_label_temp = point_label.replace(" ", "_").replace("\n", "_").replace("\t", "_")
            line = f"{point_label_temp}"

            for i in range(len(data)):
                temp = data[i][r]
                line = f"{line};{temp}"

            file.write(f"{line}\n")
# endregion

title = f"{function}" if title == "" else title
title = title if directory_set == DirectorySetEnum.all else f"{title} \n{directory_set}"

percent_function_list: List[FunctionEnum] = [FunctionEnum.RH_RECOGNITION, FunctionEnum.TWO_CNF_RECOGNITION, FunctionEnum.HYPERGRAPH_CACHING_HIT,
                                             FunctionEnum.COMPONENT_CACHING_HIT, FunctionEnum.RECOMPUTATION_CUT_SET,
                                             FunctionEnum.RATIO_GENERATE_KEY_COMPONENT_CACHING_TIME_AND_COMPILATION_TIME,
                                             FunctionEnum.RATIO_IMPLICATION_GRAPH_TIME_AND_COMPILATION_TIME,
                                             FunctionEnum.RATIO_COPY_CIRCUIT_AND_COMPILATION_TIME,
                                             FunctionEnum.RATIO_NUMBER_OF_HORN_CLAUSES_AND_NUMBER_OF_CLAUSES_LP_FORMULATION,
                                             FunctionEnum.RATIO_NUMBER_OF_SWITCHED_VARIABLES_AND_NUMBER_OF_VARIABLES_LP_FORMULATION,
                                             FunctionEnum.RATIO_EXTENDED_DECISION_NODES_AND_ALL_DECISION_NODES]
percent = True if function in percent_function_list else False

if plot_name is None:
    save_path = None
else:
    save_path = Path(os.path.join(plot_path, plot_name))

data = []
labels = None
data_x, data_y = [], []

use_more_directory = plot != PlotEnum.SCATTER

if not use_more_directory:
    directory_name_1, directory_name_2 = directory_name_1.value, directory_name_2.value
    x, uncompiled_x, uncompiled_x_set = get_statistics(directory_name_1)
    y, uncompiled_y, uncompiled_y_set = get_statistics(directory_name_2)

    data_x, data_x_together, data_y, data_y_together, point_labels, point_labels_together, labels = generate_data(x, y)

    my_print(directory_name_1, x, uncompiled_x)
    my_print(directory_name_2, y, uncompiled_y)

    if set_together:
        print(f"Total number: {len(data_x_together)}")
    else:
        print(f"Total number: {sum(len(i) for i in data_x)}")

    print(f"Total number (uncompiled intersection): {len(uncompiled_x_set.intersection(uncompiled_y_set))}")

    create_file(data=[data_x_together, data_y_together],
                labels=[[directory_name_1], [directory_name_2]],
                point_labels=point_labels_together)

else:
    directory_name_list = [directory_name.value for directory_name in directory_name_list]
    directory_name_labels_boxplot_list = [[f"{label_prefix}{directory_name}"] for directory_name in directory_name_list]
    directory_name_labels_histogram_list = [f"{label_prefix}{directory_name}" for directory_name in directory_name_list]

    temp_list = []
    for directory_name in directory_name_list:
        x, uncompiled_x, uncompiled_x_set = get_statistics(directory_name)
        temp_list.append(x)

        my_print(directory_name, x, uncompiled_x)

    data, point_labels = generate_more_data(temp_list)

    create_file(data=data,
                labels=label_list,
                point_labels=point_labels)

if plot == PlotEnum.SCATTER:
    if x_label == "":
        x_label = directory_name_1

    if y_label == "":
        y_label = directory_name_2

    x_label = f"{x_label} (log)" if log_scale else x_label
    y_label = f"{y_label} (log)" if log_scale else y_label

    scatter(data_x=data_x_together if set_together else data_x,
            data_y=data_y_together if set_together else data_y,
            title=f"{directory_name_1} vs {directory_name_2}" if title == "" else title,
            x_label=x_label,
            y_label=y_label,
            labels=labels,
            point_label=(point_labels_together if set_together else point_labels) if use_point_label else None,
            log_scale=log_scale,
            save_path=save_path)

elif plot == PlotEnum.BOXPLOT:
    boxplot(data=data,
            y_label="%" if percent else None,
            labels=directory_name_labels_boxplot_list if label_list is None else label_list,
            title=title,
            showfliers=showfliers,
            save_path=save_path)

elif plot == PlotEnum.HISTOGRAM:
    histogram(data=data,
              labels=directory_name_labels_histogram_list if label_list is None else label_list,
              title=title,
              bins=number_of_bins,
              save_path=save_path)
