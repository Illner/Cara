# Import
import mmh3
from typing import Union
from formula.incidence_graph import IncidenceGraph
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract


class BasicCachingScheme(ComponentCachingAbstract):
    """
    Basic caching scheme (b)
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Union[int, None]:
        variable_sorted_list = sorted(incidence_graph.variable_set())
        clause_list = []

        for clause_id in incidence_graph.clause_id_set(multi_occurrence=False):
            literal_set = incidence_graph.get_clause(clause_id)
            clause_list.append(sorted(literal_set))

        key_string = self._end_delimiter_2.join((self._delimiter.join(map(str, variable_sorted_list)),
                                                 self._end_delimiter.join([self._delimiter.join(map(str, clause)) for clause in sorted(clause_list)])))
        key = mmh3.hash(key_string)

        return key
    # endregion