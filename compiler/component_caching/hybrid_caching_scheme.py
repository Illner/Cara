# Import
from typing import Union, Tuple, Dict
from formula.incidence_graph import IncidenceGraph
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract


class HybridCachingScheme(ComponentCachingAbstract):
    """
    Hybrid caching scheme (h)
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Tuple[Union[str, None], Union[Tuple[Dict[int, int], Dict[int, int]], None]]:
        variable_sorted_list = sorted(incidence_graph._variable_set)
        clause_id_sorted_list = sorted(incidence_graph._clause_id_set)

        key_string = self._end_delimiter.join((self._delimiter.join([str(v) for v in variable_sorted_list]),
                                               self._delimiter.join([str(c + 1) for c in clause_id_sorted_list])))

        return key_string, None
    # endregion
