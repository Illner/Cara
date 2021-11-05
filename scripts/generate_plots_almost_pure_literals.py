import os
from formula.cnf import Cnf
from compiler.solver import Solver
from visualization.plot import histogram
from compiler.enum.sat_solver_enum import SatSolverEnum
from compiler.enum.implied_literals_enum import ImpliedLiteralsEnum
from compiler.preselection_heuristic.none_heuristic import NoneHeuristic
from compiler.decision_heuristic.jeroslow_wang_heuristic import JeroslowWangHeuristic
from compiler.decision_heuristic.clause_reduction_heuristic import ClauseReductionHeuristic
from compiler.enum.heuristic.mixed_difference_heuristic_enum import MixedDifferenceHeuristicEnum


path_directory = r"D:\Storage\OneDrive\Public\Savický\RenamableHornFormulae\RH-DLCS-DLIS (-t, c, p)\planning"
plot_path = r"C:\Users\illner\Desktop\temp"

ratio = []
length = []
pure_ratio = []
horn_clause_ratio = []
almost_pure_ratio = []
file_list = [(file, file_path) for file in os.listdir(path_directory) if (os.path.isfile(file_path := os.path.join(path_directory, file)))]

suffix = "planning"

for i, (file_name, file_path) in enumerate(file_list):
    # if not file_name.startswith("C203_FW"):
    #     continue

    literal = {}
    variable = {}
    variable_set = set()
    number_of_clauses = 0
    number_of_horn_clauses = 0

    pure_literal = set()
    almost_pure_literal = set()

    with open(file_path, "r") as file:
        for line in file.readlines():
            temp = line.split(" ")

            if line.startswith("p"):
                continue

            number_of_clauses += 1
            positive_literals = 0

            for j in temp:
                l = int(j)

                if l == 0:
                    continue

                if l > 0:
                    positive_literals += 1

                v = abs(l)

                if v not in variable:
                    variable[v] = 0
                    literal[l] = 0
                    literal[-l] = 0

                    variable_set.add(v)

                literal[l] += 1
                variable[v] += 1

            if positive_literals <= 1:
                number_of_horn_clauses += 1

    length.append(number_of_clauses)
    ratio.append(number_of_clauses / len(variable_set))
    horn_clause_ratio.append(number_of_horn_clauses / number_of_clauses)

    for v in variable_set:
        if literal[v] == 0:
            pure_literal.add(v)
            continue
        elif literal[-v] == 0:
            pure_literal.add(v)
            continue

        if literal[v] == 1:
            almost_pure_literal.add(v)
        elif literal[-v] == 1:
            almost_pure_literal.add(v)

    temp_2 = len(pure_literal) / len(variable_set)
    pure_ratio.append(temp_2)

    temp_2 = (len(almost_pure_literal) + len(pure_literal)) / len(variable_set)
    almost_pure_ratio.append(temp_2)

    print(f"{i}/{len(file_list)}")

histogram(pure_ratio, [""], "# pure literals / # variables", bins=100,
          x_label="# pure literals / # variables",
          y_label="Number of formulae",
          save_path=f"{plot_path}/pure_literals_{suffix}.png")
histogram(almost_pure_ratio, [""], "(# pure literals + # almost pure literals) / # variables", bins=100,
          x_label="(# pure literals + # almost pure literals) / # variables",
          y_label="Number of formulae",
          save_path=f"{plot_path}/almost_pure_literals_{suffix}.png")
histogram(length, [""], "Number of clauses", bins=100,
          x_label="Number of clauses",
          y_label="Number of formulae",
          save_path=f"{plot_path}/number_of_clauses_{suffix}.png")
histogram(ratio, [""], "Ratio (# clauses / # variables)", bins=100,
          x_label="Ratio (# clauses / # variables)",
          y_label="Number of formulae",
          save_path=f"{plot_path}/ratio_{suffix}.png")
histogram(horn_clause_ratio, [""], "# horn clauses / # clauses", bins=100,
          x_label="# horn clauses / # clauses",
          y_label="Number of formulae",
          save_path=f"{plot_path}/horn_clauses_ratio_{suffix}.png")

# temp = sorted(variable, key=variable.get, reverse=True)
#
# for x in range(0, 0):
#     l = temp[x]
#     print(f"{l}: {variable[l]}")
#     print(f"{l}: {literal[l]}")
#     print(f"{-l}: {literal[-l]}")
#     print()
#
# cnf = Cnf(path)
# ig = cnf.get_incidence_graph(copy=False)
# jw = JeroslowWangHeuristic(NoneHeuristic(), False, False)
# # jw = ClauseReductionHeuristic(NoneHeuristic(), True, MixedDifferenceHeuristicEnum.OK_SOLVER)
#
# s = Solver(cnf, SatSolverEnum.MiniSAT, ImpliedLiteralsEnum.BCP)
#
# print(f"Number of clauses: {ig.number_of_clauses()}")
#
# decision_variable = jw.get_decision_variable(cut_set=ig.variable_set(copy=False),
#                                              incidence_graph=ig,
#                                              solver=s,
#                                              assignment_list=[],
#                                              depth=0)
#
# print(f"decision_variable: {decision_variable}")
# print(f"{decision_variable}: {ig.literal_number_of_occurrences(decision_variable)}")
# print(f"{-decision_variable}: {ig.literal_number_of_occurrences(-decision_variable)}")
# implied_literals = s.unit_propagation([decision_variable])
# implied_literals.add(decision_variable)
# ig.remove_literal_list(list(implied_literals), None)
# print(f"Decision variable - number of clauses: {ig.number_of_clauses()}")
#
# ig.restore_backup_literal_set(implied_literals)
#
# s = Solver(cnf, SatSolverEnum.MiniSAT, ImpliedLiteralsEnum.BCP)
# implied_literals = s.unit_propagation([-decision_variable])
# implied_literals.add(-decision_variable)
# ig.remove_literal_list(list(implied_literals), None)
# print(f"- Decision variable - number of clauses: {ig.number_of_clauses()}")
#
# ig.restore_backup_literal_set(implied_literals)
