# Import
import os
import sys
from shutil import move
from other.other import listdir_no_hidden


from_path = sys.argv[1]
to_path = sys.argv[2] + r"\DNNF\D4 (DLCS-DLIS)"

benchmark_path = sys.argv[3]
benchmark_type_list = [(file, file_path) for file in listdir_no_hidden(benchmark_path) if (os.path.isdir(file_path := os.path.join(benchmark_path, file)))]

benchmark_type_experiment_name_dictionary = dict()
experiment_name_benchmark_type_dictionary = dict()

for benchmark_type, _ in benchmark_type_list:
    path = f"{benchmark_path}{os.path.sep}{benchmark_type}"
    benchmark_type_experiment_name_dictionary[benchmark_type] = set()

    file_list = [(file, file_path) for file in listdir_no_hidden(path) if (os.path.isfile(file_path := os.path.join(path, file)))]

    for file_name, _ in file_list:
        benchmark_type_experiment_name_dictionary[benchmark_type].add(file_name)
        experiment_name_benchmark_type_dictionary[file_name] = benchmark_type

dir_list = [(file, file_path) for file in listdir_no_hidden(from_path) if (os.path.isdir(file_path := os.path.join(from_path, file)))]

for dir_name, dir_path in dir_list:
    experiment_dir_list = [(file, file_path) for file in listdir_no_hidden(dir_path) if (os.path.isdir(file_path := os.path.join(dir_path, file)))]

    for experiment_name, experiment_path in experiment_dir_list:
        if experiment_name not in experiment_name_benchmark_type_dictionary:
            print(f"!!!!! For {experiment_name} is missing the type of benchmark!")
            continue

        benchmark_type = experiment_name_benchmark_type_dictionary[experiment_name]

        path = f"{to_path}{os.path.sep}{benchmark_type}{os.path.sep}{experiment_name}"

        move(experiment_path, path)
        print(f"{experiment_name} has been copied ({benchmark_type})")
