# Import
from enum import IntEnum, unique


@unique
class LpFormulationObjectiveFunctionEnum(IntEnum):
    HORN_FORMULA = 1                                    # z_1 + z_2 + ... + z_n
    LENGTH_WEIGHTED_HORN_FORMULA = 2                    # |C_1| * z_1 + |C_2| * z_2 + ... + |C_n| * z_n
    SQUARED_LENGTH_WEIGHTED_HORN_FORMULA = 3            # |C_1|^2 * z_1 + |C_2|^2 * z_2 + ... + |C_n|^2 * z_n
    INVERSE_LENGTH_WEIGHTED_HORN_FORMULA = 4            # 1/|C_1| * z_1 + 1/|C_2| * z_2 + ... + 1/|C_n| * z_n
    SQUARED_INVERSE_LENGTH_WEIGHTED_HORN_FORMULA = 5    # (1/|C_1|)^2 * z_1 + (1/|C_2|)^2 * z_2 + ... + (1/|C_n|)^2 * z_n
    RESPECT_DECOMPOSITION_HORN_FORMULA = 6              # 1 * z_1 + c * z_2 + ...


lp_formulation_objective_function_enum_names = [lpfof.name for lpfof in LpFormulationObjectiveFunctionEnum]
lp_formulation_objective_function_enum_values = [lpfof.value for lpfof in LpFormulationObjectiveFunctionEnum]
