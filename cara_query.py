# Import
import cara
import argparse
import warnings
from circuit.circuit import Circuit
from other.sorted_list import SortedList

# Import exception
import exception.cara_exception as c_exception


def main(main_args):
    try:
        cara.print_logo()

        result = ""
        circuit = Circuit(main_args.circuit_file)
        print("The circuit has been processed!\n")

        assumption_set = set(main_args.a__assumption)
        assumption_str = SortedList(assumption_set).str_delimiter(', ')
        assumption_str = f"Assumption set: {assumption_str}"

        clause = set(main_args.cl__clause)
        clause_str = SortedList(clause).str_delimiter(' v ')
        clause_str = f"Clause: {clause_str}"

        observation_set = set(main_args.o__observation)
        observation_str = SortedList(observation_set).str_delimiter(", ")
        observation_str = f"Observation set: {observation_str}"

        default_set = set(main_args.d__default)
        default_str = SortedList(default_set).str_delimiter(", ")
        default_str = f"Default set: {default_str}"

        # Consistency
        if main_args.consistency:
            print("Consistency check (CO)")
            print(assumption_str)

            result = circuit.is_satisfiable(assumption_set=assumption_set, exist_quantification_set=set(), use_cache=False)
            result = "SATISFIABLE" if result else "UNSATISFIABLE"

        # Validity
        if main_args.validity:
            print("Validity check (VA)")
            print(assumption_str)

            result = circuit.is_valid(assumption_set=assumption_set, use_cache=False)
            result = "TAUTOLOGY" if result else "NOT TAUTOLOGY"

        # Clausal entailment
        if main_args.clausal_entailment:
            print("Clausal entailment check (CE)")
            print(clause_str)

            result = circuit.clause_entailment(clause=clause, exist_quantification_set=set(), use_cache=False)
            result = "ENTAILED" if result else "NOT ENTAILED"

        # Model counting
        if main_args.model_counting:
            print("Model counting (CT)")
            print(assumption_str)

            result = circuit.model_counting(assumption_set=assumption_set, use_cache=False)
            result = str(result)

        # Minimum cardinality
        if main_args.minimum_cardinality:
            print("Minimum cardinality (MC)")
            print(observation_str)
            print(default_str)

            result = circuit.minimum_default_cardinality(observation_set=observation_set, default_set=default_set, use_cache=False)
            result = str(result)

        print()
        print(f"---{'-'*len(result)}---")
        print(f"-- {result} --")
        print(f"---{'-'*len(result)}---")
    except (c_exception.CaraException, Exception) as err:
        print(f"An error has occurred!\n{str(err)}")


def create_parser() -> argparse.ArgumentParser:
    # Create the parser
    parser_temp = argparse.ArgumentParser(prog="cara_query.py",
                                          description="CaraCompiler - query",
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter     # default values are shown in the help
                                          )

    # Add arguments
    parser_temp.add_argument("circuit_file",
                             action="store",
                             type=cara.input_file_path_parser,
                             help="path of the circuit file, which is in the DIMACS NNF format")

    parser_query_group = parser_temp.add_mutually_exclusive_group(required=True)
    parser_query_group.add_argument("-co",
                                    "--consistency",
                                    action="store_true",
                                    default=False,
                                    help="consistency check (CO)")
    parser_query_group.add_argument("-va",
                                    "--validity",
                                    action="store_true",
                                    default=False,
                                    help="validity check (VA)")
    parser_query_group.add_argument("-ce",
                                    "--clausal_entailment",
                                    action="store_true",
                                    default=False,
                                    help="clausal entailment check (CE)")
    parser_query_group.add_argument("-ct",
                                    "--model_counting",
                                    action="store_true",
                                    default=False,
                                    help="model counting (CT)")
    parser_query_group.add_argument("-mc",
                                    "--minimum_cardinality",
                                    action="store_true",
                                    default=False,
                                    help="minimum cardinality (MC)")

    parser_temp.add_argument("-a"
                             "--assumption",
                             action='store',
                             default=[],
                             nargs="+",
                             type=int,
                             metavar="literal",
                             help='assumption set (CO, VA, CT)')
    parser_temp.add_argument("-cl"
                             "--clause",
                             action='store',
                             default=[],
                             nargs="+",
                             type=int,
                             metavar="literal",
                             help='clause (CE)')
    parser_temp.add_argument("-o"
                             "--observation",
                             action='store',
                             default=[],
                             nargs="+",
                             type=int,
                             metavar="literal",
                             help='observation set (MC)')
    parser_temp.add_argument("-d"
                             "--default",
                             action='store',
                             default=[],
                             nargs="+",
                             type=int,
                             metavar="variable",
                             help='default set (MC)')

    return parser_temp


if __name__ == "__main__":
    # Parser
    parser = create_parser()
    args = parser.parse_args()

    # Warning
    warnings.simplefilter('ignore', category=ResourceWarning)

    main(args)
