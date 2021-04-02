# Import
import sortedcontainers


class SortedList(sortedcontainers.SortedList):
    def __init__(self, iterable=None, key=None):
        super().__init__(iterable, key)

    def str_delimiter(self, delimiter: str = " ", end_delimiter: str = "") -> str:
        result = f"{delimiter}".join(map(str, self))

        if end_delimiter != "":
            result = " ".join((result, end_delimiter))

        return result

    def __str__(self):
        return self.str_delimiter()
