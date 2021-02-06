# Import
import os.path
import argparse
import warnings

# Import exception
import exception.cara_exception as c_exception

# Import enum
import compiler.base_class_enum as bc_enum
import circuit.circuit_type_enum as ct_enum
import compiler.implied_literals_enum as il_enum
import external.sat_solver.sat_solver_enum as ss_enum
import compiler.component_caching.component_caching_enum as cc_enum

# Constant
VERSION = "0.0.1"


def main(args):
    pass


def check_input_file_path(path: str) -> str:
    """
    Check if the input file exists. In case the file does not exist returns an exception (argparse.ArgumentTypeError).
    Parser
    :param path: the path of the input file
    :return: the path
    """

    if os.path.isfile(path):
        return path

    raise argparse.ArgumentTypeError(f"The input file ({path}) doesn't exist!")


def check_output_file_path(path: str) -> str:
    """
    Try to create an empty output file. In case the file creation fails, or the file already exists returns an exception (argparse.ArgumentTypeError).
    Parser
    :param path: the path of the output file
    :return: the path
    """

    # The output file already exists
    if os.path.isfile(path):
        raise argparse.ArgumentTypeError(
            f"The output file ({path}) already exists, please delete it or choose another name of the file!")

    try:
        with open(path, "w") as _:
            pass
    except PermissionError as err:
        raise argparse.ArgumentTypeError(f"An error occurred while trying to create the output file. {str(err)}")

    # Check if the output file has been created
    if os.path.isfile(path):
        return path

    raise argparse.ArgumentTypeError(f"An error occurred while trying to create the output file ({path}).")


def str2bool(v) -> bool:
    """
    Convert string to boolean. If the string cannot be converted to boolean returns an exception (ArgumentTypeError).
    Parser
    :param v: the string which will be converted to boolean
    :return: boolean
    """

    if isinstance(v, bool):
        return v

    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def create_parser() -> argparse.ArgumentParser:
    # Create the parser
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(prog="Cara",
                                     description="Backdoor Decomposable Monotone Circuits (BDMC) compiler",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                     # Default values are shown in help
                                     )

    # Add the arguments
    parser.add_argument("input_file",
                        action="store",
                        type=check_input_file_path,
                        help="The path of the input file which is in the DIMACS CNF format.")
    parser.add_argument("output_file",
                        action="store",
                        type=check_output_file_path,
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
    parser.add_argument("-bc",
                        "--base_class",
                        action="store",
                        default=bc_enum.base_class_enum_names[0],
                        type=str,
                        choices=bc_enum.base_class_enum_names,
                        help="Which base class will appear in the leaves of the circuit.")

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

    # Warning
    warnings.simplefilter('ignore', category=ResourceWarning)

    main(args)
