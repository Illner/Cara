# Import
from pathlib import Path
from datetime import timedelta
from typing import Dict, List, Union, Tuple
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
        limit_clause_list = [100, 300, 500, 700]
        limit_variable_list = [100, 300, 500, 700]

        file_dictionary: Dict[str, List[Union[timedelta, None]]] = dict()
        hypergraph_partitioning_dictionary: Dict[str, List[Union[timedelta]]] = dict()
        generate_key_cache_dictionary: Dict[str, List[Union[timedelta]]] = dict()
        cache_performance_dictionary: Dict[str, List[Union[float]]] = dict()

        for file_name, file_path in self._files:
            for i_c, hp_cache_enum in enumerate(hp_cache_enum_value_list):
                for i_lc, limit_clause in enumerate(limit_clause_list):
                    for i_lv, limit_variable in enumerate(limit_variable_list):
                        cache_name = hp_cache_enum_name_list[i_c]

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
    # endregion

    # region Static method
    @staticmethod
    def __generate_key_cache(hp_cache_name: str, limit: Union[Tuple[int, int], None]) -> str:
        if limit is None:
            return hp_cache_name
        else:
            return "_".join((hp_cache_name, str(limit[0]), str(limit[1])))
    # endregion
