# Import
import os
import cara
import argparse
import warnings
from typing import Tuple
from tests.test_abstract import TestAbstract

# Formula
import tests.formula.cnf.cnf_test as fc_test
import tests.formula.incidence_graph.incidence_graph_test as fig_test

# Circuit
import tests.circuit.node.node_test as cn_test
import tests.circuit.circuit.circuit_test as cc_test

# Compiler
import tests.compiler.solver.solver_test as cs_test
import tests.compiler.compiler.compiler_test as c_test
import tests.compiler.backbones.backbones_test as cb_test
# import tests.compiler.dynamic_graph.dynamic_graph_test as cdg_test
import tests.compiler.hypergraph_partitioning.hypergraph_partitioning_test as chp_test

# Import exception
import exception.test.test_exception as t_exception

# Static variable - Path
LOG_PATH = os.path.join(os.getcwd(), "log")


def main(args):
    log_string = "Test automation results\n"
    print(log_string)

    # Cnf test
    if args.formula_cnf_test:
        cnf_test = fc_test.CnfTest()
        print(cnf_test.test_name, end=": ")
        result, log_result = test(cnf_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Incidence graph test
    if args.formula_incidence_graph_test:
        incidence_graph_test = fig_test.IncidenceGraphTest()
        print(incidence_graph_test.test_name, end=": ")
        result, log_result = test(incidence_graph_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Node test
    if args.circuit_node_test:
        node_test = cn_test.NodeTest()
        print(node_test.test_name, end=": ")
        result, log_result = test(node_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Circuit test
    if args.circuit_test:
        circuit_test = cc_test.CircuitTest()
        print(circuit_test.test_name, end=": ")
        result, log_result = test(circuit_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Solver test
    if args.compiler_solver_test:
        solver_test = cs_test.SolverTest()
        print(solver_test.test_name, end=": ")
        result, log_result = test(solver_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Hypergraph partitioning test
    if args.compiler_hypergraph_partitioning_test:
        hypergraph_partitioning_test = chp_test.HypergraphPartitioningTest()
        print(hypergraph_partitioning_test.test_name, end=": ")
        result, log_result = test(hypergraph_partitioning_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Backbones test
    if args.compiler_backbones_test:
        backbones_test = cb_test.BackbonesTest()
        print(backbones_test.test_name, end=": ")
        result, log_result = test(backbones_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Compiler test
    if args.compiler_test:
        compiler_test = c_test.CompilerTest()
        print(compiler_test.test_name, end=": ")
        result, log_result = test(compiler_test)
        # print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Save the log
    with open(LOG_PATH, "w") as log_file:
        log_file.write(log_string)


def test(test_instantiation: TestAbstract) -> Tuple[bool, str]:
    """
    Run a test on the test's instantiation (test_instantiation)
    :param test_instantiation: the test's instantiation
    :return: the result of the test
    """

    result_bool = False

    try:
        (result_bool, result_tuple) = test_instantiation.test()
        if result_bool:  # Test passed
            result = f"{test_instantiation.test_name}: {str(result_bool)}"
        else:  # Test failed
            result = "\n".join((test_instantiation.test_name, str(result_bool), result_tuple[1]))
    except t_exception.TestException as err:
        result = "\n".join((test_instantiation.test_name, str(err)))

    return result_bool, result


def create_parser() -> argparse.ArgumentParser:
    # Create the parser
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(prog="Cara - test automation",
                                     description="Test automation for Cara compiler",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter     # Default values are shown in help
                                     )

    # Add the arguments
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
                        "--circuit_test",
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
    parser.add_argument("-cst",
                        "--compiler_solver_test",
                        action="store",
                        default=True,
                        type=cara.str2bool,
                        help="Test automation for solvers.")
    parser.add_argument("-chpt",
                        "--compiler_hypergraph_partitioning_test",
                        action="store",
                        default=True,
                        type=cara.str2bool,
                        help="Test automation for hypergraph partitioning.")
    parser.add_argument("-cbt",
                        "--compiler_backbones_test",
                        action="store",
                        default=True,
                        type=cara.str2bool,
                        help="Test automation for backbones.")
    parser.add_argument("-ct",
                        "--compiler_test",
                        action="store",
                        default=False,
                        type=cara.str2bool,
                        help="Test automation for compilers.")

    return parser


if __name__ == "__main__":
    # Parser
    parser = create_parser()
    args = parser.parse_args()

    # Warning
    warnings.simplefilter('ignore')

    main(args)
