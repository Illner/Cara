# n = CircuitTest()
# n.save()

# n = DynamicGraphTest()
# n.save()

# # path = r"C:\Users\illner\Desktop\temp.txt"
# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\formula\CNF_formulae\large_cnf_valid.cnf"
# # path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\SAT benchmarks\SATLIB - Benchmark Problems\All Intervall Series\ais\ais12.cnf"
#
# cnf = Cnf(path)
# print(cnf.number_of_variables)
# print(cnf.real_number_of_clauses)
# s = 0
#
# cl = list(range(cnf.real_number_of_clauses))
# c = random.sample(cl, 300)
# va = list(cnf.get_variable_in_clauses(set(c)))
#
# print(len(va))
# p = int(len(va) / 100 * 50)
# print(p)
# print("-")
#
#
# for j in range(500):
#
#     v = random.sample(va, p)
#     v = list(set(v))
#
#     c2 = []
#     for n in c:
#         if not (cnf.get_clause(n)).intersection(set(v)):
#             c2.append(n)
#
#     if not c2:
#         print("Shit")
#         continue
#     print("----: " + str(len(c2)))
#     start = time.time()
#     cnf.hypergraph.get_cut_set(c2, v)
#     print(f"{j}")
#     end = time.time()
#     s += (end - start)
# print(s / 500)

# import formula.cnf as cnf
# import compiler.solver
# import compiler.enum.sat_solver_enum as ss_emum
#
# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\formula\cnf\CNF_formulae\large_cnf_valid.cnf"
#
# cnf = cnf.Cnf(path)
# solver = compiler.solver.Solver(cnf, None, ss_emum.SatSolverEnum.CaDiCal)
#
# n = solver.unit_propagation([])
# print(n)
#
# iup = solver.implicit_unit_propagation([])
# print(iup)

# print()
# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\formula\CNF_formulae\no_comments_valid.cnf"
# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\SAT benchmarks\D4\Handmade\LatinSquare\qg2-08.cnf"
#
# start = time.time()
# cnf = Cnf(path)
# n = cnf.get_incidence_graph()
# print(n.number_of_nodes())
# n.remove_literal(-1)
# end = time.time()
# print(end - start)
# start = time.time()
# x = n.create_incidence_graphs_for_components()
# print(n.number_of_nodes())
# end = time.time()
# print(end - start)

# from tests.compiler.solver.solver_test import SolverTest
#
# s = SolverTest()
# s.save()
