from circuit.node.leaf.constant_leaf import ConstantLeaf
from circuit.node.leaf.literal_leaf import LiteralLeaf
from circuit.node.inner_node.and_inner_node import AndInnerNode
from circuit.node.inner_node.or_inner_node import OrInnerNode

# TODO NNF parser (save / load)
# TODO static index of nodes
# TODO decision node
# TODO circuit test - files (read, circuit)

from other.sorted_list import SortedList
from tests.circuit.node_test import NodeTest
from tests.formula.formula_test import FormulaTest

n = NodeTest()
n.save()
