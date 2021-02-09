# Import
import cara
import argparse
import warnings
import tests.circuit.node_test as n_test
import tests.formula.formula_test as f_test
import tests.circuit.circuit_test as c_test
from tests.test_abstract import TestAbstract

# Import exception
import exception.test_exception as t_exception


def main(args):
    result = "Test automation results"

    # Formula test
    if args.formula_test:
        formula_test = f_test.FormulaTest()
        result = "\n".join((result, "", test(formula_test)))

    # Node test
    if args.node_test:
        node_test = n_test.NodeTest()
        result = "\n".join((result, "", test(node_test)))

    # Circuit test
    if args.circuit_test:
        circuit_test = c_test.CircuitTest()
        result = "\n".join((result, "", test(circuit_test)))

    # Print the result
    if args.output_file is None:
        print(result)
    # Save the result to the output file
    else:
        with open(args.output_file, "w") as file_output:
            file_output.write(result)


def test(test_instantiation: TestAbstract) -> str:
    """
    Run a test on the test's instantiation (test_instantiation)
    :param test_instantiation: the test's instantiation
    :return: the result of the test
    """

    result = ""
    try:
        (result_bool, result_tuple) = test_instantiation.test()
        if result_bool:  # Test passed
            result = "\n".join((test_instantiation.test_name, str(result_bool)))
        else:   # Test failed
            result = "\n".join((test_instantiation.test_name, str(result_bool),
                                # "Original result", result_tuple[0],
                                "Actual result", result_tuple[1]))
    except t_exception.TestException as err:
        result = "\n".join((test_instantiation.test_name, str(err)))

    return result


def create_parser() -> argparse.ArgumentParser:
    # Create the parser
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(prog="Cara - test automation",
                                     description="Test automation for Cara compiler",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter     # Default values are shown in help
                                     )

    # Add the arguments
    parser.add_argument("-of",
                        "--output_file",
                        action="store",
                        type=cara.check_output_file_path,
                        help="The path of the output file where the result of the tests will be saved.")
    parser.add_argument("-ft",
                        "--formula_test",
                        action="store",
                        default=True,
                        type=cara.str2bool,
                        help="Test automation for formulae.")
    parser.add_argument("-ct",
                        "--circuit_test",
                        action="store",
                        default=True,
                        type=cara.str2bool,
                        help="Test automation for circuits.")
    parser.add_argument("-nt",
                        "--node_test",
                        action="store",
                        default=True,
                        type=cara.str2bool,
                        help="Test automation for nodes.")

    return parser


if __name__ == "__main__":
    # Parser
    parser = create_parser()
    args = parser.parse_args()

    # Warning
    warnings.simplefilter('ignore')

    main(args)
