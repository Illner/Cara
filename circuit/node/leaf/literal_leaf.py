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
    """

    def __init__(self, literal: int, id: int = 0):
        self.__literal: int = literal
        self.__variable: int = abs(literal)
        super().__init__(id, nt_enum.NodeTypeEnum.LITERAL, {self.__variable}, 0)

    # region Override method
    def is_satisfiable(self, assumption_set: set[int], exist_quantification_set: set[int], use_caches: bool = True) -> bool:
        # The assumption set
        if self.__literal in assumption_set:
            return True
        if -self.__literal in assumption_set:
            return False

        # The exist quantification set
        if self.__variable in exist_quantification_set:
            return True

        return True

    def model_counting(self, assumption_set: set[int], exist_quantification_set: set[int], use_caches: bool = True) -> int:
        # The assumption set
        if self.__literal in assumption_set:
            return 1
        if -self.__literal in assumption_set:
            return 0

        # The exist quantification set
        if self.__variable in exist_quantification_set:
            return 1

        return 1

    def smooth(self, variable_need_to_be_added_set: set[int]) -> None:
        # The set is empty
        if not len(variable_need_to_be_added_set):
            return

        # TODO smooth
    # endregion

    # endregion Magic method
    def __repr__(self):
        string_temp = super().__repr__()

        string_temp = " ".join((string_temp, f"Literal: {self.__literal}"))

        return string_temp
    # endregion

    # region Property
    @property
    def literal(self):
        return self.__literal

    @property
    def variable(self):
        return self.__variable
    # endregion
