# Import
import os
import gc
import pickle
import kthread
import datetime
import warnings
from pathlib import Path
from datetime import timedelta
from compiler.compiler import Compiler
from compiler_statistics.statistics import Statistics
from typing import Set, Dict, List, Tuple, Union, TypeVar

# Import exception
import exception.cara_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.base_class_enum as bc_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.enum.component_caching_enum as cc_enum
import formula.enum.lp_formulation_type_enum as lpft_enum
import compiler.enum.heuristic.decision_heuristic_enum as dh_enum
import formula.enum.eliminating_redundant_clauses_enum as erc_enum
import compiler.enum.heuristic.preselection_heuristic_enum as ph_enum
import compiler.enum.heuristic.mixed_difference_heuristic_enum as mdh_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_patoh_sugparam_enum as hpps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum

# Type
TExperimentThread = TypeVar("TExperimentThread", bound="ExperimentThread")


class Experiment:
    """
    Experiment
    """

    """
    Private bool save_circuit
    Private str node_statistics
    Private str experiment_name
    Private timedelta total_time
    Private Path log_directory_path
    Private str mapping_node_statistics
    Private timedelta timeout_experiment
    
    Protected List<Tuple<str, str>> files
    """

    def __init__(self, experiment_name: str, directory_path: [str, Path], timeout_experiment: Union[timedelta, None] = None,
                 log_directory_path: Union[str, Path, None] = None, save_circuit: bool = False,
                 mapping_node_statistics: Union[str, None] = None, node_statistics: Union[str, None] = None):
        self.__save_circuit: bool = save_circuit
        self.__total_time: timedelta = timedelta()
        self.__experiment_name: str = experiment_name
        self.__timeout_experiment: Union[timedelta, None] = timeout_experiment

        self.__node_statistics: Union[str, None] = node_statistics
        self.__mapping_node_statistics: Union[str, None] = mapping_node_statistics

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
        self._files: List[Tuple[str, str]] = Experiment.__get_files(directory_path)

    # region Public method
    def experiment(self,
                   file_name: str, file_path: str,
                   smooth: bool,
                   preprocessing: bool,
                   imbalance_factor: Union[float, None],
                   subsumed_threshold: Union[int, None],
                   new_cut_set_threshold: float,
                   decision_heuristic_enum: dh_enum.DecisionHeuristicEnum,
                   sat_solver_enum: ss_enum.SatSolverEnum,
                   base_class_enum_set: Set[bc_enum.BaseClassEnum],
                   implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                   implied_literals_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum,
                   first_implied_literals_enum: il_enum.ImpliedLiteralsEnum,
                   first_implied_literals_preselection_heuristic_enum: ph_enum.PreselectionHeuristicEnum,
                   component_caching_enum: cc_enum.ComponentCachingEnum,
                   component_caching_before_unit_propagation: bool,
                   component_caching_after_unit_propagation: bool,
                   eliminating_redundant_clauses_enum: erc_enum.EliminatingRedundantClausesEnum,
                   eliminating_redundant_clauses_threshold: Union[int, None],
                   hp_cache_enum: hpc_enum.HypergraphPartitioningCacheEnum,
                   hp_software_enum: hps_enum.HypergraphPartitioningSoftwareEnum,
                   hp_node_weight_type_enum: hpwt_enum.HypergraphPartitioningNodeWeightEnum,
                   hp_hyperedge_weight_type_enum: hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum,
                   hp_variable_simplification_enum: hpvs_enum.HypergraphPartitioningVariableSimplificationEnum,
                   hp_patoh_sugparam_enum: hpps_enum.PatohSugparamEnum = hpps_enum.PatohSugparamEnum.QUALITY,
                   hp_multi_occurrence_cache: bool = True,
                   hp_limit_number_of_clauses_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                   hp_limit_number_of_variables_cache: Tuple[Union[int, None], Union[int, None]] = (None, None),
                   base_class_threshold: Union[int, None] = None,
                   base_class_ratio_threshold: Union[float, None] = None,
                   cut_set_try_cache: bool = False,
                   new_cut_set_threshold_reduction: float = 1,
                   implied_literals_preselection_heuristic_prop_z_depth_threshold: int = 5,
                   implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound: Union[int, None] = 10,
                   implied_literals_preselection_heuristic_cra_rank: float = 0.1,
                   first_implied_literals_preselection_heuristic_prop_z_depth_threshold: int = 5,
                   first_implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound: Union[int, None] = 10,
                   first_implied_literals_preselection_heuristic_cra_rank: float = 0.1,
                   decision_heuristic_mixed_difference_enum: mdh_enum.MixedDifferenceHeuristicEnum = mdh_enum.MixedDifferenceHeuristicEnum.OK_SOLVER,
                   decision_heuristic_vsids_d4_version: bool = True,
                   decision_heuristic_vsads_p_constant_factor: float = 1,
                   decision_heuristic_vsads_q_constant_factor: float = 0.5,
                   decision_heuristic_weight_for_satisfied_clauses: bool = True,
                   decision_heuristic_ignore_binary_clauses: bool = False,
                   decision_heuristic_renamable_horn_use_total_number_of_conflict_variables: bool = True,
                   decision_heuristic_renamable_horn_use_conflicts: bool = True,
                   decision_heuristic_renamable_horn_use_auxiliary_variables: bool = False,
                   decision_heuristic_renamable_horn_prefer_conflict_variables: bool = True,
                   decision_heuristic_maximum_renamable_horn_is_exact: bool = True,
                   decision_heuristic_maximum_renamable_horn_use_conflicts: bool = True,
                   decision_heuristic_maximum_renamable_horn_prefer_conflict_variables: bool = True,
                   decision_heuristic_maximum_renamable_horn_lp_formulation_type: lpft_enum.LpFormulationTypeEnum = lpft_enum.LpFormulationTypeEnum.HORN_FORMULA,
                   decision_heuristic_maximum_renamable_horn_weight_for_variables_not_in_cut_set: int = 2,
                   component_caching_cara_caching_scheme_multi_occurrence: bool = False,
                   component_caching_cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold: int = 50,
                   file_name_extension: str = "",
                   disable_sat: bool = False,
                   disable_decomposition: bool = False,
                   cara_circuit: bool = True,
                   strong_determinism: bool = False,
                   strong_determinism_max: Union[int, None] = None) -> \
            Tuple[bool, bool, Union[int, None], Statistics]:
        """
        :return: (timeout exceeded, exception, size of the circuit, statistics)
        """

        if file_name_extension == "":
            print(f"File name: {file_name}")
        else:
            print(f"File name: {file_name}, params: {file_name_extension}")

        # Log - directory
        file_name_temp = file_name if file_name_extension == "" else f"{file_name}_{file_name_extension}"
        directory_path_temp: Path = Path(os.path.join(self.__log_directory_path, file_name_temp))
        directory_path_temp.mkdir(exist_ok=True)

        # mapping_node_statistics
        mapping_node_statistics_temp = None
        if self.__mapping_node_statistics is not None:
            mapping_node_statistics_path: Path = Path(os.path.join(directory_path_temp, "mapping_node"))
            mapping_node_statistics_path.mkdir(exist_ok=True)

            mapping_node_statistics_temp = rf"{mapping_node_statistics_path}/{self.__mapping_node_statistics}"

        # node_statistics
        node_statistics_temp = None
        if self.__node_statistics is not None:
            node_statistics_path: Path = Path(os.path.join(directory_path_temp, "decision_node"))
            node_statistics_path.mkdir(exist_ok=True)

            node_statistics_temp = rf"{node_statistics_path}/{self.__node_statistics}"

        compiler = Compiler(cnf=file_path,
                            name=file_name,
                            smooth=smooth,
                            statistics=True,
                            preprocessing=preprocessing,
                            imbalance_factor=imbalance_factor,
                            subsumption_threshold=subsumed_threshold,
                            new_cut_set_threshold=new_cut_set_threshold,
                            decision_heuristic_enum=decision_heuristic_enum,
                            sat_solver_enum=sat_solver_enum,
                            base_class_enum_set=base_class_enum_set,
                            base_class_threshold=base_class_threshold,
                            base_class_ratio_threshold=base_class_ratio_threshold,
                            implied_literals_enum=implied_literals_enum,
                            implied_literals_preselection_heuristic_enum=implied_literals_preselection_heuristic_enum,
                            first_implied_literals_enum=first_implied_literals_enum,
                            first_implied_literals_preselection_heuristic_enum=first_implied_literals_preselection_heuristic_enum,
                            component_caching_enum=component_caching_enum,
                            component_caching_before_unit_propagation=component_caching_before_unit_propagation,
                            component_caching_after_unit_propagation=component_caching_after_unit_propagation,
                            eliminating_redundant_clauses_enum=eliminating_redundant_clauses_enum,
                            eliminating_redundant_clauses_threshold=eliminating_redundant_clauses_threshold,
                            hp_cache_enum=hp_cache_enum,
                            hp_software_enum=hp_software_enum,
                            hp_node_weight_type_enum=hp_node_weight_type_enum,
                            hp_hyperedge_weight_type_enum=hp_hyperedge_weight_type_enum,
                            hp_variable_simplification_enum=hp_variable_simplification_enum,
                            hp_patoh_sugparam_enum=hp_patoh_sugparam_enum,
                            hp_multi_occurrence_cache=hp_multi_occurrence_cache,
                            hp_limit_number_of_clauses_cache=hp_limit_number_of_clauses_cache,
                            hp_limit_number_of_variables_cache=hp_limit_number_of_variables_cache,
                            cut_set_try_cache=cut_set_try_cache,
                            new_cut_set_threshold_reduction=new_cut_set_threshold_reduction,
                            implied_literals_preselection_heuristic_prop_z_depth_threshold=implied_literals_preselection_heuristic_prop_z_depth_threshold,
                            implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound=implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound,
                            implied_literals_preselection_heuristic_cra_rank=implied_literals_preselection_heuristic_cra_rank,
                            first_implied_literals_preselection_heuristic_prop_z_depth_threshold=first_implied_literals_preselection_heuristic_prop_z_depth_threshold,
                            first_implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound=first_implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound,
                            first_implied_literals_preselection_heuristic_cra_rank=first_implied_literals_preselection_heuristic_cra_rank,
                            decision_heuristic_mixed_difference_enum=decision_heuristic_mixed_difference_enum,
                            decision_heuristic_vsids_d4_version=decision_heuristic_vsids_d4_version,
                            decision_heuristic_vsads_p_constant_factor=decision_heuristic_vsads_p_constant_factor,
                            decision_heuristic_vsads_q_constant_factor=decision_heuristic_vsads_q_constant_factor,
                            decision_heuristic_weight_for_satisfied_clauses=decision_heuristic_weight_for_satisfied_clauses,
                            decision_heuristic_ignore_binary_clauses=decision_heuristic_ignore_binary_clauses,
                            decision_heuristic_renamable_horn_use_total_number_of_conflict_variables=decision_heuristic_renamable_horn_use_total_number_of_conflict_variables,
                            decision_heuristic_renamable_horn_use_conflicts=decision_heuristic_renamable_horn_use_conflicts,
                            decision_heuristic_renamable_horn_use_auxiliary_variables=decision_heuristic_renamable_horn_use_auxiliary_variables,
                            decision_heuristic_renamable_horn_prefer_conflict_variables=decision_heuristic_renamable_horn_prefer_conflict_variables,
                            decision_heuristic_maximum_renamable_horn_is_exact=decision_heuristic_maximum_renamable_horn_is_exact,
                            decision_heuristic_maximum_renamable_horn_use_conflicts=decision_heuristic_maximum_renamable_horn_use_conflicts,
                            decision_heuristic_maximum_renamable_horn_prefer_conflict_variables=decision_heuristic_maximum_renamable_horn_prefer_conflict_variables,
                            decision_heuristic_maximum_renamable_horn_lp_formulation_type=decision_heuristic_maximum_renamable_horn_lp_formulation_type,
                            decision_heuristic_maximum_renamable_horn_weight_for_variables_not_in_cut_set=decision_heuristic_maximum_renamable_horn_weight_for_variables_not_in_cut_set,
                            component_caching_cara_caching_scheme_multi_occurrence=component_caching_cara_caching_scheme_multi_occurrence,
                            component_caching_cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold=component_caching_cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold,
                            mapping_node_statistics=mapping_node_statistics_temp,
                            node_statistics=node_statistics_temp,
                            disable_sat=disable_sat,
                            disable_decomposition=disable_decomposition,
                            cara_circuit=cara_circuit,
                            strong_determinism=strong_determinism,
                            strong_determinism_max=strong_determinism_max)

        experiment_thread: TExperimentThread = self.__ExperimentThread(compiler)
        thread = kthread.KThread(target=Experiment.__experiment, args=(experiment_thread,))
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

            self.__total_time += statistics.cnf_statistics.get_time()       # CNF
            self.__total_time += statistics.compiler_statistics.get_time()  # compiler

        # Timeout exceeded
        while thread.is_alive():
            # ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.native_id, ctypes.py_object(TimeoutError))
            thread.terminate()
            thread.join(5)

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
                print(f"Done (time: {str(statistics.compiler_statistics.get_time())}, size: {str(statistics.size)})")

        print(f"Time: {datetime.datetime.now()}")

        # Log - statistics
        statistics_path_temp: Path = Path(os.path.join(directory_path_temp, "statistics.pkl"))
        with open(statistics_path_temp, "wb") as file:
            pickle.dump(statistics, file, pickle.HIGHEST_PROTOCOL)
        statistics_path_temp: Path = Path(os.path.join(directory_path_temp, "statistics.stat"))
        with open(statistics_path_temp, "w", encoding="utf-8") as file:
            file.write(str(statistics))

        # Log - circuit
        if self.__save_circuit and (not timeout_exceeded) and (not exception):
            circuit_path_temp = Path(os.path.join(directory_path_temp, "circuit.nnf"))
            with open(circuit_path_temp, "w", encoding="utf-8") as file:
                experiment_thread.compiler.circuit.save_to_io(source=file,
                                                              mapping_node_statistics=mapping_node_statistics_temp,
                                                              node_statistics=node_statistics_temp)

        del compiler
        gc.collect()

        print("end")
        print()

        return timeout_exceeded, exception, size, statistics

    def pickle_object(self, file_name: str, object_to_save: Union[Dict]) -> None:
        path_temp: Path = Path(os.path.join(self.__log_directory_path, f"{file_name}.pkl"))
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
            warnings.warn("The directory doesn't exist!", category=UserWarning)
            return []

        return [(file, file_path) for file in os.listdir(directory_path)
                if (os.path.isfile(file_path := os.path.join(directory_path, file)))]

    @staticmethod
    def __experiment(experiment_thread: TExperimentThread):
        try:
            experiment_thread.compiler.create_circuit()
        # Timeout exceeded
        except (TimeoutError, SystemExit):
            experiment_thread.timeout_exceeded = True
        except c_exception.CaraException as err:
            experiment_thread.exception = err
    # endregion

    # region Property
    @property
    def experiment_name(self) -> str:
        return self.__experiment_name

    @property
    def log_directory_path(self) -> Path:
        return self.__log_directory_path

    @property
    def total_time(self) -> timedelta:
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
