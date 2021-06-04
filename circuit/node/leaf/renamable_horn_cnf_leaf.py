# Import
from typing import Set, Tuple, Dict, Union
from formula.pysat_horn_cnf import PySatHornCnf
from circuit.node.node_abstract import NodeAbstract
from circuit.node.leaf.leaf_abstract import LeafAbstract

# Import exception
import exception.circuit.circuit_exception as c_exception

# Import enum
import circuit.node.node_type_enum as nt_enum


class RenamableHornCnfLeaf(LeafAbstract):
    """
    Circuit renamable Horn CNF leaf representation
    """

    """
    Private PySatHornCnf cnf
    Private Set<int> renaming_function
    """

    def __init__(self, cnf: PySatHornCnf, renaming_function: Set[int], id: int = 0):
        self.__cnf: PySatHornCnf = cnf
        self.__renaming_function: Set[int] = renaming_function

        size_temp = self.__cnf.formula_length
        super().__init__(id=id,
                         size=size_temp,
                         node_type=nt_enum.NodeTypeEnum.RENAMABLE_HORN_CNF,
                         variable_in_circuit_set=self.__cnf._variable_set,
                         literal_in_circuit_set=self.__cnf._literal_set)

    # region Override method
    def is_satisfiable(self, assumption_set: Set[int], exist_quantification_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> bool:
        restricted_assumption_set_temp = self._create_restricted_assumption_set(assumption_set=assumption_set,
                                                                                variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)
        restricted_exist_quantification_set_temp = self._create_restricted_exist_quantification_set(exist_quantification_set=exist_quantification_set,
                                                                                                    mapping_id_variable_id_dictionary=mapping_id_variable_id_dictionary)

        # Cache
        key = None  # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_assumption_set_temp, restricted_exist_quantification_set_temp)
            value = self._get_satisfiable_cache(key)
            if value is not None:
                return value

        # Mapping is used
        if variable_id_mapping_id_dictionary is not None:
            restricted_assumption_set_temp = NodeAbstract.use_mapping_on_literal_set(literal_set=restricted_assumption_set_temp,
                                                                                     mapping_dictionary=variable_id_mapping_id_dictionary)

        restricted_renamed_assumption_set_temp = self.__rename_assignment(restricted_assumption_set_temp)
        model = self.__cnf.get_model(assignment_list=list(restricted_renamed_assumption_set_temp))
        is_satisfiable = False if model is None else True

        # Cache
        if use_cache:
            self._add_satisfiable_cache(key, is_satisfiable)

        return is_satisfiable

    def model_counting(self, assumption_set: Set[int], use_cache: bool = True,
                       mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                       variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> int:
        restricted_assumption_set_temp = self._create_restricted_assumption_set(assumption_set=assumption_set,
                                                                                variable_id_mapping_id_dictionary=variable_id_mapping_id_dictionary)

        # Cache
        key = None  # initialization
        if use_cache:
            key = self._generate_key_cache(restricted_assumption_set_temp, set())
            value = self._get_model_counting_cache(key)
            if value is not None:
                return value

        # Mapping is used
        if variable_id_mapping_id_dictionary is not None:
            restricted_assumption_set_temp = NodeAbstract.use_mapping_on_literal_set(literal_set=restricted_assumption_set_temp,
                                                                                     mapping_dictionary=variable_id_mapping_id_dictionary)

        restricted_renamed_assumption_set_temp = self.__rename_assignment(restricted_assumption_set_temp)
        number_of_models = self.__cnf.get_number_of_models(assignment_list=list(restricted_renamed_assumption_set_temp))

        # Cache
        if use_cache:
            self._add_model_counting_cache(key, number_of_models)

        return number_of_models

    def minimum_default_cardinality(self, observation_set: Set[int], default_set: Set[int], use_cache: bool = True,
                                    mapping_id_variable_id_dictionary: Union[Dict[int, int], None] = None,
                                    variable_id_mapping_id_dictionary: Union[Dict[int, int], None] = None) -> float:
        raise c_exception.OperationIsNotSupportedException("minimum default-cardinality")

    def str_with_mapping(self) -> Tuple[str, Dict[int, int]]:
        return self.__cnf.str_with_mapping(horn_renaming_function=self.__renaming_function)
    # endregion

    # region Private method
    def __rename_assignment(self, assignment_set: Set[int]) -> Set[int]:
        """
        :param assignment_set: an assignment set
        :return: the renamed assignment based on the renaming function
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
        return self.__cnf.str_renaming_function(horn_renaming_function=self.__renaming_function)
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
