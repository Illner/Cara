# Import
import os
import pickle
from pathlib import Path
from enum import Enum, unique
from visualization.plot import scatter
from visualization.plot import boxplot
from typing import Dict, Tuple, List, Set
from compiler_statistics.statistics import Statistics

# Import enum
import circuit.node.node_type_enum as nt_enum


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


none_value: float = 0
uncompiled_value: float = 0     # 10**10

log_scale: bool = True
show_scatter: bool = True
use_uncompiled: bool = False
directory_set: DirectorySetEnum = DirectorySetEnum.all

# JW-TS, extended, 0.1
# DLCS-DLIS, extended, 0.1
# VSADS, d4, extended, 0.1

directory_name_1: str = "DLCS-DLIS, extended, 0.1"
directory_name_2: str = "DLCS-DLIS, extended, 0.25"
root_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\BDMC"


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
        value = statistics_temp.size

        if value is None:
            return none_value

        return value

    for key in key_set:
        value_1 = get_value(key, dictionary_1)
        value_2 = get_value(key, dictionary_2)

        list_1.append(value_1)
        list_2.append(value_2)

    return list_1, list_2


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

if show_scatter:
    scatter(data_x=data_x,
            data_y=data_y,
            title=f"{directory_name_1} vs {directory_name_2}",
            x_label=directory_name_1,
            y_label=directory_name_2,
            log_scale=log_scale)
else:
    boxplot(data=[[data_x], [data_y]],
            labels=[[directory_name_1], [directory_name_2]],
            title=f"{directory_name_1} vs {directory_name_2}",
            x_label=directory_name_1,
            y_label=directory_name_2)
