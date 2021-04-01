# Import
from typing import Set
from formula.pysat_horn_cnf import PySatHornCnf
from circuit.node.leaf.leaf_abstract import LeafAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class HornCnfLeaf(LeafAbstract):
    """
    Circuit Horn CNF leaf representation
    """

    """
    Private PySatHornCnf cnf
    Private Set<int> renaming_function
    """

    def __init__(self, cnf: PySatHornCnf, renaming_function: Set[int], id: int = 0):
        self.__cnf: PySatHornCnf = cnf
        self.__renaming_function: Set[int] = renaming_function

        size_temp = self.formula_length
        super().__init__(id=id,
                         size=size_temp,
                         node_type=nt_enum.NodeTypeEnum.HORN_CNF,
                         variable_in_circuit_set=self.__cnf.get_variable_set(),
                         literal_in_circuit_set=self.__cnf.get_literal_set())

    # region Override method
    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_caches: bool = True) -> bool:
        assumption_restricted_set_temp = set(filter(lambda l: self._exist_variable_in_circuit_set(abs(l)), assumption_set))
        renamed_assumption_restricted_set_temp = self.__rename_assignment(assumption_restricted_set_temp)
        exist_quantification_restricted_set_temp = exist_quantification_set.intersection(self._get_variable_in_circuit_set())

        # Cache
        key = ""  # initialization
        if use_caches:
            key = self._generate_key_cache(renamed_assumption_restricted_set_temp, exist_quantification_restricted_set_temp)
            value = self._get_satisfiable_cache(key)
            if value is not None:
                return value

        model = self.__cnf.get_model(assignment_list=list(renamed_assumption_restricted_set_temp))
        is_satisfiable = False if model is None else True

        # Cache
        if use_caches:
            self._add_satisfiable_cache(key, is_satisfiable)

        return is_satisfiable

    def model_counting(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_caches: bool = True) -> int:
        assumption_restricted_set_temp = set(filter(lambda l: self._exist_variable_in_circuit_set(abs(l)), assumption_set))
        renamed_assumption_restricted_set_temp = self.__rename_assignment(assumption_restricted_set_temp)

        # Cache
        key = ""  # initialization
        if use_caches:
            key = self._generate_key_cache(renamed_assumption_restricted_set_temp, set())
            value = self._get_model_counting_cache(key)
            if value is not None:
                return value

        number_of_models = self.__cnf.get_number_of_models(assignment_list=list(renamed_assumption_restricted_set_temp))

        # Cache
        if use_caches:
            self._add_model_counting_cache(key, number_of_models)

        return number_of_models

    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_caches: bool = True) -> float:
        raise c_exception.OperationIsNotSupportedException("minimum default cardinality")
    # endregion

    # region Private method
    def __rename_assignment(self, assignment_set: Set[int]) -> Set[int]:
        """
        :return: renamed assignment based on the renaming function
        """

        renamed_assignment_set = set()

        for lit in assignment_set:
            var = abs(lit)
            # Positive
            if var in self.__renaming_function:
                renamed_assignment_set.add(-lit)
            # Negative
            else:
                renamed_assignment_set.add(lit)

        return renamed_assignment_set
    # endregion

    # region Magic method
    def __str__(self):
        return str(self.__cnf)
    # endregion

    # region Property
    @property
    def number_of_variables(self):
        return self.__cnf.number_of_variables

    @property
    def number_of_clauses(self):
        return self.__cnf.number_of_clauses

    @property
    def formula_length(self):
        return self.__cnf.formula_length
    # endregion
