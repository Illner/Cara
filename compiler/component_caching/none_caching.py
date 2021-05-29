# Import
from typing import Union, Tuple, Dict
from formula.incidence_graph import IncidenceGraph
from compiler.component_caching.component_caching_abstract import ComponentCachingAbstract


class NoneCaching(ComponentCachingAbstract):
    """
    None caching (n)
    """

    def __init__(self):
        super().__init__()

    # region Override method
    def generate_key_cache(self, incidence_graph: IncidenceGraph) -> Tuple[Union[str, None], Union[Tuple[Dict[int, int], Dict[int, int]], None]]:
        return None, None
    # endregion
