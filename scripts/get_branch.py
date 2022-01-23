import sys
import random
from circuit.circuit import Circuit
import circuit.node.node_type_enum as nt_enum
from circuit.node.node_abstract import NodeAbstract
from circuit.node.inner_node.inner_node_abstract import InnerNodeAbstract

path = sys.argv[1]

circuit = Circuit(path)
node_id = circuit.root_id
decision_node_list = []


def is_leaf(node_func: NodeAbstract):
    if (node_func.node_type == nt_enum.NodeTypeEnum.LITERAL) or \
       (node_func.node_type == nt_enum.NodeTypeEnum.TWO_CNF) or \
       (node_func.node_type == nt_enum.NodeTypeEnum.RENAMABLE_HORN_CNF) or \
       (node_func.node_type == nt_enum.NodeTypeEnum.CONSTANT):
        return True

    return False


def get_random_child_id(node_func: InnerNodeAbstract) -> int:
    child_set = node_func._child_id_set
    temp_set = set()

    for child_id in child_set:
        child = circuit.get_node(child_id)
        if not is_leaf(child):
            temp_set.add(child_id)

    if not temp_set:
        temp_set.add(list(child_set)[0])

    child_id = random.sample(temp_set, 1)[0]

    return child_id


while True:
    while True:
        node = circuit.get_node(node_id)

        # The node does not exist
        if node is None:
            break

        # Leaf
        if is_leaf(node):
            break

        # OR node
        if node.node_type == nt_enum.NodeTypeEnum.OR_NODE:
            decision_node_list.append(node_id)
            node_id = get_random_child_id(node)
            continue

        # AND node
        if node.node_type == nt_enum.NodeTypeEnum.AND_NODE:
            node_id = get_random_child_id(node)
            continue

        # Mapping node
        if node.node_type == nt_enum.NodeTypeEnum.MAPPING_NODE:
            node_id = list(node._child_id_set)[0]
            continue

    if len(decision_node_list) > 2:
        break
    else:
        decision_node_list = []
        node_id = circuit.root_id


print(decision_node_list)
