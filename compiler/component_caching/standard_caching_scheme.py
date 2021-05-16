# Import
from typing import Union
from formula.incidence_graph import IncidenceGraph
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract


class StandardCachingScheme(ComponentCachingAbstract):
    """
    Standard caching scheme (s)
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Union[str, None]:
        clause_list = []

        for clause_id in incidence_graph.clause_id_set(copy=False):
            clause_sorted_list = incidence_graph.get_sorted_clause(clause_id, copy=False)
            clause_list.append(self._delimiter.join([str(lit) for lit in clause_sorted_list]))

        key_string = self._end_delimiter.join(clause_list)

        return key_string
    # endregion
