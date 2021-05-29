# Import
from typing import Union, Tuple, Dict
from formula.incidence_graph import IncidenceGraph
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract


class BasicCachingScheme(ComponentCachingAbstract):
    """
    Basic caching scheme (b)
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Tuple[Union[str, None], Union[Tuple[Dict[int, int], Dict[int, int]], None]]:
        self._clear_multi_occurrence_cache()    # cache

        variable_sorted_list = sorted(incidence_graph.variable_set(copy=False))
        clause_list = []

        for clause_id in incidence_graph.clause_id_set(copy=False):
            clause_sorted_list = incidence_graph.get_sorted_clause(clause_id, copy=False)

            clause_key_string = self._generate_key_multi_occurrence_cache(clause_sorted_list)
            # Multi-occurrent clause
            if self._exist_multi_occurrence_cache(clause_key_string):
                continue

            self._add_multi_occurrence_cache(clause_key_string)
            clause_list.append(clause_key_string)

        key_string = self._end_delimiter_2.join((self._delimiter.join([str(v) for v in variable_sorted_list]),
                                                 self._end_delimiter.join(sorted(clause_list))))

        self._clear_multi_occurrence_cache()    # cache
        return key_string, None
    # endregion
