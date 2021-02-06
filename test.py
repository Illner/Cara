from circuit.node.leaf.constant_leaf import ConstantLeaf
from circuit.node.leaf.literal_leaf import LiteralLeaf
from circuit.node.inner_node.and_inner_node import AndInnerNode
from circuit.node.inner_node.or_inner_node import OrInnerNode

from other.sorted_list import SortedList
from tests.circuit import circuit_test
from tests.circuit.node_test import NodeTest
from tests.formula.formula_test import FormulaTest
from tests.circuit.circuit_test import CircuitTest

# n = CircuitTest()
# n.save()

from circuit.circuit import Circuit


path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Diplomová práce\Program\Cara\tests\circuit\NNF_formulae\sat-grid-pbl-0010.nnf"

c = Circuit(path)
# print(repr(c))

# print(c.topological_ordering())
c.smooth()
# print(repr(c))
# print(c.topological_ordering())

print(c.is_smooth())
