# Import
import cara
import argparse
import warnings
import traceback
import other.environment as env
from compiler.compiler import Compiler

# Import exception
import exception.cara_exception as c_exception

# Import enum
import compiler.enum.sat_solver_enum as ss_enum
import compiler.enum.implied_literals_enum as il_enum
import compiler.enum.component_caching_enum as cc_enum
import compiler.enum.heuristic.decision_heuristic_enum as dh_enum
import formula.enum.eliminating_redundant_clauses_enum as erc_enum
import compiler.enum.heuristic.preselection_heuristic_enum as ph_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_cache_enum as hpc_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_weight_type_enum as hpwt_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_patoh_sugparam_enum as hpps_enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_variable_simplification_enum as hpvs_enum


def main(main_args):
    try:
        print("Processing...")

        compiler = Compiler(cnf=main_args.input_file,
                            smooth=main_args.smooth,
                            statistics=main_args.statistics,
                            preprocessing=False,
                            imbalance_factor=0.20,
                            subsumption_threshold=500,
                            new_cut_set_threshold=0.1,
                            decision_heuristic_enum=dh_enum.DecisionHeuristicEnum.VSADS,
                            sat_solver_enum=ss_enum.SatSolverEnum.MiniSAT,
                            base_class_enum_set=set(),
                            implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
                            implied_literals_preselection_heuristic_enum=ph_enum.PreselectionHeuristicEnum.NONE,
                            first_implied_literals_enum=il_enum.ImpliedLiteralsEnum.BCP,
                            first_implied_literals_preselection_heuristic_enum=ph_enum.PreselectionHeuristicEnum.NONE,
                            component_caching_enum=cc_enum.ComponentCachingEnum.BASIC_CACHING_SCHEME,
                            component_caching_before_unit_propagation=False,
                            component_caching_after_unit_propagation=True,
                            eliminating_redundant_clauses_enum=erc_enum.EliminatingRedundantClausesEnum.NONE,
                            eliminating_redundant_clauses_threshold=None,
                            hp_cache_enum=hpc_enum.HypergraphPartitioningCacheEnum.NONE,
                            hp_software_enum=hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS if env.is_windows() else hps_enum.HypergraphPartitioningSoftwareEnum.PATOH,
                            hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                            hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                            hp_variable_simplification_enum=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL,
                            hp_patoh_sugparam_enum=hpps_enum.PatohSugparamEnum.QUALITY,
                            decision_heuristic_vsids_d4_version=True,
                            decision_heuristic_vsads_p_constant_factor=1,
                            decision_heuristic_vsads_q_constant_factor=1)
        print("The formula has been processed!\n")

        print("Compiling...")
        compiler.create_circuit()
        print("The circuit has been compiled!")

        circuit = compiler.circuit
        statistics = compiler.statistics
        print(f"Time: {statistics.compiler_statistics.get_time()}\n")

        print("Generating file(s)...")
        # Circuit
        with open(main_args.output_file, "w", encoding="utf-8") as file:
            circuit.save_to_io(file)

        # Statistics
        if main_args.statistics:
            statistics_file = main_args.output_file + ".stat"
            with open(statistics_file, "w", encoding="utf-8") as file:
                file.write(str(statistics))

        if main_args.statistics:
            print("The files have been generated!")
        else:
            print("The file has been generated!")
    except (c_exception.CaraException, Exception) as err:
        print(f"An error has occurred! (see log for details)\n{str(err)}")

        stack_trace = traceback.format_exc()

        # Save the log
        with open(cara.LOG_PATH, "w", encoding="utf-8") as log_file:
            log_file.write(stack_trace)


def create_parser() -> argparse.ArgumentParser:
    # Create the parser
    parser_temp = argparse.ArgumentParser(prog="d4.py",
                                          description="D4 compiler",
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter     # default values are shown in the help
                                          )

    # Add arguments
    parser_temp.add_argument("input_file",
                             action="store",
                             type=cara.input_file_path_parser,
                             help="path of the input file, which is in the DIMACS CNF format")
    parser_temp.add_argument("output_file",
                             action="store",
                             type=cara.output_file_path_parser,
                             help="path of the output file, where the circuit will be saved in the DIMACS NNF format")
    parser_temp.add_argument("-s",
                             "--smooth",
                             action="store_true",
                             default=False,
                             help="smooth the circuit")
    parser_temp.add_argument("-stat",
                             "--statistics",
                             action="store_true",
                             default=False,
                             help="generate statistics")

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
