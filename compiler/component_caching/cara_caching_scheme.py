# Import
from typing import Union, Dict, Tuple, List
from formula.incidence_graph import IncidenceGraph
from compiler.component_caching.basic_caching_scheme import BasicCachingScheme
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract


class CaraCachingScheme(ComponentCachingAbstract):
    """
    Cara caching scheme (c)
    """

    """
    Private bool multi_occurrence
    Private BasicCachingScheme basic_caching_scheme
    Private int basic_caching_scheme_number_of_variables_threshold
    """

    def __init__(self, multi_occurrence: bool, basic_caching_scheme_number_of_variables_threshold: int):
        super().__init__()

        self.__multi_occurrence: bool = multi_occurrence
        self.__basic_caching_scheme: BasicCachingScheme = BasicCachingScheme()
        self.__basic_caching_scheme_number_of_variables_threshold: int = basic_caching_scheme_number_of_variables_threshold

    # region Override method
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Tuple[Union[str, None], Union[Tuple[Dict[int, int], Dict[int, int]], None]]:
        # The basic caching scheme is used
        if incidence_graph.number_of_variables() <= self.__basic_caching_scheme_number_of_variables_threshold:
            return self.__basic_caching_scheme.generate_key_cache(incidence_graph=incidence_graph)

        used_clause_set = set()
        occurrence_dictionary: Dict[int, List[int, int]] = dict()       # key: a variable, value: (positive, negative)
        mean_dictionary: Dict[int, List[float, float]] = dict()         # key: a variable, value: (positive, negative)

        # Compute occurrences and means
        for clause_id in incidence_graph.clause_id_set(copy=False, multi_occurrence=self.__multi_occurrence):
            used_clause_set.add(clause_id)

            clause_set = incidence_graph.get_clause(clause_id, copy=False)
            clause_len = len(clause_set)

            for literal in clause_set:
                variable = abs(literal)
                sign = 0 if literal > 0 else 1

                # Initialize
                if variable not in occurrence_dictionary:
                    occurrence_dictionary[variable] = [0, 0]
                    mean_dictionary[variable] = [0, 0]

                occurrence_dictionary[variable][sign] += 1
                mean_dictionary[variable][sign] += clause_len

        variable_property_dictionary: Dict[int, Tuple[int, int, float, float, int]] = dict()

        for variable in incidence_graph._variable_set:
            occurrence = occurrence_dictionary[variable]
            mean = mean_dictionary[variable]
            variable_property_dictionary[variable] = occurrence[0], occurrence[1], mean[0], mean[1], variable

        variable_sorted_list = sorted(variable_property_dictionary, key=variable_property_dictionary.get)

        # Mapping
        variable_id_mapping_id_dictionary: Dict[int, int] = dict()  # mapping variable_id -> mapping_id
        mapping_id_variable_id_dictionary: Dict[int, int] = dict()  # mapping mapping_id -> variable_id

        for i, variable in enumerate(variable_sorted_list):
            variable_id_mapping_id_dictionary[variable] = i + 1
            mapping_id_variable_id_dictionary[i + 1] = variable

        clause_mapping_list = []
        for clause_id in used_clause_set:
            clause_set = incidence_graph.get_clause(clause_id, copy=False)
            sorted_clause_mapping = sorted(map(lambda l: variable_id_mapping_id_dictionary[abs(l)] if l > 0 else -variable_id_mapping_id_dictionary[abs(l)], clause_set))
            clause_mapping_list.append(self._delimiter.join([str(lit) for lit in sorted_clause_mapping]))

        clause_mapping_sorted_list = sorted(clause_mapping_list)

        key_string = self._end_delimiter.join(clause_mapping_sorted_list)

        return key_string, (variable_id_mapping_id_dictionary, mapping_id_variable_id_dictionary)
    # endregion
