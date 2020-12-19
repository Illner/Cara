# Import
import os
from abc import ABC, abstractmethod


class TestAbstract(ABC):
    __FOLDER = "tests"

    def __init__(self, *dictionaries: str):
        self._test_name = "Test"
        self._original_result_file_name = "original_result.txt"
        self._path_dictionary = self._create_path(*dictionaries)
        self._files = self.__get_files()
        self._files.sort()  # deterministic

    # region Abstract method
    @abstractmethod
    def test(self) -> (bool, str):
        pass

    @abstractmethod
    def save(self):
        pass
    # endregion

    # region Static method
    @staticmethod
    def _create_path(*dictionaries: str) -> str:
        path_dictionary = os.path.join(os.getcwd(), TestAbstract.__FOLDER)
        for dictionary in dictionaries:
            path_dictionary = os.path.join(path_dictionary, dictionary)

        return path_dictionary

    @staticmethod
    def _exists_file(file_path: str) -> bool:
        """
        Check if the file exists
        :param file_path: the path of the file
        :return: True if the file exists. Otherwise False is returned.
        """

        if os.path.isfile(file_path):
            return True

        return False

    @staticmethod
    def _compare_results(actual_result: str, original_result: str) -> (bool, str):
        """
        Check if two strings are identical. If both strings are identical (True, "") is returned. Otherwise (False, original_result + actual_result) is returned.
        :param actual_result: string that represents an actual result
        :param original_result: string that represents the original result
        :return: (bool, str)
        """

        if actual_result == original_result:
            return True, ""

        result = "\n".join(("Original result", original_result, "Actual result", actual_result))
        return False, result
    # endregion

    # region Private method
    def __get_files(self) -> list:
        """
        Return a list of all files (name, path) in the dictionary (_path_dictionary)
        :return: list of files
        """

        return [(file, file_path) for file in os.listdir(self._path_dictionary)
                if (os.path.isfile(file_path := os.path.join(self._path_dictionary, file)))]
    # endregion

    # region Property
    @property
    def test_name(self):
        return self._test_name
    # endregion
