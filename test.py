import ctypes

from circuit.node.leaf.constant_leaf import ConstantLeaf
from circuit.node.leaf.literal_leaf import LiteralLeaf
from circuit.node.inner_node.and_inner_node import AndInnerNode
from circuit.node.inner_node.or_inner_node import OrInnerNode

from circuit.circuit import Circuit

from other.sorted_list import SortedList
from tests.circuit import circuit_test
from tests.circuit.node_test import NodeTest
from tests.formula.formula_test import FormulaTest
from tests.circuit.circuit_test import CircuitTest

# n = CircuitTest()
# n.save()


from formula.cnf import Cnf
import time

# path = r"C:\Users\illner\Desktop\temp.txt"
path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\formula\CNF_formulae\large_cnf_valid.cnf"
# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\SAT benchmarks\SATLIB - Benchmark Problems\All Intervall Series\ais\ais12.cnf"

cnf = Cnf(path)

start = time.time()
c = cnf.hypergraph.get_cut_set(set(list(range(cnf.real_number_of_clauses))), [])
end = time.time()
print(end - start)

variables = cnf._get_variable_set()

occurrences = dict()
len_list = [[]]*(len(variables) + 1)

start = time.time()
for var in variables:
    temp = set()
    temp.update(cnf._get_clause_set(var))
    temp.update(cnf._get_clause_set(-var))
    occ = len(temp)
    if occ not in occurrences:
        occurrences[occ] = 1
    else:
        occurrences[occ] += 1

    for clause_id in temp:
        temp_a = len(cnf.get_clause(clause_id))
        len_list[var].append(temp_a)

# print(occurrences)

# print(mean)
end = time.time()
print(end - start)


print(2**30)