# Import
import os
import gc
import pickle
import ctypes
import warnings
import threading
from abc import ABC
from pathlib import Path
from datetime import timedelta
from compiler.compiler import Compiler
from typing import Dict, List, Tuple, Union, TypeVar
from compiler_statistics.statistics import Statistics

# Import exception
import exception.cara_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.component_caching.component_caching_enum as cc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum

# Type
TExperimentThread = TypeVar("TExperimentThread", bound="ExperimentThread")


class ExperimentAbstract(ABC):
    """
    Experiment
    """

    """
    Private bool save_circuit
    Private str experiment_name
    Private timedelta total_time
    Private Path log_directory_path
    Private timedelta timeout_experiment
    
    Protected List<Tuple<str, str>> files
    """

    def __init__(self, experiment_name: str, directory_path: [str, Path], timeout_experiment: Union[timedelta, None] = None,
                 log_directory_path: Union[str, Path, None] = None, save_circuit: bool = False):
        self.__save_circuit: bool = save_circuit
        self.__experiment_name: str = experiment_name
        self.__total_time: timedelta = timedelta()  # initialization
        self.__timeout_experiment: Union[timedelta, None] = timeout_experiment

        # Log
        if log_directory_path is not None:
            if isinstance(log_directory_path, str):
                self.__log_directory_path: Path = Path(log_directory_path)
            else:
                self.__log_directory_path: Path = log_directory_path
        else:
            self.__log_directory_path: Path = Path(os.path.join(directory_path, self.__experiment_name))

        self.__log_directory_path.mkdir(parents=True, exist_ok=True)

        # Get all files in the directory
        if isinstance(directory_path, str):
            directory_path = Path(directory_path)
        self._files: List[Tuple[str, str]] = self.__get_files(directory_path)

    # region Protected method
    def _experiment(self,
                    file_name: str, file_path: str,
                    smooth: bool,
                    ub_factor: float,
                    preprocessing: bool,
                    subsumed_threshold: Union[int, None],
                    new_cut_set_threshold: float,
                    sat_solver_enum: ss_enum.SatSolverEnum,
                    implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                    first_implied_literals_enum: il_enum.FirstImpliedLiteralsEnum,
                    component_caching_enum: cc_enum.ComponentCachingEnum,
                    hp_cache_enum: hpc_enum.HypergraphPartitioningCacheEnum,
                    hp_software_enum: hps_enum.HypergraphPartitioningSoftwareEnum,
                    hp_node_weight_type_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum,
                    hp_hyperedge_weight_type_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum,
                    hp_variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum,
                    hp_limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                    hp_limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                    cut_set_try_cache: bool = False,
                    new_cut_set_threshold_reduction: float = 1,
                    file_name_extension: str = "") -> \
            Tuple[bool, bool, Union[int, None], Statistics]:
        """
        :return: (timeout exceeded, exception, size of the circuit, statistics)
        """

        print("----------------------------------------------------------")
        if file_name_extension == "":
            print(f"File name: {file_name}")
        else:
            print(f"File name: {file_name}, params: {file_name_extension}")

        compiler = Compiler(cnf=file_path,
                            smooth=smooth,
                            ub_factor=ub_factor,
                            preprocessing=preprocessing,
                            subsumed_threshold=subsumed_threshold,
                            new_cut_set_threshold=new_cut_set_threshold,
                            sat_solver_enum=sat_solver_enum,
                            implied_literals_enum=implied_literals_enum,
                            first_implied_literals_enum=first_implied_literals_enum,
                            component_caching_enum=component_caching_enum,
                            hp_cache_enum=hp_cache_enum,
                            hp_software_enum=hp_software_enum,
                            hp_node_weight_type_enum=hp_node_weight_type_enum,
                            hp_hyperedge_weight_type_enum=hp_hyperedge_weight_type_enum,
                            hp_variable_simplification_enum=hp_variable_simplification_enum,
                            hp_limit_number_of_clauses_cache=hp_limit_number_of_clauses_cache,
                            hp_limit_number_of_variables_cache=hp_limit_number_of_variables_cache,
                            cut_set_try_cache=cut_set_try_cache,
                            new_cut_set_threshold_reduction=new_cut_set_threshold_reduction)

        experiment_thread: TExperimentThread = self.__ExperimentThread(compiler)
        thread = threading.Thread(target=self.__experiment, args=(experiment_thread,))
        thread.start()

        if self.__timeout_experiment is not None:
            thread.join(timeout=self.__timeout_experiment.total_seconds())
        else:
            thread.join()

        # Total time
        if thread.is_alive():
            self.__total_time += self.__timeout_experiment
        else:
            statistics: Statistics = experiment_thread.compiler.statistics

            self.__total_time += statistics.compiler_statistics.get_time()  # compiler
            self.__total_time += statistics.cnf_statistics.get_time()       # CNF

        # Timeout exceeded
        while thread.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.native_id, ctypes.py_object(TimeoutError))
            thread.join(1)

        timeout_exceeded: bool = experiment_thread.timeout_exceeded
        exception: bool = False if experiment_thread.exception is None else True
        size: Union[int, None] = None if timeout_exceeded or exception else experiment_thread.compiler.circuit.size
        statistics: Statistics = experiment_thread.compiler.statistics

        if exception:
            print(f"Error: {experiment_thread.exception}")
        else:
            if timeout_exceeded:
                print("Timeout exceeded")
            else:
                print(f"Done ({str(statistics.compiler_statistics.get_time())})")

        # Log - directory
        file_name_temp = file_name if file_name_extension == "" else f"{file_name}_{file_name_extension}"
        directory_path_temp: Path = Path(os.path.join(self.__log_directory_path, file_name_temp))
        directory_path_temp.mkdir(exist_ok=True)

        # Log - statistics
        statistics_path_temp: Path = Path(os.path.join(directory_path_temp, "statistics.pkl"))
        with open(statistics_path_temp, "wb") as file:
            pickle.dump(statistics, file, pickle.HIGHEST_PROTOCOL)
        statistics_path_temp: Path = Path(os.path.join(directory_path_temp, "statistics.stat"))
        with open(statistics_path_temp, "w", encoding="utf8") as file:
            file.write(str(statistics))

        # Log - circuit
        if self.__save_circuit and (not timeout_exceeded) and (not exception):
            circuit_path_temp = Path(os.path.join(directory_path_temp, "circuit.nnf"))
            with open(circuit_path_temp, "w", encoding="utf8") as file:
                file.write(str(experiment_thread.compiler.circuit))

        del compiler
        gc.collect()

        return timeout_exceeded, exception, size, statistics

    def _pickle_object(self, file_name: str, object_to_save: Union[Dict]) -> None:
        path_temp: Path = Path(os.path.join(self.log_directory_path, f"{file_name}.pkl"))
        with open(path_temp, "wb") as file:
            pickle.dump(object_to_save, file, pickle.HIGHEST_PROTOCOL)
    # endregion

    # region Static method
    @staticmethod
    def __get_files(directory_path: Path) -> List[Tuple[str, str]]:
        """
        Return a list of all files (name, path) in the directory (directory_path)
        :return: a list of files
        """

        # Check if the directory exists
        if not directory_path.exists():
            warnings.warn("Directory doesn't exist!", category=UserWarning)
            return []

        return [(file, file_path) for file in os.listdir(directory_path)
                if (os.path.isfile(file_path := os.path.join(directory_path, file)))]

    @staticmethod
    def __experiment(experiment_thread: TExperimentThread):
        try:
            experiment_thread.compiler.create_circuit()
        # Timeout exceeded
        except TimeoutError:
            experiment_thread.timeout_exceeded = True
        except c_exception.CaraException as err:
            experiment_thread.exception = err
    # endregion

    # region Property
    @property
    def experiment_name(self):
        return self.__experiment_name

    @property
    def log_directory_path(self):
        return self.__log_directory_path

    @property
    def total_time(self):
        return self.__total_time
    # endregion

    class __ExperimentThread:
        """
        Public Compiler compiler
        Public bool timeout_exceeded
        Public Exception exception
        """

        def __init__(self, compiler: Compiler):
            self.compiler: Compiler = compiler
            self.timeout_exceeded: bool = False
            self.exception: [Exception, None] = None
