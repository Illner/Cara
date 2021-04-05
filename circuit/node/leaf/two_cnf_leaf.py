# Import
from typing import Set
from formula.pysat_2_cnf import PySat2Cnf
from circuit.node.leaf.leaf_abstract import LeafAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class TwoCnfLeaf(LeafAbstract):
    """
    Circuit 2-CNF leaf representation
    """

    """
    Private PySat2Cnf cnf
    """

    def __init__(self, cnf: PySat2Cnf, id: int = 0):
        self.__cnf: PySat2Cnf = cnf

        size_temp = self.formula_length
        super().__init__(id=id,
                         size=size_temp,
                         node_type=nt_enum.NodeTypeEnum.TWO_CNF,
                         variable_in_circuit_set=self.__cnf.get_variable_set(copy=False),
                         literal_in_circuit_set=self.__cnf.get_literal_set(copy=False))

    # region Override method
    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True) -> bool:
        restricted_assumption_set_temp = self._create_restricted_assumption_set(assumption_set)
        restricted_exist_quantification_set_temp = self._create_restricted_exist_quantification_set(exist_quantification_set)

        # Cache
        key = ""    # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_assumption_set_temp, restricted_exist_quantification_set_temp)
            value = self._get_satisfiable_cache(key)
            if value is not None:
                return value

        model = self.__cnf.get_model(assignment_list=list(restricted_assumption_set_temp))
        is_satisfiable = False if model is None else True

        # Cache
        if use_cache:
            self._add_satisfiable_cache(key, is_satisfiable)

        return is_satisfiable

    def model_counting(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True) -> int:
        restricted_assumption_set_temp = self._create_restricted_assumption_set(assumption_set)

        # Cache
        key = ""    # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_assumption_set_temp, set())
            value = self._get_model_counting_cache(key)
            if value is not None:
                return value

        number_of_models = self.__cnf.get_number_of_models(assignment_list=list(restricted_assumption_set_temp))

        # Cache
        if use_cache:
            self._add_model_counting_cache(key, number_of_models)

        return number_of_models

    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_cache: bool = True) -> float:
        raise c_exception.OperationIsNotSupportedException("minimum default cardinality")
    # endregion

    # region Magic method
    def __str__(self):
        return str(self.__cnf)
    # endregion

    # region Property
    @property
    def number_of_variables(self) -> int:
        return self.__cnf.number_of_variables

    @property
    def number_of_clauses(self) -> int:
        return self.__cnf.number_of_clauses

    @property
    def formula_length(self) -> int:
        return self.__cnf.formula_length
    # endregion