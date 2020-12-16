# Import
import argparse

# Import enum
import circuit.circuit_type_enum as ct_enum
import compiler.implied_literals_enum as il_enum
import external.sat_solver.sat_solver_enum as ss_enum
import compiler.component_caching.component_caching_enum as cc_enum

# Constant
VERSION = "0.0.1"


def main(args):
    pass  # TODO main


def input_file_path(path: str) -> str:
    pass  # TODO input_file_path


def output_file_path(path: str) -> str:
    pass  # TODO output_file_path


def create_parser() -> argparse.ArgumentParser:
    # Create the parser
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(prog="Cara",
                                     description="Backdoor Decomposable Monotone Circuits (BDMC) compiler",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                     )

    # Add the arguments
    parser.add_argument("input_file",
                        action="store",
                        type=input_file_path,
                        help="The path of the input file which is in the DIMACS CNF format.")
    parser.add_argument("output_file",
                        action="store",
                        type=output_file_path,
                        help="The path of the output file where the circuit will be saved.")
    parser.add_argument("-ct",
                        "--circuit_type",
                        action="store",
                        default=ct_enum.circuit_type_enum_names[0],
                        type=str,
                        choices=ct_enum.circuit_type_enum_names,
                        help="The circuit type into which the input formula will be compiled.")
    parser.add_argument("-ss",
                        "--sat_solver",
                        action="store",
                        default=ss_enum.sat_solver_enum_names[0],
                        type=str,
                        choices=ss_enum.sat_solver_enum_names,
                        help="The SAT solver which will be used for compiling the circuit.")
    parser.add_argument("-cc",
                        "--component_caching",
                        action="store",
                        default=cc_enum.component_caching_enum_names[0],
                        type=str,
                        choices=cc_enum.component_caching_enum_names,
                        help="Which component caching will be used for compiling the circuit.")
    parser.add_argument("-il",
                        "--implied_literals",
                        action="store",
                        default=il_enum.implied_literals_enum_names[0],
                        type=str,
                        choices=il_enum.implied_literals_enum_names,
                        help="Which method will be used for deriving implied literals at every decision node.")

    decomposition_approach_group = parser.add_mutually_exclusive_group()
    decomposition_approach_group.add_argument("-dd",
                                              "--dynamic_decomposition",
                                              action="store_true",
                                              default=True,
                                              help="A dynamic decomposition approach will be used for compiling.")
    decomposition_approach_group.add_argument("-sd",
                                              "--static_decomposition",
                                              action="store_true",
                                              default=False,
                                              help="A static decomposition approach will be used for compiling.")

    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=VERSION
                        )

    return parser


if __name__ == "__main__":
    # Parser
    parser = create_parser()
    args = parser.parse_args()

    main(args)
