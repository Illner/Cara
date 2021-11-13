from formula.cnf import Cnf
import formula.enum.lp_formulation_objective_function_enum as objective_function
from formula.renamable_horn_formula_lp_formulation import RenamableHornFormulaLpFormulation
from compiler_statistics.formula.renamable_horn_formula_lp_formulation_statistics import RenamableHornFormulaLpFormulationStatistics

path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\CaraCompiler\tests\formula\horn_cnf\CNF_formulae\renamable_horn.cnf"

cnf = Cnf(path)
incidence_graph = cnf.get_incidence_graph(copy=False)

stat = RenamableHornFormulaLpFormulationStatistics(active=True)
lp_formulation = RenamableHornFormulaLpFormulation(incidence_graph, objective_function=objective_function.LpFormulationObjectiveFunctionEnum.SQUARED_INVERSE_LENGTH_WEIGHTED_HORN_FORMULA, is_exact=True, statistics=stat)

print(str(lp_formulation))

result = lp_formulation.solve()

print(result)

print(stat)
