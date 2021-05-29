# Import
from typing import Union, Dict, Tuple
from formula.incidence_graph import IncidenceGraph
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract


class CaraCachingScheme(ComponentCachingAbstract):
    """
    Cara caching scheme (c)
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Tuple[Union[str, None], Union[Tuple[Dict[int, int], Dict[int, int]], None]]:
        variable_property_dictionary: Dict[int, Tuple[int, int, float, float, int]] = dict()

        # Compute occurrences and means
        for variable in incidence_graph.variable_set(copy=False):
            occurrence_positive = incidence_graph.literal_number_of_occurrences(variable)
            occurrence_negative = incidence_graph.literal_number_of_occurrences(-variable)
            mean_positive = incidence_graph.literal_sum_lengths_clauses(variable)
            mean_negative = incidence_graph.literal_sum_lengths_clauses(-variable)

            variable_property_dictionary[variable] = occurrence_positive, occurrence_negative, mean_positive, mean_negative, variable

        variable_sorted_list = sorted(variable_property_dictionary, key=variable_property_dictionary.get)

        # Mapping
        variable_id_mapping_id_dictionary: Dict[int, int] = dict()  # mapping variable_id -> mapping_id
        mapping_id_variable_id_dictionary: Dict[int, int] = dict()  # mapping mapping_id -> variable_id

        for i, variable in enumerate(variable_sorted_list):
            variable_id_mapping_id_dictionary[variable] = i + 1
            mapping_id_variable_id_dictionary[i + 1] = variable

        clause_mapping_list = []
        for clause_id in incidence_graph.clause_id_set(copy=False):
            clause_set = incidence_graph.get_clause(clause_id, copy=False)
            sorted_clause_mapping = sorted(map(lambda l: variable_id_mapping_id_dictionary[abs(l)] if l > 0 else -variable_id_mapping_id_dictionary[abs(l)], clause_set))
            clause_mapping_list.append(self._delimiter.join([str(lit) for lit in sorted_clause_mapping]))

        clause_mapping_sorted_list = sorted(clause_mapping_list)

        key_string = self._end_delimiter.join(clause_mapping_sorted_list)

        return key_string, (variable_id_mapping_id_dictionary, mapping_id_variable_id_dictionary)
    # endregion
