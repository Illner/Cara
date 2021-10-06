# Import
import os
import argparse
import warnings
import traceback
from pathlib import Path
from typing import Union
import other.environment as env
from compiler.compiler import Compiler

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

# Static variable - Path
LOG_PATH = os.path.join(os.getcwd(), "log")

# Constant
VERSION = "12.8"


def main(main_args):
    try:
        print_logo()

        print("Processing...")

        base_class_list = [] if main_args.base_class is None else main_args.base_class
        mapping_node_statistics = None if not main_args.mapping_node_statistics else main_args.output_file
        node_statistics = None if not main_args.node_statistics else main_args.output_file

        compiler = Compiler(cnf=main_args.input_file,
                            smooth=main_args.smooth,
                            statistics=main_args.statistics,
                            preprocessing=main_args.preprocessing,
                            imbalance_factor=main_args.hp_imbalance_factor,
                            subsumption_threshold=main_args.subsumption_threshold,
                            new_cut_set_threshold=main_args.new_cut_set_threshold,
                            decision_heuristic_enum=dh_enum.DecisionHeuristicEnum[main_args.decision_heuristic],
                            sat_solver_enum=ss_enum.SatSolverEnum[main_args.sat_solver],
                            base_class_enum_set=set([bc_enum.BaseClassEnum[base_class] for base_class in base_class_list]),
                            base_class_threshold=main_args.bc_threshold,
                            implied_literals_enum=il_enum.ImpliedLiteralsEnum[main_args.implied_literals],
                            implied_literals_preselection_heuristic_enum=ph_enum.PreselectionHeuristicEnum[main_args.il_preselection_heuristic],
                            first_implied_literals_enum=il_enum.ImpliedLiteralsEnum[main_args.first_implied_literals],
                            first_implied_literals_preselection_heuristic_enum=ph_enum.PreselectionHeuristicEnum[main_args.fil_preselection_heuristic],
                            component_caching_enum=cc_enum.ComponentCachingEnum[main_args.component_caching],
                            component_caching_before_unit_propagation=main_args.cc_before_bcp,
                            component_caching_after_unit_propagation=main_args.cc_after_bcp,
                            eliminating_redundant_clauses_enum=erc_enum.EliminatingRedundantClausesEnum[main_args.eliminating_redundant_clauses],
                            eliminating_redundant_clauses_threshold=main_args.erc_threshold,
                            hp_cache_enum=hpc_enum.HypergraphPartitioningCacheEnum[main_args.hp_caching],
                            hp_software_enum=hps_enum.HypergraphPartitioningSoftwareEnum[main_args.hp_software],
                            hp_node_weight_type_enum=hpwt_enum.HypergraphPartitioningNodeWeightEnum.NONE,
                            hp_hyperedge_weight_type_enum=hpwt_enum.HypergraphPartitioningHyperedgeWeightEnum.NONE,
                            hp_variable_simplification_enum=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum[main_args.hp_variable_simplification],
                            hp_patoh_sugparam_enum=hpps_enum.PatohSugparamEnum[main_args.hp_patoh_sugparam],
                            hp_multi_occurrence_cache=not main_args.hp_cache_remove_multi_occurrent_clauses,
                            hp_limit_number_of_clauses_cache=(None, main_args.hp_limit_number_of_clauses),
                            hp_limit_number_of_variables_cache=(None, main_args.hp_limit_number_of_variables),
                            cut_set_try_cache=main_args.cut_set_try_cache,
                            new_cut_set_threshold_reduction=main_args.new_cut_set_threshold_reduction,
                            implied_literals_preselection_heuristic_prop_z_depth_threshold=main_args.il_ph_prop_z_depth_threshold,
                            implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound=main_args.il_ph_prop_z_number_of_variables_lower_bound,
                            implied_literals_preselection_heuristic_cra_rank=main_args.il_ph_cra_rank,
                            first_implied_literals_preselection_heuristic_prop_z_depth_threshold=main_args.fil_ph_prop_z_depth_threshold,
                            first_implied_literals_preselection_heuristic_prop_z_number_of_variables_lower_bound=main_args.fil_ph_prop_z_number_of_variables_lower_bound,
                            first_implied_literals_preselection_heuristic_cra_rank=main_args.fil_ph_cra_rank,
                            decision_heuristic_mixed_difference_enum=mdh_enum.MixedDifferenceHeuristicEnum[main_args.dh_mixed_difference_heuristic],
                            decision_heuristic_vsids_d4_version=main_args.dh_vsids_d4_version,
                            decision_heuristic_vsads_p_constant_factor=main_args.dh_vsads_p_factor,
                            decision_heuristic_vsads_q_constant_factor=main_args.dh_vsads_q_factor,
                            decision_heuristic_weight_for_satisfied_clauses=main_args.dh_weight_for_satisfied_clauses,
                            decision_heuristic_ignore_binary_clauses=main_args.dh_ignore_binary_clauses,
                            decision_heuristic_preselection_heuristic_enum=ph_enum.PreselectionHeuristicEnum[main_args.dh_preselection_heuristic],
                            decision_heuristic_preselection_heuristic_prop_z_depth_threshold=main_args.dh_ph_prop_z_depth_threshold,
                            decision_heuristic_preselection_heuristic_prop_z_number_of_variables_lower_bound=main_args.dh_ph_prop_z_number_of_variables_lower_bound,
                            decision_heuristic_preselection_heuristic_cra_rank=main_args.dh_ph_cra_rank,
                            component_caching_cara_caching_scheme_multi_occurrence=not main_args.cc_cara_caching_scheme_remove_multi_occurrent_clauses,
                            component_caching_cara_caching_scheme_basic_caching_scheme_number_of_variables_threshold=main_args.cc_cara_caching_scheme_number_of_variables_threshold,
                            mapping_node_statistics=mapping_node_statistics,
                            node_statistics=node_statistics)

        print("The formula has been processed!\n")

        print("Compiling...")
        compiler.create_circuit()
        print("The circuit has been compiled!")

        circuit = compiler.circuit
        statistics = compiler.statistics
        print(f"Time: {statistics.compiler_statistics.get_time()}")
        print(f"Size: {statistics.size}\n")

        print("Generating file(s)...")
        # Circuit
        with open(main_args.output_file, "w", encoding="utf-8") as file:
            circuit.save_to_io(source=file,
                               mapping_node_statistics=mapping_node_statistics,
                               node_statistics=node_statistics)

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
        with open(LOG_PATH, "w", encoding="utf-8") as log_file:
            log_file.write(stack_trace)


def print_logo() -> None:
    text = "CaraCompiler"

    print(f"-----{'-' * len(text)}-----")
    print(f"---- {text} ----")
    print(f"-----{'-' * len(text)}-----")

    print()


def directory_path_parser(path: str) -> str:
    """
    Check if the directory exists
    :param path: the path of the directory
    :return: the path
    :raises ArgumentTypeError: if the directory does not exist
    """

    path_temp = Path(path)

    if not path_temp.is_dir():
        raise argparse.ArgumentTypeError(f"The directory ({path}) doesn't exist!")

    return path


def create_directory(path: str) -> str:
    """
    Create the directory
    :param path: the path of the directory
    :return: the path
    """

    path_temp = Path(path)

    path_temp.mkdir(parents=True, exist_ok=True)

    return path


def input_file_path_parser(path: str) -> str:
    """
    Check if the input file exists and try to open it
    :param path: the path of the input file
    :return: the path
    :raises ArgumentTypeError: if the input file does not exist or cannot be opened
    """

    path_temp = Path(path)

    # The input file does not exist
    if not path_temp.exists():
        raise argparse.ArgumentTypeError(f"The input file ({path}) doesn't exist!")

    try:
        with open(path_temp, "r", encoding="utf-8") as _:
            pass
    except Exception as err:
        raise argparse.ArgumentTypeError(f"The input file ({path}) cannot be opened! ({str(err)})")

    return path


def output_file_path_parser(path: str) -> str:
    """
    Try to create an empty output file
    :param path: the path of the output file
    :return: the path
    :raises ArgumentTypeError: if the output file creation fails, or the output file already exists
    """

    path_temp = Path(path)

    # The output file already exists
    if path_temp.exists():
        raise argparse.ArgumentTypeError(f"The output file ({path}) already exists. Please delete it or choose another name for the output file!")

    try:
        with open(path_temp, "w", encoding="utf-8") as _:
            pass
    except Exception as err:
        raise argparse.ArgumentTypeError(f"An error occurred while trying to create the output file ({path})! ({str(err)})")

    # Check if the output file has been created
    if path_temp.exists():
        path_temp.unlink()
        return path

    raise argparse.ArgumentTypeError(f"An error occurred while trying to create the output file ({path})!")


def str_to_bool_parser(value: Union[str, bool]) -> bool:
    """
    Convert a string to boolean
    :param value: a string that will be converted to boolean
    :return: boolean
    :raises ArgumentTypeError: if the value cannot be converted to boolean
    """

    # Boolean
    if isinstance(value, bool):
        return value

    if value.lower() in ['yes', 'true', 't', 'y', '1']:
        return True
    elif value.lower() in ['no', 'false', 'f', 'n', '0']:
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected!')


def non_negative_int_or_none_parser(value: Union[int, str]) -> Union[int, None]:
    """
    Check if the value is a (non-negative) number or None
    :raises ArgumentTypeError: if the value has an invalid type
    """

    # None
    if isinstance(value, str) and value.lower() == "none":
        return None

    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} has an invalid type ({type(value)}), expected int or \"None\"!")

    # Number
    if value < 0:
        raise argparse.ArgumentTypeError(f"{value} is negative!")

    return value


def non_negative_int_parser(value: Union[int, str]) -> int:
    # None
    if isinstance(value, str) and value.lower() == "none":
        raise argparse.ArgumentTypeError(f"{value} has an invalid type ({type(value)}), expected int!")

    return non_negative_int_or_none_parser(value)


def create_parser() -> argparse.ArgumentParser:
    # Create the parser
    parser_temp = argparse.ArgumentParser(prog="cara.py",
                                          description="Backdoor Decomposable Monotone Circuits (BDMC) compiler",
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter     # default values are shown in the help
                                          )

    hp_software_default = hps_enum.HypergraphPartitioningSoftwareEnum.PATOH
    if env.is_windows():
        hp_software_default = hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS

    # Add arguments
    parser_temp.add_argument("input_file",
                             action="store",
                             type=input_file_path_parser,
                             help="path of the input file, which is in the DIMACS CNF format")
    parser_temp.add_argument("output_file",
                             action="store",
                             type=output_file_path_parser,
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
    parser_temp.add_argument("-mn_stat",
                             "--mapping_node_statistics",
                             action="store_true",
                             default=False,
                             help="generate mapping node statistics")
    parser_temp.add_argument("-n_stat",
                             "--node_statistics",
                             action="store_true",
                             default=False,
                             help="generate node statistics")
    parser_temp.add_argument("-p",
                             "--preprocessing",
                             action="store_true",
                             default=False,
                             help="find all backbone literals before the compilation")
    parser_temp.add_argument("-dh_ibc",
                             "--dh_ignore_binary_clauses",
                             action="store_true",
                             default=False,
                             help="binary clauses will be ignored in the decision heuristic (Jeroslow-Wang, DLCS, DLIS, DLCS-DLIS, VSADS)")
    parser_temp.add_argument("-cc_bbcp",
                             "--cc_before_bcp",
                             action="store",
                             default=False,
                             type=str_to_bool_parser,
                             metavar="[True, False]",
                             help="use component caching before BCP")
    parser_temp.add_argument("-cc_abcp",
                             "--cc_after_bcp",
                             action="store",
                             default=True,
                             type=str_to_bool_parser,
                             metavar="[True, False]",
                             help="use component caching after BCP")
    parser_temp.add_argument("-hp_c_rmoc",
                             "--hp_cache_remove_multi_occurrent_clauses",
                             action="store",
                             default=False,
                             type=str_to_bool_parser,
                             metavar="[True, False]",
                             help="multi-occurrent clauses will be removed during the hypergraph caching (ISOMORFISM, ISOMORFISM_VARIANCE)")
    parser_temp.add_argument("-cc_ccs_rmoc",
                             "--cc_cara_caching_scheme_remove_multi_occurrent_clauses",
                             action="store",
                             default=True,
                             type=str_to_bool_parser,
                             metavar="[True, False]",
                             help="multi-occurrent clauses will be removed during the component caching (cara caching scheme)")
    parser_temp.add_argument("-cc_ccs_novt",
                             "--cc_cara_caching_scheme_number_of_variables_threshold",
                             action="store",
                             default=0,
                             type=non_negative_int_parser,
                             metavar="[non-negative number]",
                             help="if a subformula has at most x variables, the basic caching scheme will be used (cara caching scheme)")
    parser_temp.add_argument("-bc",
                             "--base_class",
                             action="append",
                             type=str,
                             choices=bc_enum.base_class_enum_names,
                             help="types of base classes in the circuit's leaves (literal leaves are mandatory)")
    parser_temp.add_argument("-bc_t",
                             "--bc_threshold",
                             action="store",
                             default=None,
                             type=non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="threshold (formula length) for applying base classes (None for no limit)")
    parser_temp.add_argument("-dh",
                             "--decision_heuristic",
                             action="store",
                             default=dh_enum.DecisionHeuristicEnum.JEROSLOW_WANG_TWO_SIDED.name,
                             type=str,
                             choices=dh_enum.decision_heuristic_enum_names,
                             help="type of decision heuristic")
    parser_temp.add_argument("-dh_mdh",
                             "--dh_mixed_difference_heuristic",
                             action="store",
                             default=mdh_enum.MixedDifferenceHeuristicEnum.OK_SOLVER.name,
                             type=str,
                             choices=mdh_enum.mixed_difference_heuristic_enum_names,
                             help="type of mixed difference heuristic for the decision heuristic (clause reduction heuristic, weighted binaries heuristic, backbone search heuristic and exact unit propagation count heuristic)")
    parser_temp.add_argument("-dh_vsids_d4",
                             "--dh_vsids_d4_version",
                             action="store",
                             default=True,
                             type=str_to_bool_parser,
                             metavar="[True, False]",
                             help="use \"D4 version\" of VSIDS score for the decision heuristic (VSIDS, VSADS)")
    parser_temp.add_argument("-dh_vsads_p_f",
                             "--dh_vsads_p_factor",
                             action="store",
                             default=1,
                             type=float,
                             metavar="[non-negative number]",
                             help="constant factor p (VSADS)")
    parser_temp.add_argument("-dh_vsads_q_f",
                             "--dh_vsads_q_factor",
                             action="store",
                             default=0.5,
                             type=float,
                             metavar="[non-negative number]",
                             help="constant factor q (VSADS)")
    parser_temp.add_argument("-dh_wfsc",
                             "--dh_weight_for_satisfied_clauses",
                             action="store",
                             default=True,
                             type=str_to_bool_parser,
                             metavar="[True, False]",
                             help="use a weight for satisfied clauses (clause reduction heuristic, weighted binaries heuristic, backbone search heuristic)")
    parser_temp.add_argument("-dh_ph",
                             "--dh_preselection_heuristic",
                             action="store",
                             default=ph_enum.PreselectionHeuristicEnum.NONE.name,
                             type=str,
                             choices=ph_enum.preselection_heuristic_enum_names,
                             help="type of preselection heuristic for the decision heuristic")
    parser_temp.add_argument("-dh_ph_cra_r",
                             "--dh_ph_cra_rank",
                             action="store",
                             default=0.1,
                             type=float,
                             metavar="[0.01-1.00]",
                             help="how many variables should be preselected (clause reduction approximation - rank)")
    parser_temp.add_argument("-dh_ph_prop_z_novlb",
                             "--dh_ph_prop_z_number_of_variables_lower_bound",
                             action="store",
                             default=10,
                             type=non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="how many variables should be preselected (prop_z - lower bound) (None for no limit)")
    parser_temp.add_argument("-dh_ph_prop_z_dt",
                             "--dh_ph_prop_z_depth_threshold",
                             action="store",
                             default=5,
                             type=non_negative_int_parser,
                             metavar="[non-negative number]",
                             help="depth threshold (prop_z)")
    parser_temp.add_argument("-hp_if",
                             "--hp_imbalance_factor",
                             action="store",
                             default=0.1,
                             type=float,
                             metavar="[0.01-0.49]",
                             help="imbalance factor that is used for hypergraph partitioning (hMETIS - UBfactor, PaToH - final_imbal, KaHyPar - epsilon)")
    parser_temp.add_argument("-st",
                             "--subsumption_threshold",
                             action="store",
                             default=500,
                             type=non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="threshold (number of clauses) for applying subsumption (None for no limit)")
    parser_temp.add_argument("-ncst",
                             "--new_cut_set_threshold",
                             action="store",
                             default=0.1,
                             type=float,
                             metavar="[0.00-1.00]",
                             help="threshold for computing a new cut set (if the number of implied literals is at least x per cent of the component's number of variables)")
    parser_temp.add_argument("-ss",
                             "--sat_solver",
                             action="store",
                             default=ss_enum.SatSolverEnum.MiniSAT.name,
                             type=str,
                             choices=ss_enum.sat_solver_enum_names,
                             help="type of SAT solver that will be used for compiling the circuit")
    parser_temp.add_argument("-il",
                             "--implied_literals",
                             action="store",
                             default=il_enum.ImpliedLiteralsEnum.BCP.name,
                             type=str,
                             choices=il_enum.implied_literals_enum_names,
                             help="type of method that will be used for deriving implied literals at every decision node")
    parser_temp.add_argument("-il_ph",
                             "--il_preselection_heuristic",
                             action="store",
                             default=ph_enum.PreselectionHeuristicEnum.CRA.name,
                             type=str,
                             choices=ph_enum.preselection_heuristic_enum_names,
                             help="type of preselection heuristic for implied literals (relevant only for IMPLICIT_BCP and IMPLICIT_BCP_ITERATION)")
    parser_temp.add_argument("-il_ph_cra_r",
                             "--il_ph_cra_rank",
                             action="store",
                             default=0.1,
                             type=float,
                             metavar="[0.01-1.00]",
                             help="how many variables should be preselected (clause reduction approximation - rank)")
    parser_temp.add_argument("-il_ph_prop_z_novlb",
                             "--il_ph_prop_z_number_of_variables_lower_bound",
                             action="store",
                             default=10,
                             type=non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="how many variables should be preselected (prop_z - lower bound) (None for no limit)")
    parser_temp.add_argument("-il_ph_prop_z_dt",
                             "--il_ph_prop_z_depth_threshold",
                             action="store",
                             default=5,
                             type=non_negative_int_parser,
                             metavar="[non-negative number]",
                             help="depth threshold (prop_z)")
    parser_temp.add_argument("-fil",
                             "--first_implied_literals",
                             action="store",
                             default=il_enum.ImpliedLiteralsEnum.BCP.name,
                             type=str,
                             choices=il_enum.implied_literals_enum_names,
                             help="type of method that will be used for deriving implied literals after each component decomposition")
    parser_temp.add_argument("-fil_ph",
                             "--fil_preselection_heuristic",
                             action="store",
                             default=ph_enum.PreselectionHeuristicEnum.CRA.name,
                             type=str,
                             choices=ph_enum.preselection_heuristic_enum_names,
                             help="type of preselection heuristic for first implied literals (relevant only for IMPLICIT_BCP and IMPLICIT_BCP_ITERATION)")
    parser_temp.add_argument("-fil_ph_cra_r",
                             "--fil_ph_cra_rank",
                             action="store",
                             default=0.1,
                             type=float,
                             metavar="[0.01-1.00]",
                             help="how many variables should be preselected (clause reduction approximation - rank)")
    parser_temp.add_argument("-fil_ph_prop_z_novlb",
                             "--fil_ph_prop_z_number_of_variables_lower_bound",
                             action="store",
                             default=10,
                             type=non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="how many variables should be preselected (prop_z - lower bound) (None for no limit)")
    parser_temp.add_argument("-fil_ph_prop_z_dt",
                             "--fil_ph_prop_z_depth_threshold",
                             action="store",
                             default=5,
                             type=non_negative_int_parser,
                             metavar="[non-negative number]",
                             help="depth threshold (prop_z)")
    parser_temp.add_argument("-cc",
                             "--component_caching",
                             action="store",
                             default=cc_enum.ComponentCachingEnum.BASIC_CACHING_SCHEME.name,
                             type=str,
                             choices=cc_enum.component_caching_enum_names,
                             help="type of component caching that will be used for compiling the circuit")
    parser_temp.add_argument("-erc",
                             "--eliminating_redundant_clauses",
                             action="store",
                             default=erc_enum.EliminatingRedundantClausesEnum.NONE.name,
                             type=str,
                             choices=erc_enum.eliminating_redundant_clauses_enum_names,
                             help="procedure that will be applied for determining redundant clauses")
    parser_temp.add_argument("-erc_t",
                             "--erc_threshold",
                             action="store",
                             default=None,
                             type=non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="threshold (number of clauses) for applying a procedure that eliminates redundant clauses (None for no limit)")
    parser_temp.add_argument("-hp_s",
                             "--hp_software",
                             action="store",
                             default=hp_software_default.name,
                             type=str,
                             choices=hps_enum.hps_enum_names,
                             help="software used for hypergraph partitioning")
    parser_temp.add_argument("-hp_c",
                             "--hp_caching",
                             action="store",
                             default=hpc_enum.HypergraphPartitioningCacheEnum.ISOMORFISM.name,
                             type=str,
                             choices=hpc_enum.hpc_enum_names,
                             help="type of hypergraph partitioning caching")
    parser_temp.add_argument("-hp_lnc",
                             "--hp_limit_number_of_clauses",
                             action="store",
                             default=1000,
                             type=non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="threshold (number of clauses) for applying hypergraph partitioning caching (None for no limit)")
    parser_temp.add_argument("-hp_lnv",
                             "--hp_limit_number_of_variables",
                             action="store",
                             default=1000,
                             type=non_negative_int_or_none_parser,
                             metavar="[non-negative number or None]",
                             help="threshold (number of variables) for applying hypergraph partitioning caching (None for no limit)")
    parser_temp.add_argument("-cstc",
                             "--cut_set_try_cache",
                             action="store_true",
                             default=False,
                             help="compute a new cut set at every decision node that satisfies the limits for hypergraph partitioning caching (number of clauses/variables)")
    parser_temp.add_argument("-hp_vs",
                             "--hp_variable_simplification",
                             action="store",
                             default=hpvs_enum.HypergraphPartitioningVariableSimplificationEnum.EQUIV_SIMPL.name,
                             type=str,
                             choices=hpvs_enum.hpvs_enum_names,
                             help="type of hypergraph partitioning variable simplification")
    parser_temp.add_argument("-hp_patoh_s",
                             "--hp_patoh_sugparam",
                             action="store",
                             default=hpps_enum.PatohSugparamEnum.QUALITY.name,
                             type=str,
                             choices=hpps_enum.patoh_sugparam_enum_names,
                             help="SBProbType parameter in PaToH")
    parser_temp.add_argument("-ncstr",
                             "--new_cut_set_threshold_reduction",
                             action="store",
                             default=1,
                             type=float,
                             metavar="[0.00-1.00]",
                             help="if the limits for hypergraph partitioning caching (number of clauses/variables) are satisfied, then the new_cut_set_threshold will be multiplied by x")

    parser_temp.add_argument("-v",
                             "--version",
                             action="version",
                             version=VERSION
                             )

    return parser_temp


if __name__ == "__main__":
    # Parser
    parser = create_parser()
    args = parser.parse_args()

    # Warning
    warnings.simplefilter('ignore', category=ResourceWarning)

    main(args)
