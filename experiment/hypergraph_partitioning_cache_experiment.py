# Import
import os
import numpy as np
from pathlib import Path
from datetime import timedelta
import visualization.plot as plot
from typing import Set, Dict, List, Union, Tuple
from experiment.experiment_abstract import ExperimentAbstract
from compiler_statistics.statistics_component_timer import StatisticsComponentTimer

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
    
    Private bool save_plot
    Private bool show_plot
    Private Path plot_directory_path
    """

    # Static variable
    __KEY_DELIMITER: str = "-"

    def __init__(self, directory_path: [str, Path], timeout_experiment: Union[timedelta, None],
                 log_directory_path: Union[str, Path, None] = None, total_timeout_experiments: Union[timedelta, None] = None,
                 save_plot: bool = True, show_plot: bool = False):
        super().__init__(experiment_name="Hypergraph partitioning cache",
                         directory_path=directory_path,
                         timeout_experiment=timeout_experiment,
                         log_directory_path=log_directory_path,
                         save_circuit=False)
        self.__total_timeout_experiments: Union[timedelta, None] = total_timeout_experiments

        # Plot
        self.__save_plot: bool = save_plot
        self.__show_plot: bool = show_plot
        self.__plot_directory_path: Path = Path(os.path.join(self.log_directory_path, "plot"))

    # region Public method
    def experiment(self, limit_clause_list: List[int], limit_variable_list: List[int]):
        hp_cache_enum_list = list(zip(hpc_enum.hpc_enum_values, hpc_enum.hpc_enum_names))

        file_dictionary: Dict[str, List[Union[timedelta, None]]] = dict()
        hypergraph_partitioning_dictionary: Dict[str, List[timedelta]] = dict()
        generate_key_cache_dictionary: Dict[str, List[timedelta]] = dict()
        cache_performance_dictionary: Dict[str, List[float]] = dict()

        for file_name, file_path in self._files:
            for i_c, (hp_cache_enum, cache_name) in enumerate(hp_cache_enum_list):
                for i_lc, limit_clause in enumerate(limit_clause_list):
                    for i_lv, limit_variable in enumerate(limit_variable_list):
                        if (hp_cache_enum == hpc_enum.HypergraphPartitioningCacheEnum.NONE) and not(i_lc == 0 and i_lv == 0):
                            break

                        limit_temp = None if hp_cache_enum == hpc_enum.HypergraphPartitioningCacheEnum.NONE else (limit_clause, limit_variable)
                        key = self.__generate_key_cache(cache_name, limit_temp)     # key, file_name_extension

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
                                                                                      hp_limit_number_of_clauses_cache=(None, limit_clause),
                                                                                      hp_limit_number_of_variables_cache=(None, limit_variable),
                                                                                      file_name_extension=key)

                        # File - file_dictionary
                        if timeout_exceeded or exception:
                            result = None
                        else:
                            result = statistics.compiler_statistics.get_time()
                        if key not in file_dictionary:
                            file_dictionary[key] = []
                        file_dictionary[key].append(result)

                        def convert_none_to_0(variable):
                            return 0 if variable is None else variable

                        # Time consumed with hypergraph partitioning - hypergraph_partitioning_dictionary
                        if key not in hypergraph_partitioning_dictionary:
                            hypergraph_partitioning_dictionary[key] = []
                        hypergraph_partitioning_time = convert_none_to_0(statistics.component_statistics.get_cut_set.average_time)
                        hypergraph_partitioning_dictionary[key].append(StatisticsComponentTimer.convert_to_datetime(hypergraph_partitioning_time))

                        if hp_cache_enum != hpc_enum.HypergraphPartitioningCacheEnum.NONE:
                            # Generate key - generate_key_cache_dictionary
                            if key not in generate_key_cache_dictionary:
                                generate_key_cache_dictionary[key] = []
                            generate_key_time = convert_none_to_0(statistics.hypergraph_partitioning_statistics.generate_key_cache.average_time)
                            generate_key_cache_dictionary[key].append(StatisticsComponentTimer.convert_to_datetime(generate_key_time))

                            # Cache performance - cache_performance_dictionary
                            if key not in cache_performance_dictionary:
                                cache_performance_dictionary[key] = []
                            cache_performance = convert_none_to_0(statistics.hypergraph_partitioning_statistics.cached.average_count)
                            cache_performance_dictionary[key].append(cache_performance)

                            print(f"Cache performance: {cache_performance}")

            # Total timeout
            if self.__total_timeout_experiments is not None:
                if self.total_time >= self.__total_timeout_experiments:
                    print("Total timeout exceeded!")
                    break

        # Pickle
        self._pickle_object("file_dictionary", file_dictionary)
        self._pickle_object("hypergraph_partitioning_dictionary", hypergraph_partitioning_dictionary)
        self._pickle_object("generate_key_cache_dictionary", generate_key_cache_dictionary)
        self._pickle_object("cache_performance_dictionary", cache_performance_dictionary)

        # Plot
        if self.__save_plot or self.__show_plot:
            print("\n")
            self.__file_dictionary_plot(file_dictionary)
    # endregion

    # region Private method
    def __file_dictionary_plot(self, file_dictionary: Dict[str, List[Union[timedelta, None]]]) -> None:
        print("Plot - file_dictionary: ", end="")

        # Valid indices
        valid_index_dictionary: Dict[str, Set[int]] = dict()
        for key in file_dictionary:
            value = file_dictionary[key]
            valid_value = [i for i, v in enumerate(value) if v is not None]
            valid_index_dictionary[key] = set(valid_value)

        file_dictionary_path: Union[Path, None] = None
        if self.__save_plot:
            file_dictionary_path = Path(os.path.join(self.__plot_directory_path, "file_dictionary"))
            file_dictionary_path.mkdir(parents=True, exist_ok=True)

        key_none = self.__generate_key_cache(hp_cache_name=hpc_enum.HypergraphPartitioningCacheEnum.NONE.name, limit=None)
        value_none = file_dictionary[key_none]
        label_none = self.__key_to_label(key_none)

        count_temp = 0
        for key in file_dictionary.keys():
            if key == key_none:
                continue

            count_temp += 1

            value = file_dictionary[key]
            label = self.__key_to_label(key)

            valid_value_index_list = list(valid_index_dictionary[key].intersection(valid_index_dictionary[key_none]))

            valid_value = [t.total_seconds() for t in np.array(value)[valid_value_index_list]]
            valid_value_none = [t.total_seconds() for t in np.array(value_none)[valid_value_index_list]]

            path_temp: Union[Path, None] = None
            if self.__save_plot:
                path_temp = Path(os.path.join(file_dictionary_path, f"{key}.png"))

            plot.scatter(data_x=valid_value, data_y=valid_value_none, title=f"{label}\nvs\n{label_none}\n\nTIME [s]",
                         x_label=label, y_label=label_none, save_path=path_temp, show=self.__show_plot)

            print("|", end="" if count_temp % 10 != 0 else " ")

        print()
    # endregion

    # region Static method
    @staticmethod
    def __generate_key_cache(hp_cache_name: str, limit: Union[Tuple[int, int], None]) -> str:
        if limit is None:
            return hp_cache_name
        else:
            return HypergraphPartitioningCacheExperiment.__KEY_DELIMITER.join((hp_cache_name, str(limit[0]), str(limit[1])))

    @staticmethod
    def __key_to_label(key: str) -> str:
        temp = key.split(HypergraphPartitioningCacheExperiment.__KEY_DELIMITER)

        if len(temp) == 1:  # None
            return key

        return f"{temp[0]} (limit clauses: {temp[1]}, limit variables: {temp[2]})"
    # endregion
