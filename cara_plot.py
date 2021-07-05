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
    D4 = "D4"
    JW_TS_1 = "JW-TS, extended, 0.1"
    JW_TS_25 = "JW-TS, extended, 0.25"
    DLCS_DLIS_1 = "DLCS-DLIS, extended, 0.1"
    DLCS_DLIS_25 = "DLCS-DLIS, extended, 0.25"
    VSADS_1 = "VSADS, d4, extended, 0.1"
    VSADS_25 = "VSADS, d4, extended, 0.25"
    CLAUSE_REDUCTION_1 = "Clause reduction, 0.1"
    CLAUSE_REDUCTION_25 = "Clause reduction, 0.25"
    WEIGHTED_BINARIES_1 = "Weighted binaries, 0.1"
    WEIGHTED_BINARIES_25 = "Weighted binaries, 0.25"

    NONE = "NONE"
    ISOMORFISM_250 = "ISOMORFISM 250"
    ISOMORFISM_500 = "ISOMORFISM 500"
    ISOMORFISM_1000 = "ISOMORFISM 1000"


@unique
class PlotEnum(IntEnum):
    BOXPLOT = 1
    SCATTER = 2
    HISTOGRAM = 3


root_path = bdmc_root_path
directory_name_1: ExperimentEnum = ExperimentEnum.VSADS_1
directory_name_2: ExperimentEnum = ExperimentEnum.VSADS_25

none_value: float = 10**10
uncompiled_value: float = 10**10

log_scale: bool = True
showfliers: bool = False
use_uncompiled: bool = True
plot: PlotEnum = PlotEnum.SCATTER
directory_set: DirectorySetEnum = DirectorySetEnum.all


def function(statistics: Statistics) -> Union[float, None]:
    # return statistics.compiler_statistics.create_circuit.average_time
    return statistics.size
    # return statistics.hypergraph_partitioning_statistics.get_cut_set.average_time
    # return statistics.hypergraph_partitioning_statistics.cache_hit.average_count
    # return statistics.component_statistics.component_caching_after_hit.average_count


def get_statistics(directory_name: str) -> Tuple[Dict[str, Statistics], Set[str]]:
    path = Path(os.path.join(root_path, directory_name))

    uncompiled_set: Set[str] = set()
    experiment_dictionary: Dict[str, Statistics] = dict()

    for directory in os.listdir(path):
        if (directory_set != DirectorySetEnum.all) and (directory != directory_set.value):
            continue

        path_temp = Path(os.path.join(path, directory))

        for experiment_directory in os.listdir(path_temp):
            statistics_path_temp = Path(os.path.join(path_temp, experiment_directory, "statistics.pkl"))

            with open(statistics_path_temp, 'rb') as file:
                statistics = pickle.load(file)

            if not statistics.compiled:
                uncompiled_set.add(experiment_directory)

            experiment_dictionary[experiment_directory] = statistics

    return experiment_dictionary, uncompiled_set


def generate_data(dictionary_1: Dict[str, Statistics], dictionary_2: Dict[str, Statistics]) -> Tuple[List[float], List[float]]:
    list_1: List[float] = []
    list_2: List[float] = []

    key_set = set(dictionary_1.keys()).intersection(set(dictionary_2.keys()))

    if not use_uncompiled:
        key_set_temp = set()

        for key in key_set:
            if dictionary_1[key].compiled and dictionary_2[key].compiled:
                key_set_temp.add(key)

        key_set = key_set_temp

    def get_value(key_func: str, dictionary_func: Dict[str, Statistics]):
        statistics_temp = dictionary_func[key_func]

        if not statistics_temp.compiled:
            return uncompiled_value

        # Function
        value = function(statistics_temp)

        if value is None:
            return none_value

        return value

    for key in key_set:
        value_1 = get_value(key, dictionary_1)
        value_2 = get_value(key, dictionary_2)

        list_1.append(value_1)
        list_2.append(value_2)

    return list_1, list_2


directory_name_1, directory_name_2 = directory_name_1.value, directory_name_2.value
x, uncompiled_x = get_statistics(directory_name_1)
y, uncompiled_y = get_statistics(directory_name_2)
data_x, data_y = generate_data(x, y)

print(f"---{'-'*len(directory_name_1)}---")
print(f"-- {directory_name_1} --")
print(f"---{'-'*len(directory_name_1)}---")
print(f"Count: {len(x)}")
print(f"Count (uncompiled): ({len(uncompiled_x)})")
print()

print(f"---{'-'*len(directory_name_2)}---")
print(f"-- {directory_name_2} --")
print(f"---{'-'*len(directory_name_2)}---")
print(f"Count: {len(y)}")
print(f"Count (uncompiled): ({len(uncompiled_y)})")
print()

print(f"Count: {len(data_x)}")
print(f"Count (uncompiled intersection): {len(uncompiled_x.intersection(uncompiled_y))}")

if plot == PlotEnum.SCATTER:
    scatter(data_x=data_x,
            data_y=data_y,
            title=f"{directory_name_1} vs {directory_name_2}",
            x_label=directory_name_1,
            y_label=directory_name_2,
            log_scale=log_scale)

elif plot == PlotEnum.BOXPLOT:
    boxplot(data=[[data_x], [data_y]],
            labels=[[directory_name_1], [directory_name_2]],
            title=f"{directory_name_1} vs {directory_name_2}",
            showfliers=showfliers)

elif plot == PlotEnum.HISTOGRAM:
    histogram(data=[data_x, data_y],
              title=f"{directory_name_1} vs {directory_name_2}",
              labels=[directory_name_1, directory_name_2])
