from datetime import timedelta
from experiment.hypergraph_partitioning_cache_experiment import HypergraphPartitioningCacheExperiment

directory_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\temp\Cache"
timeout_experiment = timedelta(seconds=50)
total_timeout_experiments = None # timedelta(hours=9)

e = HypergraphPartitioningCacheExperiment(directory_path=directory_path, timeout_experiment=timeout_experiment, total_timeout_experiments=total_timeout_experiments)
e.experiment()
