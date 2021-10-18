# Import
import cara
import argparse
import warnings
import datetime
import traceback
from datetime import timedelta
import other.environment as env
from experiment.experiment import Experiment

# Import exception
import exception.cara_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.base_class_enum as bc_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.enum.component_caching_enum as cc_enum
import compiler.enum.heuristic.decision_heuristic_enum as dh_enum
import formula.enum.eliminating_redundant_clauses_enum as erc_enum
import compiler.enum.heuristic.preselection_heuristic_enum as ph_enum
import compiler.enum.heuristic.mixed_difference_heuristic_enum as mdh_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_patoh_sugparam_enum as hpps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


def main(main_args):
    if main_args.experiment_timeout is None:
        timeout_experiment = None
    else:
        timeout_experiment = timedelta(seconds=main_args.experiment_timeout)

    experiment = Experiment(experiment_name="experiment",
                            directory_path=main_args.directory_path,
                            timeout_experiment=timeout_experiment,
                            log_directory_path=main_args.log_directory_path,
                            save_circuit=False,
                            mapping_node_statistics=None,
                            node_statistics=None)

    # Total timeout
    start = datetime.datetime.now()
    if main_args.total_timeout is None:
        end = start + timedelta(days=7)
    else:
        end = start + timedelta(seconds=main_args.total_timeout)

    print("----------------------------------------------------------")
    print(f"Start: {start}")
    print(f"End: {end}")
    print("----------------------------------------------------------")
    print()

    # Hypergraph partitioning - software
    hp_software_enum = hps_enum.HypergraphPartitioningSoftwareEnum.PATOH
    if env.is_windows():
        hp_software_enum = hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS

    for i, (file_name, file_path) in enumerate(experiment._files):
        print("----------------------------------------------------------")
        print(f"{i + 1}/{len(experiment._files)}")

        try:
            experiment.experiment(file_name=file_name, file_path=file_path,

                                  decision_heuristic_ignore_binary_clauses=True,
                                  decision_heuristic_enum=dh_enum.DecisionHeuristicEnum.RENAMABLE_HORN_DLCS_DLIS,
                                  base_class_enum_set={bc_enum.BaseClassEnum.RENAMABLE_HORN_CNF},
                                  decision_heuristic_vsids_d4_version=True,
                                  decision_heuristic_vsads_p_constant_factor=1,
                                  decision_heuristic_vsads_q_constant_factor=0.5,

                                  decision_heuristic_renamable_horn_use_total_number_of_conflict_variables=True,
                                  decision_heuristic_renamable_horn_use_conflicts=True,
                                  decision_heuristic_renamable_horn_prefer_conflict_variables=True,

                                  smooth=False,
                                  preprocessing=False,
                                  imbalance_factor=0.1,
                                  subsumed_threshold=500,
                                  new_cut_set_threshold=0.1,
                                  sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
                                  implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
                                  implied_literals_preselection_heuristic_enum=ph_enum.PreselectionHeuristicEnum.NONE,
                                  first_implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
                                  first_implied_literals_preselection_heuristic_enum=ph_enum.PreselectionHeuristicEnum.NONE,
                                  component_caching_enum=cc_enum.ComponentCachingEnum.BASIC_CACHING_SCHEME,
                                  component_caching_before_unit_propagation=False,
                                  component_caching_after_unit_propagation=True,
                                  eliminating_redundant_clauses_enum=erc_enum.EliminatingRedundantClausesEnum.NONE,
                                  eliminating_redundant_clauses_threshold=None,
                                  hp_cache_enum=hpc_enum.HypergraphPartitioningCacheEnum.ISOMORFISM,
                                  hp_software_enum=hp_software_enum,
                                  hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                                  hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                                  hp_variable_simplification_enum=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL,
                                  hp_patoh_sugparam_enum=hpps_enum.PatohSugparamEnum.QUALITY,
                                  hp_multi_occurrence_cache=True,
                                  hp_limit_number_of_clauses_cache=(None, 500),
                                  hp_limit_number_of_variables_cache=(None, 500),
                                  decision_heuristic_mixed_difference_enum=mdh_enum.MixedDifferenceHeuristicEnum.OK_SOLVER,
                                  decision_heuristic_weight_for_satisfied_clauses=True,
                                  component_caching_cara_caching_scheme_multi_occurrence=False,
                                  component_caching_cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold=30)

        except (c_exception.CaraException, Exception) as err:
            print(f"An error has occurred! (see log for details)\n{str(err)}")

            stack_trace = traceback.format_exc()

            # Save the log
            with open(cara.LOG_PATH, "a", encoding="utf-8") as log_file:
                log_file.write(f"File: {file_name}\n")
                log_file.write(stack_trace)
                log_file.write("\n")

        # Total timeout
        now = datetime.datetime.now()
        now += timeout_experiment
        if now > end:
            print("Total timeout exceeded!")
            break


def create_parser() -> argparse.ArgumentParser:
    # Create the parser
    parser_temp = argparse.ArgumentParser(prog="cara_experiment.py",
                                          description="CaraCompiler - experiment",
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter     # default values are shown in the help
                                          )

    # Add arguments
    parser_temp.add_argument("directory_path",
                             action="store",
                             type=cara.directory_path_parser,
                             help="directory with experiments")
    parser_temp.add_argument("log_directory_path",
                             action="store",
                             type=cara.create_directory,
                             help="directory where the logs will be saved")
    parser_temp.add_argument("-et",
                             "--experiment_timeout",
                             action="store",
                             default=None,
                             type=cara.non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="experiment timeout [s] (None for no limit)")
    parser_temp.add_argument("-tt",
                             "--total_timeout",
                             action="store",
                             default=None,
                             type=cara.non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="total timeout [s] (None for no limit)")

    parser_temp.add_argument("-v",
                             "--version",
                             action="version",
                             version=cara.VERSION
                             )

    return parser_temp


if __name__ == "__main__":
    # Parser
    parser = create_parser()
    args = parser.parse_args()

    # Warning
    warnings.simplefilter('ignore', category=ResourceWarning)

    main(args)
