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

plot_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\Plots\BDMC"

bdmc_root_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\BDMC"
hp_cache_root_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\HP cache"


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
    LIMIT_250 = "250"
    LIMIT_500 = "500"
    LIMIT_1000 = "1000"
    LIMIT_1500 = "1500"
    D4 = "D4"
    JW_TS_1_EXTENDED = "JW-TS, extended, 0.1"
    JW_TS_25_EXTENDED = "JW-TS, extended, 0.25"
    JW_TS_25 = "JW-TS, 0.25"
    DLCS_DLIS_1_EXTENDED = "DLCS-DLIS, extended, 0.1"
    DLCS_DLIS_25_EXTENDED = "DLCS-DLIS, extended, 0.25"
    DLCS_DLIS_25 = "DLCS-DLIS, 0.25"
    VSADS_1_EXTENDED = "VSADS, d4, extended, 0.1"
    VSADS_25_EXTENDED = "VSADS, d4, extended, 0.25"
    VSADS_25 = "VSADS, d4, 0.25"
    CLAUSE_REDUCTION_1 = "Clause reduction, 0.1"
    CLAUSE_REDUCTION_25 = "Clause reduction, 0.25"
    CLAUSE_REDUCTION_25_WITHOUT_GAMMA_0 = "Clause reduction, 0.25, without gamma_0"
    WEIGHTED_BINARIES_1 = "Weighted binaries, 0.1"
    WEIGHTED_BINARIES_25 = "Weighted binaries, 0.25"
    WEIGHTED_BINARIES_25_WITHOUT_GAMMA_0 = "Weighted binaries, 0.25, without gamma_0"

    NONE = "NONE"
    ISOMORFISM_250 = "ISOMORFISM 250"
    ISOMORFISM_250_no_moc = "ISOMORFISM 250 (no moc)"
    ISOMORFISM_500 = "ISOMORFISM 500"
    ISOMORFISM_500_no_moc = "ISOMORFISM 500 (no moc)"
    ISOMORFISM_1000 = "ISOMORFISM 1000"
    ISOMORFISM_1000_no_moc = "ISOMORFISM 1000 (no moc)"
    ISOMORFISM_1500 = "ISOMORFISM 1500"
    ISOMORFISM_1500_no_moc = "ISOMORFISM 1500 (no moc)"
    ISOMORFISM_VARIANCE_250 = "ISOMORFISM_VARIANCE 250"
    ISOMORFISM_VARIANCE_250_no_moc = "ISOMORFISM_VARIANCE 250 (no moc)"
    ISOMORFISM_VARIANCE_500 = "ISOMORFISM_VARIANCE 500"
    ISOMORFISM_VARIANCE_500_no_moc = "ISOMORFISM_VARIANCE 500 (no moc)"
    ISOMORFISM_VARIANCE_1000 = "ISOMORFISM_VARIANCE 1000"
    ISOMORFISM_VARIANCE_1000_no_moc = "ISOMORFISM_VARIANCE 1000 (no moc)"
    ISOMORFISM_VARIANCE_1500 = "ISOMORFISM_VARIANCE 1500"
    ISOMORFISM_VARIANCE_1500_no_moc = "ISOMORFISM_VARIANCE 1500 (no moc)"


@unique
class PlotEnum(IntEnum):
    BOXPLOT = 1
    SCATTER = 2
    HISTOGRAM = 3


root_path = bdmc_root_path

# SCATTER
directory_name_1: ExperimentEnum = ExperimentEnum.D4
directory_name_2: ExperimentEnum = ExperimentEnum.LIMIT_250

# BOXPLOT, HISTOGRAM
directory_name_list: List[ExperimentEnum] = [ExperimentEnum.VSADS_25_EXTENDED,
                                             ExperimentEnum.LIMIT_250,
                                             ExperimentEnum.LIMIT_500,
                                             ExperimentEnum.LIMIT_1000,
                                             ExperimentEnum.LIMIT_1500,
                                             ExperimentEnum.D4]

none_value: float = 0   #10**10
uncompiled_value: Union[float, None] = None     # 10**10

title: str = ""
x_label: str = ""
y_label: str = ""

use_uncompiled: bool = True
plot: PlotEnum = PlotEnum.SCATTER
plot_name: Union[str, None] = None
directory_set: DirectorySetEnum = DirectorySetEnum.all

# SCATTER
log_scale: bool = True
set_together: bool = False

# BOXPLOT
showfliers: bool = False


def function(statistics: Statistics) -> Union[float, None]:
    return statistics.size
    # return statistics.compiler_statistics.create_circuit.average_time
    # return statistics.component_statistics.two_cnf_formula_length.average_count
    # return statistics.hypergraph_partitioning_statistics.get_cut_set.average_time
    # return statistics.hypergraph_partitioning_statistics.cache_hit.average_count
    # return statistics.component_statistics.component_caching_after_hit.average_count


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

    return value


def generate_data(dictionary_1: Dict[str, Dict[str, Statistics]], dictionary_2: Dict[str, Dict[str, Statistics]]) -> \
        Union[Tuple[List[float], List[float], Union[List[str], None]], Tuple[List[List[float]], List[List[float]], Union[List[str], None]]]:

    label_list: Union[List[str], None] = None
    if not set_together:
        label_list = []

    list_1: List[Union[float, List[float]]] = []
    list_2: List[Union[float, List[float]]] = []

    key_set = set(dictionary_1.keys()).intersection(set(dictionary_2.keys()))

    for set_name in sorted(key_set):
        if (directory_set != DirectorySetEnum.all) and (directory_set.value != set_name):
            continue

        dictionary_1_experiment = dictionary_1[set_name]
        dictionary_2_experiment = dictionary_2[set_name]

        if not set_together:
            label_list.append(set_name)
            list_1.append([])
            list_2.append([])

        key_experiment = set(dictionary_1_experiment.keys()).intersection(set(dictionary_2_experiment.keys()))

        if not use_uncompiled:
            key_experiment_temp = set()

            for experiment_name in key_experiment:
                if dictionary_1_experiment[experiment_name].compiled and dictionary_2_experiment[experiment_name].compiled:
                    key_experiment_temp.add(experiment_name)

            key_experiment = key_experiment_temp

        for experiment_name in key_experiment:
            value_1 = get_value(dictionary_1_experiment[experiment_name])
            value_2 = get_value(dictionary_2_experiment[experiment_name])

            if not set_together:
                list_1[-1].append(value_1)
                list_2[-1].append(value_2)
            else:
                list_1.append(value_1)
                list_2.append(value_2)

    return list_1, list_2, label_list


def generate_data_more(data_list: List[Dict[str, Dict[str, Statistics]]]) -> List[List[float]]:
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

    key_experiment = set() if not len(data_list_temp) else set(data_list_temp[0].keys())
    for temp in data_list_temp:
        key_experiment.intersection_update(temp.keys())

    if not use_uncompiled:
        key_experiment_temp = set()

        for experiment_name in key_experiment:
            compiled = True

            for temp in data_list_temp:
                if not temp[experiment_name].compiled:
                    compiled = False
                    break

            if compiled:
                key_experiment_temp.add(experiment_name)

        key_experiment = key_experiment_temp

    for experiment_name in key_experiment:
        for i, temp in enumerate(data_list_temp):
            value = get_value(temp[experiment_name])
            result_list[i].append(value)

    return result_list


def my_print(directory_name: str, z: Dict[str, Dict[str, Statistics]], uncompiled_z: Dict[str, Set[str]]) -> None:
    print(f"---{'-' * len(directory_name)}---")
    print(f"-- {directory_name} --")
    print(f"---{'-' * len(directory_name)}---")

    count = sum(len(z[i]) for i in z)
    uncompiled = sum(len(uncompiled_z[i]) for i in uncompiled_z)
    print(f"Count: {count}")
    print(f"Compiled: {count - uncompiled}")
    print(f"Uncompiled: {uncompiled}")
    print()

    for set_name in z:
        count = len(z[set_name])
        uncompiled = len(uncompiled_z[set_name])
        print(f"\t{set_name}: {count}")
        print(f"\t{set_name} (compiled): {count - uncompiled}")
        print(f"\t{set_name} (uncompiled): {uncompiled}")

        print()
    print()


if plot_name is None:
    save_path = None
else:
    save_path = Path(os.path.join(plot_path, plot_name))

data = []
data_x, data_y = [], []
labels = None

use_more_directory = plot != PlotEnum.SCATTER

if not use_more_directory:
    directory_name_1, directory_name_2 = directory_name_1.value, directory_name_2.value
    x, uncompiled_x, uncompiled_x_set = get_statistics(directory_name_1)
    y, uncompiled_y, uncompiled_y_set = get_statistics(directory_name_2)

    data_x, data_y, labels = generate_data(x, y)

    my_print(directory_name_1, x, uncompiled_x)
    my_print(directory_name_2, y, uncompiled_y)

    if set_together:
        print(f"Count: {len(data_x)}")
    else:
        print(f"Count: {sum(len(i) for i in data_x)}")

    print(f"Count (uncompiled intersection): {len(uncompiled_x_set.intersection(uncompiled_y_set))}")

else:
    directory_name_list = [directory_name.value for directory_name in directory_name_list]
    directory_name_labels_list = [[directory_name] for directory_name in directory_name_list]

    temp_list = []
    for directory_name in directory_name_list:
        x, uncompiled_x, uncompiled_x_set = get_statistics(directory_name)
        temp_list.append(x)

        my_print(directory_name, x, uncompiled_x)

    data = generate_data_more(temp_list)

if plot == PlotEnum.SCATTER:
    scatter(data_x=data_x,
            data_y=data_y,
            title=f"{directory_name_1} vs {directory_name_2}" if title == "" else title,
            x_label=directory_name_1 if x_label == "" else x_label,
            y_label=directory_name_2 if y_label == "" else y_label,
            labels=labels,
            log_scale=log_scale,
            save_path=save_path)

elif plot == PlotEnum.BOXPLOT:
    boxplot(data=data,
            labels=directory_name_labels_list,
            title=f"{directory_name_1} vs {directory_name_2}" if title == "" else title,
            showfliers=showfliers,
            save_path=save_path)

elif plot == PlotEnum.HISTOGRAM:
    histogram(data=data,
              labels=directory_name_labels_list,
              title=f"{directory_name_1} vs {directory_name_2}" if title == "" else title,
              save_path=save_path)
