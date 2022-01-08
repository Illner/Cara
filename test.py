import os
import sys
import pickle
import subprocess
import time as sys_time
from pathlib import Path
from datetime import timedelta


benchmark_name = sys.argv[1]
benchmark_path = fr"Benchmark/{benchmark_name}"

number = 0
time_directory = dict()

dir_list = [(file, file_path) for file in os.listdir(benchmark_path) if (os.path.isdir(file_path := os.path.join(benchmark_path, file)))]

for folder_name, folder_path in dir_list:
    experiment_list = [(file, file_path) for file in os.listdir(folder_path) if (os.path.isfile(file_path := os.path.join(folder_path, file)))]

    output_path: Path = Path(os.path.join("Benchmark_prime", benchmark_name, folder_name))
    output_path.mkdir(exist_ok=True, parents=True)

    for experiment_name, experiment_path in experiment_list:
        number += 1
        print(f"Experiment name ({number}): {experiment_name}")

        stopwatch_time = sys_time.perf_counter_ns()

        subprocess.run([f"sed 's/^M$//' {experiment_path} > {experiment_path}"])

        output_path_temp = Path(os.path.join(output_path, experiment_name))
        subprocess.run(["./cnfprime", experiment_path, output_path_temp])

        temp = sys_time.perf_counter_ns()
        time = temp - stopwatch_time

        time_directory[experiment_name] = time
        print(f"Time: {timedelta(microseconds=time * 0.001)}")
        print()

with open(f"{benchmark_name}_time.pkl", "wb") as file:
    pickle.dump(time_directory, file, pickle.HIGHEST_PROTOCOL)
