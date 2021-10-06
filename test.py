from formula.cnf import Cnf

path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\CaraCompiler\cnf_formulae\sum.32.cnf"

cnf = Cnf(path)

print(cnf.get_incidence_graph().convert_to_cnf())
