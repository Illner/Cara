# Import
from circuit.node.leaf.leaf_abstract import LeafAbstract

# Import enum
import circuit.node.node_type_enum as nt_enum


class LiteralLeaf(LeafAbstract):
    """
    Circuit literal leaf representation
    """

    """
    Private int literal
    Private int variable
    Private bool is_positive
    """

    def __init__(self, literal: int, id: int = 0):
        self.__literal: int = literal
        self.__variable: int = abs(literal)
        self.__is_positive = True if self.__literal > 0 else False
        super().__init__(id, nt_enum.NodeTypeEnum.LITERAL, {self.__variable}, {self.__literal}, 0)

    # region Override method
    def is_satisfiable(self, assumption_set: set[int], exist_quantification_set: set[int], use_caches: bool = True) -> bool:
        # The assumption set
        if self.literal in assumption_set:
            return True
        if -self.literal in assumption_set:
            return False

        # The exist quantification set
        if self.variable in exist_quantification_set:
            return True

        return True

    def model_counting(self, assumption_set: set[int], exist_quantification_set: set[int], use_caches: bool = True) -> int:
        # The assumption set
        if self.literal in assumption_set:
            return 1
        if -self.literal in assumption_set:
            return 0

        # The exist quantification set
        if self.variable in exist_quantification_set:
            return 1

        return 1

    def minimum_default_cardinality(self, default_set: set[int], use_caches: bool = True) -> float:
        # The default set does not contain this variable
        if self.variable not in default_set:
            return 0

        if self.is_positive:
            return 0

        # Negative literal
        return 1

    def smooth(self, smooth_create_and_node_function) -> None:
        return
    # endregion

    # endregion Magic method
    def __repr__(self):
        string_temp = super().__repr__()

        string_temp = " ".join((string_temp, f"Literal: {self.literal}"))

        return string_temp
    # endregion

    # region Property
    @property
    def literal(self):
        return self.__literal

    @property
    def variable(self):
        return self.__variable

    @property
    def is_positive(self):
        return self.__is_positive
    # endregion
