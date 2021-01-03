# Import
import sortedcontainers


class SortedList(sortedcontainers.SortedList):
    def __init__(self, iterable=None, key=None):
        super().__init__(iterable, key)

    def __str__(self):
        result: str = ""

        for i, e in enumerate(iter(self)):
            if i == 0:
                result = str(e)
            else:
                result = " ".join((result, str(e)))

        return result
