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
# path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\formula\CNF_formulae\large_cnf_valid.cnf"
path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\SAT benchmarks\SATLIB - Benchmark Problems\All Intervall Series\ais\ais12.cnf"

cnf = Cnf(path)
print(cnf.number_of_variables)
print(cnf.real_number_of_clauses)
s = 0

for _ in range(100):
    start = time.time()
    c = cnf.hypergraph.get_cut_set(set(list(range(cnf.real_number_of_clauses))), [])
    print(len(c))
    end = time.time()
    s += (end - start)
print(s / 100)
