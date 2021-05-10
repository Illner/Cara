# Import
from typing import Union
from formula.incidence_graph import IncidenceGraph
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract


class HybridCachingScheme(ComponentCachingAbstract):
    """
    Hybrid caching scheme (h)
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Union[str, None]:
        variable_sorted_list = sorted(incidence_graph.variable_set(copy=False))
        clause_id_sorted_list = sorted(incidence_graph.clause_id_set(copy=False))

        key_string = self._end_delimiter.join((self._delimiter.join(map(str, variable_sorted_list)),
                                               self._delimiter.join(map(lambda c: str(c + 1), clause_id_sorted_list))))

        return key_string
    # endregion
