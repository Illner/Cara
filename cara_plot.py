# Import
import os
import pickle
from pathlib import Path
from enum import Enum, unique, IntEnum
from typing import Dict, Tuple, List, Set, Union
from compiler_statistics.statistics import Statistics
from visualization.plot import scatter, boxplot, histogram

# Import enum
import circuit.node.node_type_enum as nt_enum

plot_path = r"C:\Users\illner\Desktop"

bdmc_root_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\BDMC"
hp_cache_root_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\HP cache"
cara_circuit_root_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\CaraCircuit"
imbalance_factor_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\Imbalance factor"
dnnf_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\DNNF"


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

    IMBALANCE_FACTOR_1 = "0.1"
    IMBALANCE_FACTOR_1_QUALITY = "0.1 PaToH quality"
    IMBALANCE_FACTOR_1_SPEED = "0.1 PaToH speed"
    IMBALANCE_FACTOR_25 = "0.25"
    IMBALANCE_FACTOR_25_QUALITY = "0.25 PaToH quality"
    IMBALANCE_FACTOR_25_SPEED = "0.25 PaToH speed"
    IMBALANCE_FACTOR_4 = "0.4"
    IMBALANCE_FACTOR_4_QUALITY = "0.4 PaToH quality"
    IMBALANCE_FACTOR_4_SPEED = "0.4 PaToH speed"

    DNNF_CLAUSE_REDUCTION = "Clause reduction"
    DNNF_CLAUSE_REDUCTION_EXT = "Clause reduction (ext)"

@unique
class PlotEnum(IntEnum):
    BOXPLOT = 1
    SCATTER = 2
    HISTOGRAM = 3


root_path = dnnf_path

# SCATTER
directory_name_1: ExperimentEnum = ExperimentEnum.DNNF_CLAUSE_REDUCTION
directory_name_2: ExperimentEnum = ExperimentEnum.DNNF_CLAUSE_REDUCTION_EXT

# BOXPLOT, HISTOGRAM
directory_name_list: List[ExperimentEnum] = [ExperimentEnum.BDMC_VSADS_25,
                                             ExperimentEnum.BDMC_VSADS_25_EXTENDED]

none_value: float = 0   # 10**10
uncompiled_value: Union[float, None] = None     # 10**10

title: str = "Number of decisions"

percent: bool = False
use_uncompiled: bool = False
plot: PlotEnum = PlotEnum.SCATTER
plot_name: Union[str, None] = None
directory_set: DirectorySetEnum = DirectorySetEnum.all

# SCATTER
x_label: str = "size (clause reduction)"
y_label: str = "size (clause reduction ext)"
log_scale: bool = False
set_together: bool = False

# BOXPLOT
showfliers: bool = False

# BOXPLOT, HISTOGRAM
label_prefix: str = ""
label_list: Union[List[List[str]], None] = [["VSADS"],
                                            ["VSADS ext"],
                                            ["ib 40 %"],
                                            ["d-BDMC \nlimit 500"],
                                            ["d-BDMC \nlimit 1000"],
                                            ["d-BDMC \nlimit 1500"]]


def function(statistics: Statistics) -> Union[float, None]:
    return statistics.size  # + statistics.component_statistics.component_caching_after_cara_mapping_length.sum_count
    # return statistics.compiler_statistics.create_circuit.average_time

    # return statistics.hypergraph_partitioning_statistics.cut_set_size.average_count

    # return statistics.get_node_type_counter(nt_enum.NodeTypeEnum.RENAMABLE_HORN_CNF) + statistics.get_node_type_counter(nt_enum.NodeTypeEnum.TWO_CNF)

    # two_cnf_number = statistics.component_statistics.two_cnf_formula_length.number_of_calls
    # two_cnf_length = statistics.component_statistics.two_cnf_formula_length.sum_count
    # two_cnf_length = 0 if two_cnf_length is None else two_cnf_length
    #
    # horn_cnf_number = statistics.component_statistics.renamable_horn_cnf_formula_length.number_of_calls
    # horn_cnf_length = statistics.component_statistics.renamable_horn_cnf_formula_length.sum_count
    # horn_cnf_length = 0 if horn_cnf_length is None else horn_cnf_length
    #
    # # return two_cnf_number + horn_cnf_number
    #
    # if two_cnf_number + horn_cnf_number == 0:
    #     return 0
    #
    # x = (two_cnf_length + horn_cnf_length) / (two_cnf_number + horn_cnf_number)
    #
    # return x

    # try:
    #     return statistics.get_node_type_counter(nt_enum.NodeTypeEnum.MAPPING_NODE)
    # except KeyError:
    #     return 0
    # return statistics.component_statistics.component_caching_after_cara_mapping_length.number_of_calls
    # return statistics.component_statistics.two_cnf_formula_length.average_count
    # return statistics.hypergraph_partitioning_statistics.get_cut_set.average_time
    # return statistics.hypergraph_partitioning_statistics.cache_hit.average_count
    # return statistics.component_statistics.component_caching_after_hit.average_count
    # return statistics.component_statistics.component_caching_after_formula_length.average_count
    # return statistics.component_statistics.decision_variable.sum_count


def get_statistics(directory_name: str) -> Tuple[Dict[str, Dict[str, Statistics]], Dict[str, Set[str]], Set[str]]:
    path = Path(os.path.join(root_path, directory_name))

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
    if not statistics.compiled and (uncompiled_value is not None):
        return uncompiled_value

    # Function
    value = function(statistics)

    if value is None:
        return none_value

    if percent:
        return 100 * value

    return value


def generate_data(dictionary_1: Dict[str, Dict[str, Statistics]], dictionary_2: Dict[str, Dict[str, Statistics]]) -> \
        Union[Tuple[List[float], List[float], Union[List[str], None]], Tuple[List[List[float]], List[List[float]], Union[List[str], None]]]:

    label_list: Union[List[str], None] = None
    if not set_together:
        label_list = []

    list_1: List[Union[float, List[float]]] = []
    list_2: List[Union[float, List[float]]] = []

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

            if not set_together:
                list_1[-1].append(value_1)
                list_2[-1].append(value_2)
            else:
                list_1.append(value_1)
                list_2.append(value_2)

    return list_1, list_2, label_list


def generate_more_data(data_list: List[Dict[str, Dict[str, Statistics]]]) -> List[List[float]]:
    result_list = []
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

    return result_list


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

    data_x, data_y, labels = generate_data(x, y)

    my_print(directory_name_1, x, uncompiled_x)
    my_print(directory_name_2, y, uncompiled_y)

    if set_together:
        print(f"Total number: {len(data_x)}")
    else:
        print(f"Total number: {sum(len(i) for i in data_x)}")

    print(f"Total number (uncompiled intersection): {len(uncompiled_x_set.intersection(uncompiled_y_set))}")

else:
    directory_name_list = [directory_name.value for directory_name in directory_name_list]
    directory_name_labels_boxplot_list = [[f"{label_prefix}{directory_name}"] for directory_name in directory_name_list]
    directory_name_labels_histogram_list = [f"{label_prefix}{directory_name}" for directory_name in directory_name_list]

    temp_list = []
    for directory_name in directory_name_list:
        x, uncompiled_x, uncompiled_x_set = get_statistics(directory_name)
        temp_list.append(x)

        my_print(directory_name, x, uncompiled_x)

    data = generate_more_data(temp_list)

if plot == PlotEnum.SCATTER:
    if x_label == "":
        x_label = directory_name_1

    if y_label == "":
        y_label = directory_name_2

    x_label = f"{x_label} (log)" if log_scale else x_label
    y_label = f"{y_label} (log)" if log_scale else y_label

    scatter(data_x=data_x,
            data_y=data_y,
            title=f"{directory_name_1} vs {directory_name_2}" if title == "" else title,
            x_label=x_label,
            y_label=y_label,
            labels=labels,
            log_scale=log_scale,
            save_path=save_path)

elif plot == PlotEnum.BOXPLOT:
    boxplot(data=data,
            labels=directory_name_labels_boxplot_list if label_list is None else label_list,
            title=title,
            showfliers=showfliers,
            save_path=save_path)

elif plot == PlotEnum.HISTOGRAM:
    histogram(data=data,
              labels=directory_name_labels_histogram_list if label_list is None else label_list,
              title=title,
              save_path=save_path)
