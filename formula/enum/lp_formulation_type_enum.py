# Import
from enum import IntEnum, unique


@unique
class LpFormulationTypeEnum(IntEnum):
    # Number of Horn formulae
    HORN_FORMULA = 1                                    # z_1 + z_2 + ... + z_n
    LENGTH_WEIGHTED_HORN_FORMULA = 2                    # |C_1| * z_1 + |C_2| * z_2 + ... + |C_n| * z_n
    SQUARED_LENGTH_WEIGHTED_HORN_FORMULA = 3            # |C_1|^2 * z_1 + |C_2|^2 * z_2 + ... + |C_n|^2 * z_n
    INVERSE_LENGTH_WEIGHTED_HORN_FORMULA = 4            # 1/|C_1| * z_1 + 1/|C_2| * z_2 + ... + 1/|C_n| * z_n
    SQUARED_INVERSE_LENGTH_WEIGHTED_HORN_FORMULA = 5    # (1/|C_1|)^2 * z_1 + (1/|C_2|)^2 * z_2 + ... + (1/|C_n|)^2 * z_n
    RESPECT_DECOMPOSITION_HORN_FORMULA = 6              # 1 * z_1 + c * z_2 + ...

    # Number of edges
    NUMBER_OF_EDGES = 7
    RESPECT_DECOMPOSITION_NUMBER_OF_EDGES = 8

    # Number of vertices
    NUMBER_OF_VERTICES = 9
    RESPECT_DECOMPOSITION_NUMBER_OF_VERTICES = 10

    # Vertex cover
    VERTEX_COVER = 11
    RESPECT_DECOMPOSITION_VERTEX_COVER = 12


lp_formulation_type_enum_names = [lpft.name for lpft in LpFormulationTypeEnum]
lp_formulation_type_enum_values = [lpft.value for lpft in LpFormulationTypeEnum]
