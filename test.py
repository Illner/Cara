from datetime import timedelta
from experiment.hypergraph_partitioning_cache_experiment import HypergraphPartitioningCacheExperiment

directory_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\temp\Temp"
timeout_experiment = timedelta(minutes=10)
total_timeout_experiments = timedelta(hours=13)

e = HypergraphPartitioningCacheExperiment(directory_path=directory_path, timeout_experiment=timeout_experiment, total_timeout_experiments=total_timeout_experiments,
                                          save_plot=True, show_plot=False)

limit_clause_list = [100, 300, 500, 700]
limit_variable_list = [100, 300, 500, 700]

e.experiment(limit_clause_list, limit_variable_list)
