# Import
import os
import pickle
from pathlib import Path
from datetime import timedelta
from typing import Dict, List, Union
from experiment.experiment_abstract import ExperimentAbstract
from compiler_statistics.statistics_component_counter import StatisticsComponentCounter

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.component_caching.component_caching_enum as cc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


class HypergraphPartitioningCacheExperiment(ExperimentAbstract):
    """
    Hypergraph partitioning cache - experiment
    """

    """
    Private timedelta total_timeout_experiments
    """

    def __init__(self, directory_path: [str, Path], timeout_experiment: Union[timedelta, None],
                 log_directory_path: Union[str, Path, None] = None, total_timeout_experiments: Union[timedelta, None] = None):
        super().__init__(experiment_name="Hypergraph partitioning cache",
                         directory_path=directory_path,
                         timeout_experiment=timeout_experiment,
                         log_directory_path=log_directory_path,
                         save_circuit=False)
        self.__total_timeout_experiments: Union[timedelta, None] = total_timeout_experiments

    # region Public method
    def experiment(self):
        hp_cache_enum_value_list = hpc_enum.hpc_enum_values
        hp_cache_enum_name_list = hpc_enum.hpc_enum_names
        limit_list = [100, 200, 300, 400, 500]

        file_dictionary: Dict[str, List[Union[timedelta, None]]] = dict()
        cache_performance_dictionary: Dict[str, StatisticsComponentCounter] = dict()

        for file_name, file_path in self._files:
            for i_c, hp_cache_enum in enumerate(hp_cache_enum_value_list):
                for i_l, limit in enumerate(limit_list):
                    cache_name = hp_cache_enum_name_list[i_c]
                    file_name_extension = cache_name if hp_cache_enum == hpc_enum.HypergraphPartitioningCacheEnum.NONE else f"{cache_name}_{limit}"

                    if (hp_cache_enum == hpc_enum.HypergraphPartitioningCacheEnum.NONE) and (i_l > 0):
                        break

                    limit_temp = None if hp_cache_enum == hpc_enum.HypergraphPartitioningCacheEnum.NONE else limit
                    key = self.__generate_key_cache(cache_name, limit_temp)

                    timeout_exceeded, exception, _, statistics = self._experiment(file_name=file_name, file_path=file_path,
                                                                                  smooth=False,
                                                                                  ub_factor=0.1,
                                                                                  subsumed_threshold=1000,
                                                                                  new_cut_set_threshold=0.1,
                                                                                  sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
                                                                                  implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
                                                                                  component_caching_enum=cc_enum.ComponentCachingEnum.BASIC_CACHING_SCHEME,
                                                                                  hp_cache_enum=hp_cache_enum,
                                                                                  hp_software_enum=hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS,
                                                                                  hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                                                                                  hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                                                                                  hp_variable_simplification_enum=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL,
                                                                                  hp_limit_number_of_clauses_cache=(None, limit),
                                                                                  hp_limit_number_of_variables_cache=(None, limit),
                                                                                  file_name_extension=file_name_extension)

                    # Files
                    if timeout_exceeded or exception:
                        result = None
                    else:
                        result = statistics.compiler_statistics.get_time()
                    if key not in file_dictionary:
                        file_dictionary[key] = []
                    file_dictionary[key].append(result)

                    # Cache performance
                    if hp_cache_enum != hpc_enum.HypergraphPartitioningCacheEnum.NONE:
                        if key not in cache_performance_dictionary:
                            cache_performance_dictionary[key] = StatisticsComponentCounter(f"cache performance {cache_name} {limit}")
                        cache_performance = statistics.hypergraph_partitioning_statistics.cached.average_count
                        cache_performance = 0 if cache_performance is None else cache_performance
                        cache_performance_dictionary[key].add_count(cache_performance)

                        print(f"Cache performance: {cache_performance}")

            # Total timeout
            if self.__total_timeout_experiments is not None:
                if self.total_time >= self.__total_timeout_experiments:
                    print("Total timeout exceeded!")
                    break

        # file_dictionary - pickle
        file_dictionary_path_temp: Path = Path(os.path.join(self.log_directory_path, "file_dictionary.pkl"))
        with open(file_dictionary_path_temp, "wb") as file:
            pickle.dump(file_dictionary, file, pickle.HIGHEST_PROTOCOL)

        # cache_performance_dictionary - pickle
        cache_performance_dictionary_path_temp: Path = Path(os.path.join(self.log_directory_path, "cache_performance_dictionary.pkl"))
        with open(cache_performance_dictionary_path_temp, "wb") as file:
            pickle.dump(cache_performance_dictionary, file, pickle.HIGHEST_PROTOCOL)
    # endregion

    # region Static method
    @staticmethod
    def __generate_key_cache(hp_cache_name: str, limit: Union[int, None]) -> str:
        if limit is None:
            return hp_cache_name
        else:
            return "-".join((hp_cache_name, str(limit)))
    # endregion
