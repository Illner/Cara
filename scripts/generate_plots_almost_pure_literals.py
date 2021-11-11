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

# C168_FW, C203_FW, C203_FS, C638_FKB
# C220_FV, C220_FW, C140_FV, C208_FC, C129_FR, C208_FA

configuration_name = "C168_FW"

path_directory = r"C:\Users\illner\Desktop\Temp3"
plot_path = fr"C:\Users\illner\Desktop\{configuration_name}"

ratio = []
length = []
pure_ratio = []
horn_clause_ratio = []
almost_pure_ratio = []

min_occurrence = []
min_occurrence_number = 2
min_occurrence_clauses = []

max_variable_occurrence = []
max_variable_occurrence_two_cnf = []
min_variable_occurrence = []
min_variable_occurrence_two_cnf = []

two_cnf = []

file_list = [(file, file_path) for file in os.listdir(path_directory) if (os.path.isfile(file_path := os.path.join(path_directory, file)))]

suffix = configuration_name

for i, (file_name, file_path) in enumerate(file_list):
    if not file_name.startswith(configuration_name):
        continue

    literal = {}
    variable = {}
    variable_set = set()
    number_of_clauses = 0
    number_of_two_clauses = 0
    number_of_horn_clauses = 0

    min_occurrence_temp = []
    min_occurrence_clauses_temp = []

    literal_two_clauses = {}
    variable_two_clauses = {}

    pure_literal = set()
    almost_pure_literal = set()

    with open(file_path, "r") as file:
        for line in file.readlines():
            temp = line.split(" ")

            if line.startswith("p"):
                continue

            number_of_clauses += 1
            positive_literals = 0
            literal_temp = set()

            for j in temp:
                l = int(j)

                if l == 0:
                    continue

                literal_temp.add(l)

                if l > 0:
                    positive_literals += 1

                v = abs(l)

                if v not in variable:
                    variable[v] = 0
                    literal[l] = 0
                    literal[-l] = 0
                    literal_two_clauses[l] = 0
                    literal_two_clauses[-l] = 0
                    variable_two_clauses[v] = 0

                    variable_set.add(v)

                literal[l] += 1
                variable[v] += 1

            if positive_literals <= 1:
                number_of_horn_clauses += 1

            if len(literal_temp) == 2:
                number_of_two_clauses += 1
                for lit in literal_temp:
                    literal_two_clauses[lit] += 1
                    variable_two_clauses[abs(lit)] += 1

    two_cnf.append(number_of_two_clauses / number_of_clauses)

    length.append(number_of_clauses)
    ratio.append(number_of_clauses / len(variable_set))
    horn_clause_ratio.append(number_of_horn_clauses / number_of_clauses)

    variable_occurrences = {}
    min_variable_occurrences = {}

    for v in variable_set:
        positive_occurrence = literal[v]
        negative_occurrence = literal[-v]
        min_occ = min(positive_occurrence, negative_occurrence)
        min_occurrence_temp.append(min_occ)
        min_occurrence_clauses_temp.append(min_occ / number_of_clauses)

        variable_occurrences[v] = positive_occurrence + negative_occurrence
        min_variable_occurrences[v] = min(positive_occurrence, negative_occurrence)

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

    temptemp = sorted(min_occurrence_temp, reverse=True)[0:min_occurrence_number]
    for x in temptemp:
        min_occurrence.append(x)

    temptemp = sorted(min_occurrence_clauses_temp, reverse=True)[0:min_occurrence_number]
    for x in temptemp:
        min_occurrence_clauses.append(x)

    max_variable_occurrence_temp = [k for k, v in sorted(variable_occurrences.items(), key=lambda item: item[1], reverse = True)][0]
    min_variable_occurrence_temp = [k for k, v in sorted(min_variable_occurrences.items(), key=lambda item: item[1], reverse = True)][0]

    max_variable_occurrence.append(variable_occurrences[max_variable_occurrence_temp] / number_of_clauses)
    max_variable_occurrence_two_cnf.append(variable_two_clauses[max_variable_occurrence_temp] / variable_occurrences[max_variable_occurrence_temp])

    min_variable_occurrence.append(variable_occurrences[min_variable_occurrence_temp] / number_of_clauses)
    min_variable_occurrence_two_cnf.append(variable_two_clauses[min_variable_occurrence_temp] / variable_occurrences[min_variable_occurrence_temp])

    print(f"{i}/{len(file_list)} - {file_name}")

histogram(pure_ratio, [""], f"# pure literals / # variables \n {suffix}", bins=100,
          x_label="# pure literals / # variables",
          y_label="Number of formulae",
          save_path=f"{plot_path}/pure_literals_{suffix}.png")
histogram(almost_pure_ratio, [""], f"(# pure literals + # almost pure literals) / # variables \n {suffix}", bins=100,
          x_label="(# pure literals + # almost pure literals) / # variables",
          y_label="Number of formulae",
          save_path=f"{plot_path}/almost_pure_literals_{suffix}.png")
histogram(length, [""], f"Number of clauses \n {suffix}", bins=100,
          x_label="Number of clauses",
          y_label="Number of formulae",
          save_path=f"{plot_path}/number_of_clauses_{suffix}.png")
histogram(ratio, [""], f"Ratio (# clauses / # variables) \n {suffix}", bins=100,
          x_label="Ratio (# clauses / # variables)",
          y_label="Number of formulae",
          save_path=f"{plot_path}/ratio_{suffix}.png")
histogram(horn_clause_ratio, [""], f"# horn clauses / # clauses \n {suffix}", bins=100,
          x_label="# horn clauses / # clauses",
          y_label="Number of formulae",
          save_path=f"{plot_path}/horn_clauses_ratio_{suffix}.png")
histogram(min_occurrence, [""], f"min occurrence ({min_occurrence_number}) \n {suffix}", bins=100,
          x_label=f"min occurrence ({min_occurrence_number})",
          y_label="Number of formulae",
          save_path=f"{plot_path}/min_occurrence_{suffix}.png")
histogram(min_occurrence_clauses, [""], f"min occurrence ({min_occurrence_number}) / # clauses \n {suffix}", bins=100,
          x_label=f"min occurrence ({min_occurrence_number}) / # clauses",
          y_label="Number of formulae",
          save_path=f"{plot_path}/min_occurrence_clauses_{suffix}.png")

histogram(two_cnf, [""], f"# two clauses / # clauses \n {suffix}", bins=100,
          x_label=f"# two clauses / # clauses",
          y_label="Number of formulae",
          save_path=f"{plot_path}/two_clauses_{suffix}.png")

histogram(max_variable_occurrence, [""], f"(MAX) variable occurrence / # clauses \n {suffix}", bins=100,
          x_label=f"(MAX) variable occurrence / # clauses",
          y_label="Number of formulae",
          save_path=f"{plot_path}/max_variable_occurrence_clauses_{suffix}.png")
histogram(max_variable_occurrence_two_cnf, [""], f"(MAX) variable occurrence two cnf / variable occurrence \n {suffix}", bins=100,
          x_label=f"(MAX) variable occurrence two cnf / variable occurrence",
          y_label="Number of formulae",
          save_path=f"{plot_path}/max_variable_occurrence_two_cnf_{suffix}.png")
histogram(min_variable_occurrence, [""], f"(MIN) variable occurrence / # clauses \n {suffix}", bins=100,
          x_label=f"(MIN) variable occurrence / # clauses",
          y_label="Number of formulae",
          save_path=f"{plot_path}/min_variable_occurrence_clauses_{suffix}.png")
histogram(min_variable_occurrence_two_cnf, [""], f"(MIN) variable occurrence two cnf / variable occurrence \n {suffix}", bins=100,
          x_label=f"(MIN) variable occurrence two cnf / variable occurrence",
          y_label="Number of formulae",
          save_path=f"{plot_path}/min_variable_occurrence_two_cnf_{suffix}.png")

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
