# Import
import mmh3
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
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Union[int, None]:
        clause_list = []

        for clause_id in sorted(incidence_graph.clause_id_set(copy=False, multi_occurrence=False)):
            literal_set = incidence_graph.get_clause(clause_id)
            clause_list.append(sorted(literal_set))

        key_string = self._end_delimiter.join([self._delimiter.join(map(str, clause)) for clause in clause_list])
        key = mmh3.hash(key_string)

        return key
    # endregion
