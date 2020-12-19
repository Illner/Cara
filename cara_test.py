# Import
import cara
import argparse

# Import
import tests.formula.formula_test as f_test

# Import exception
import exception.test_exception as t_exception


def main(args):
    result = "Test automation results"

    # Formula test
    if args.formula_test:
        formula_test = f_test.FormulaTest()
        try:
            (result_bool, result_str) = formula_test.test()
            result = "\n".join((result, "", formula_test.test_name, str(result_bool), result_str))
        except t_exception.TestException as err:
            result = "\n".join((result, "", formula_test.test_name, str(err)))

    # Print the result
    if args.output_file is None:
        print(result)
    # Save the result to the output file
    else:
        with open(args.output_file, "w") as file_output:
            file_output.write(result)


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

    return parser


if __name__ == "__main__":
    # Parser
    parser = create_parser()
    args = parser.parse_args()

    main(args)
