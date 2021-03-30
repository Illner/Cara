# Import
from enum import IntEnum, unique


@unique
class PySatCnfEnum(IntEnum):
    CNF = 1
    TWO_CNF = 2
    HORN_CNF = 3


pysat_cnf_enum_names = [psc.name for psc in PySatCnfEnum]
pysat_cnf_enum_values = [psc.value for psc in PySatCnfEnum]
