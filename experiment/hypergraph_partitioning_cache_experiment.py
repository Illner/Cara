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
    def experiment(self, limit_clause_list: List[int], limit_variable_list: List[int],
                   new_cut_set_threshold: float, cut_set_try_cache: bool, new_cut_set_threshold_reduction: float):
        hp_cache_name_list = hpc_enum.hpc_enum_names
        hp_cache_enum_list = list(zip(hpc_enum.hpc_enum_values, hp_cache_name_list))

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
                                                                                      preprocessing=False,
                                                                                      subsumed_threshold=1000,
                                                                                      new_cut_set_threshold=new_cut_set_threshold,
                                                                                      sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
                                                                                      base_class_enum_set=set(),
                                                                                      implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
                                                                                      first_implied_literals_enum=il_enum.FirstImpliedLiteralsEnum.IMPLICIT_BCP,
                                                                                      component_caching_enum=cc_enum.ComponentCachingEnum.BASIC_CACHING_SCHEME,
                                                                                      hp_cache_enum=hp_cache_enum,
                                                                                      hp_software_enum=hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS,
                                                                                      hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                                                                                      hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                                                                                      hp_variable_simplification_enum=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL,
                                                                                      hp_limit_number_of_clauses_cache=(None, limit_clause),
                                                                                      hp_limit_number_of_variables_cache=(None, limit_variable),
                                                                                      cut_set_try_cache=cut_set_try_cache,
                                                                                      new_cut_set_threshold_reduction=new_cut_set_threshold_reduction,
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

            # file_dictionary
            self.__file_dictionary_plot(file_dictionary)

            # hypergraph_partitioning_dictionary
            self.__boxplot(dictionary=hypergraph_partitioning_dictionary, hp_cache_name_list=hp_cache_name_list,
                           limit_clause_list=limit_clause_list, limit_variable_list=limit_variable_list, y_label="Time [s]",
                           title="Hypergraph partitioning (time)", directory_name="hypergraph_partitioning_dictionary")

            # generate_key_cache_dictionary
            self.__boxplot(dictionary=generate_key_cache_dictionary, hp_cache_name_list=hp_cache_name_list,
                           limit_clause_list=limit_clause_list, limit_variable_list=limit_variable_list, y_label="Time [s]",
                           title="Generate key (time)", directory_name="generate_key_cache_dictionary")

            # cache_performance_dictionary
            self.__boxplot(dictionary=cache_performance_dictionary, hp_cache_name_list=hp_cache_name_list,
                           limit_clause_list=limit_clause_list, limit_variable_list=limit_variable_list, y_label="Performance [%]",
                           title="Cache performance (%)", directory_name="cache_performance_dictionary", percentage_value=True)
    # endregion

    # region Private method
    def __file_dictionary_plot(self, file_dictionary: Dict[str, List[Union[timedelta, None]]]) -> None:
        """
        file_dictionary
        :return: None
        """

        print("Plot - file_dictionary: ", end="", flush=True)

        # Valid indices
        valid_index_dictionary: Dict[str, Set[int]] = dict()
        for key in file_dictionary:
            value = file_dictionary[key]
            valid_value = [i for i, v in enumerate(value) if v is not None]
            valid_index_dictionary[key] = set(valid_value)

        # Directory
        file_dictionary_path: Union[Path, None] = None
        if self.__save_plot:
            file_dictionary_path = Path(os.path.join(self.__plot_directory_path, "file_dictionary"))
            file_dictionary_path.mkdir(parents=True, exist_ok=True)

        # None
        key_none = self.__generate_key_cache(hp_cache_name=hpc_enum.HypergraphPartitioningCacheEnum.NONE.name, limit=None)
        value_none = file_dictionary[key_none]
        label_none = self.__key_to_label(key_none)

        count_temp = 0
        for key in file_dictionary.keys():
            if key == key_none:
                continue

            value = file_dictionary[key]
            label = self.__key_to_label(key)

            valid_value_index_list = list(valid_index_dictionary[key].intersection(valid_index_dictionary[key_none]))

            valid_value = [t.total_seconds() for t in np.array(value)[valid_value_index_list]]
            valid_value_none = [t.total_seconds() for t in np.array(value_none)[valid_value_index_list]]

            path_temp: Union[Path, None] = None
            if self.__save_plot:
                path_temp = Path(os.path.join(file_dictionary_path, f"{key}.png"))

            count_temp += 1
            plot.scatter(data_x=valid_value, data_y=valid_value_none, title=f"{label}\nvs\n{label_none}\n\nTIME [s]",
                         x_label=label, y_label=label_none, save_path=path_temp, show=self.__show_plot)
            print("|", end="" if count_temp % 10 != 0 else " ", flush=True)

        print()

    def __boxplot(self, dictionary: Union[Dict[str, List[timedelta]], Dict[str, List[float]]],
                  hp_cache_name_list: List[str], limit_clause_list: List[int], limit_variable_list: List[int],
                  y_label: str, title: str, directory_name: str, percentage_value: bool = False) -> None:
        """
        hypergraph_partitioning_dictionary, generate_key_cache_dictionary and cache_performance_dictionary
        :return: None
        """

        print(f"Plot - {directory_name}: ", end="", flush=True)

        # Directory
        dictionary_path: Union[Path, None] = None
        if self.__save_plot:
            dictionary_path = Path(os.path.join(self.__plot_directory_path, directory_name))
            dictionary_path.mkdir(parents=True, exist_ok=True)

        def convert_value_to_int(value_func: Union[List[float], List[timedelta]]):
            return [v.total_seconds() if isinstance(v, timedelta) else (v * 100 if percentage_value else v) for v in value_func]

        def replace_space(var_func: str):
            return var_func.replace(" ", "_")

        # None
        key_none = self.__generate_key_cache(hpc_enum.HypergraphPartitioningCacheEnum.NONE.name, limit=None)
        value_none, label_none = None, None
        if key_none in dictionary:
            value_none = convert_value_to_int(dictionary[key_none])
            label_none = self.__key_to_label(key_none)

        count_temp = 0

        # [iterators, names of iterators, ordering (cache, limit clause, limit variable)]
        iteration_list: List[List[List[Union[List[str], List[int]]], List[str], List[int]]] = \
            [[[hp_cache_name_list, limit_clause_list, limit_variable_list], ["cache", "limit clauses", "limit variables"], [0, 1, 2]],
             [[hp_cache_name_list, limit_variable_list, limit_clause_list], ["cache", "limit variables", "limit clauses"], [0, 2, 1]],
             [[limit_clause_list, limit_variable_list, hp_cache_name_list], ["limit clauses", "limit variables", "cache"], [2, 0, 1]],
             [[limit_variable_list, limit_clause_list, hp_cache_name_list], ["limit variables", "limit clauses", "cache"], [2, 1, 0]]]

        for iteration in iteration_list:
            for first in iteration[0][0]:
                for second in iteration[0][1]:
                    for use_none in [False] if value_none is None else [True, False]:
                        data: List[List[List[float]]] = [[value_none], []] if use_none else [[]]
                        labels: List[List[str]] = [[label_none], []] if use_none else [[]]
                        legend: List[str] = [label_none] if use_none else []

                        # Group
                        for third in iteration[0][2]:
                            temp = [first, second, third]

                            cache_name = temp[iteration[2][0]]
                            limit_clause = temp[iteration[2][1]]
                            limit_variable = temp[iteration[2][2]]

                            if cache_name == hpc_enum.HypergraphPartitioningCacheEnum.NONE.name:
                                continue

                            key = self.__generate_key_cache(cache_name, (limit_clause, limit_variable))
                            value = convert_value_to_int(dictionary[key])

                            data[-1].append(value)
                            labels[-1].append(str(third))

                        # Because of None
                        if (labels == [[label_none], []]) or (labels == [[]]):
                            continue

                        legend_temp = f"{iteration[1][0]}: {str(first)}, {iteration[1][1]}: {str(second)}"
                        legend.append(legend_temp)

                        path_temp: Union[Path, None] = None
                        if self.__save_plot:
                            temp = f"_with_{label_none}" if use_none else ""
                            path_temp = Path(os.path.join(dictionary_path,
                                                          f"{replace_space(iteration[1][0])}_{str(first)}_{replace_space(iteration[1][1])}_{str(second)}{temp}.png"))

                        title_temp = "\n".join((title, legend_temp))

                        count_temp += 1
                        plot.boxplot(data=data, labels=labels, title=title_temp, x_label=(iteration[1][2]).capitalize(), y_label=y_label,
                                     legend=legend, save_path=path_temp, show=self.__show_plot)
                        print("|", end="" if count_temp % 10 != 0 else " ", flush=True)

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
