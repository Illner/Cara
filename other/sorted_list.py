# Import
import sortedcontainers


class SortedList(sortedcontainers.SortedList):
    def __init__(self, iterable=None, key=None):
        super().__init__(iterable, key)

    def __str__(self):
        return " ".join(map(str, self))
