# Import
import os
from shutil import move


from_path = r"C:\Users\illner\Desktop\temp\Results"
to_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Experiments\BDMC RH SD\DLCS-DLIS (-a, -c, p, -ext, 2)"

benchmark_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\MetaCentrum\Benchmark_one"
benchmark_type_list = [(file, file_path) for file in os.listdir(benchmark_path) if (os.path.isdir(file_path := os.path.join(benchmark_path, file)))]

benchmark_type_experiment_name_dictionary = dict()
experiment_name_benchmark_type_dictionary = dict()

for benchmark_type, _ in benchmark_type_list:
    path = f"{benchmark_path}/{benchmark_type}"
    benchmark_type_experiment_name_dictionary[benchmark_type] = set()

    file_list = [(file, file_path) for file in os.listdir(path) if (os.path.isfile(file_path := os.path.join(path, file)))]

    for file_name, _ in file_list:
        benchmark_type_experiment_name_dictionary[benchmark_type].add(file_name)
        experiment_name_benchmark_type_dictionary[file_name] = benchmark_type

dir_list = [(file, file_path) for file in os.listdir(from_path) if (os.path.isdir(file_path := os.path.join(from_path, file)))]

for dir_name, dir_path in dir_list:
    experiment_dir_list = [(file, file_path) for file in os.listdir(dir_path) if (os.path.isdir(file_path := os.path.join(dir_path, file)))]

    for experiment_name, experiment_path in experiment_dir_list:
        if experiment_name not in experiment_name_benchmark_type_dictionary:
            print(f"!!!!! For {experiment_name} is missing the type of benchmark!")
            continue

        benchmark_type = experiment_name_benchmark_type_dictionary[experiment_name]

        path = f"{to_path}/{benchmark_type}/{experiment_name}"

        move(experiment_path, path)
        print(f"{experiment_name} has been copied ({benchmark_type})")
