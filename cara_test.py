# Import
import cara
import argparse
import warnings
from tests.test_abstract import TestAbstract

import tests.formula.cnf.cnf_test as fc_test
import tests.formula.incidence_graph.incidence_graph_test as fig_test

import tests.circuit.node.node_test as cn_test
import tests.circuit.circuit.circuit_test as cc_test

# Import exception
import exception.test.test_exception as t_exception


def main(args):
    result = "Test automation results"

    # Cnf test
    if args.formula_cnf_test:
        cnf_test = fc_test.CnfTest()
        result = "\n".join((result, "", test(cnf_test)))

    # Incidence graph test
    if args.formula_incidence_graph_test:
        incidence_graph_test = fig_test.IncidenceGraphTest()
        result = "\n".join((result, "", test(incidence_graph_test)))

    # Node test
    if args.circuit_node_test:
        node_test = cn_test.NodeTest()
        result = "\n".join((result, "", test(node_test)))

    # Circuit test
    if args.circuit_circuit_test:
        circuit_test = cc_test.CircuitTest()
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
    parser.add_argument("-fct",
                        "--formula_cnf_test",
                        action="store",
                        default=True,
                        type=cara.str2bool,
                        help="Test automation for CNFs.")
    parser.add_argument("-figt",
                        "--formula_incidence_graph_test",
                        action="store",
                        default=True,
                        type=cara.str2bool,
                        help="Test automation for incidence graphs.")
    parser.add_argument("-cct",
                        "--circuit_circuit_test",
                        action="store",
                        default=True,
                        type=cara.str2bool,
                        help="Test automation for circuits.")
    parser.add_argument("-cnt",
                        "--circuit_node_test",
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
