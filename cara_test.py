# Import
import cara
import argparse
import warnings
from typing import Tuple
import other.environment as env
from tests.test_abstract import TestAbstract

# Formula
import tests.formula.cnf.cnf_test as fc_test
import tests.formula.two_cnf.two_cnf_test as ftc_test
import tests.formula.horn_cnf.horn_cnf_test as fhc_test
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

# Import enum
import compiler.enum.hypergraph_partitioning.hypergraph_partitioning_software_enum as hps_enum


def main(main_args):
    cara.print_logo()

    log_string = "Test automation results\n"
    print(log_string)

    # CNF test
    if main_args.formula_cnf_test:
        cnf_test = fc_test.CnfTest()
        print(cnf_test.test_name, end=": ", flush=True)
        result, log_result = test(cnf_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # 2-CNF test
    if main_args.formula_2_cnf_test:
        two_cnf_test = ftc_test.TwoCnfTest()
        print(two_cnf_test.test_name, end=": ", flush=True)
        result, log_result = test(two_cnf_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Horn CNF test
    if main_args.formula_horn_cnf_test:
        horn_cnf_test = fhc_test.HornCnfTest()
        print(horn_cnf_test.test_name, end=": ", flush=True)
        result, log_result = test(horn_cnf_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Incidence graph test
    if main_args.formula_incidence_graph_test:
        incidence_graph_test = fig_test.IncidenceGraphTest()
        print(incidence_graph_test.test_name, end=": ", flush=True)
        result, log_result = test(incidence_graph_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Node test
    if main_args.circuit_node_test:
        node_test = cn_test.NodeTest()
        print(node_test.test_name, end=": ", flush=True)
        result, log_result = test(node_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Circuit test
    if main_args.circuit_test:
        circuit_test = cc_test.CircuitTest()
        print(circuit_test.test_name, end=": ", flush=True)
        result, log_result = test(circuit_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Solver test
    if main_args.compiler_solver_test:
        solver_test = cs_test.SolverTest()
        print(solver_test.test_name, end=": ", flush=True)
        result, log_result = test(solver_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Hypergraph partitioning test
    if main_args.compiler_hypergraph_partitioning_test:
        for software_enum in hps_enum.hps_enum_values:
            # None
            if software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.NONE:
                continue

            # Windows
            if env.is_windows() and \
               (software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.PATOH or software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.KAHYPAR):
                continue

            # MacOS
            if env.is_mac_os() and software_enum == hps_enum.HypergraphPartitioningSoftwareEnum.HMETIS:
                continue

            hypergraph_partitioning_test = chp_test.HypergraphPartitioningTest(software_enum)
            print(hypergraph_partitioning_test.test_name, end=": ", flush=True)
            result, log_result = test(hypergraph_partitioning_test)
            print(result)
            log_string = "\n".join((log_string, log_result, ""))

    # Backbones test
    if main_args.compiler_backbones_test:
        backbones_test = cb_test.BackbonesTest()
        print(backbones_test.test_name, end=": ", flush=True)
        result, log_result = test(backbones_test)
        print(result)
        log_string = "\n".join((log_string, log_result, ""))

    # Compiler test
    if main_args.compiler_test:
        compiler_test = c_test.CompilerTest(main_args.compiler_test_limit)
        print(compiler_test.test_name, end=": ", flush=True)
        _, _ = test(compiler_test)
        # print(result)
        # log_string = "\n".join((log_string, log_result, ""))

    # Save the log
    with open(cara.LOG_PATH, "w", encoding="utf-8") as log_file:
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
    parser_temp = argparse.ArgumentParser(prog="cara_test.py",
                                          description="CaraCompiler - test automation",
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter    # Default values are shown in help
                                          )

    # Add the arguments
    parser_temp.add_argument("-fct",
                             "--formula_cnf_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for CNFs")
    parser_temp.add_argument("-f2ct",
                             "--formula_2_cnf_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for 2-CNFs")
    parser_temp.add_argument("-fhct",
                             "--formula_horn_cnf_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for Horn CNFs")
    parser_temp.add_argument("-figt",
                             "--formula_incidence_graph_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for incidence graphs")
    parser_temp.add_argument("-cct",
                             "--circuit_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for circuits")
    parser_temp.add_argument("-cnt",
                             "--circuit_node_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for nodes")
    parser_temp.add_argument("-cst",
                             "--compiler_solver_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for solvers")
    parser_temp.add_argument("-chpt",
                             "--compiler_hypergraph_partitioning_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for hypergraph partitioning")
    parser_temp.add_argument("-cbt",
                             "--compiler_backbones_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for backbones")
    parser_temp.add_argument("-ct",
                             "--compiler_test",
                             action="store",
                             default=True,
                             type=cara.str_to_bool_parser,
                             help="test automation for compilers")
    parser_temp.add_argument("-ct_l",
                             "--compiler_test_limit",
                             action="store",
                             default=10,     # 3840
                             type=cara.non_negative_int_parser,
                             metavar="[non-negative number]",
                             help="maximum tests per file")

    return parser_temp


if __name__ == "__main__":
    # Parser
    parser = create_parser()
    args = parser.parse_args()

    # Warning
    warnings.simplefilter('ignore')

    main(args)
