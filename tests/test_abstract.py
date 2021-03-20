# Import
import os
from abc import ABC, abstractmethod
from typing import List, Tuple, Union

# Import exception
import exception.test.test_exception as t_exception


class TestAbstract(ABC):
    __DIRECTORY: str = "tests"
    __ORIGINAL_RESULT_FILE_NAME: str = "original_result.txt"

    def __init__(self, *directories: str, test_name: str = "Test"):
        self.__test_name: str = test_name
        self.__original_result_path: str = self._create_path(*directories, TestAbstract.__ORIGINAL_RESULT_FILE_NAME)

        # File's variables initialization
        self.__path_directory: Union[str, None] = None
        self._files: Union[List[Tuple[str, str]], None] = None

    # region Abstract method
    @abstractmethod
    def _get_actual_result(self) -> str:
        pass
    # endregion

    # region Public method
    def test(self) -> (bool, (str, str)):
        """
        Generate an actual result and compare it with the original result
        :return: (True, None) if the actual and general results are identical. Otherwise (False, (general_result, actual_result)) is returned.
        """

        # Check if the file with the original result exists
        if not self._exists_file(self.__original_result_path):
            raise t_exception.OriginalResultDoesNotExistException(self.__test_name, self.__original_result_path)

        actual_result = self._get_actual_result()
        with open(self.__original_result_path, "r") as original_result_file:
            original_result = original_result_file.read()

        return self._compare_results(actual_result, original_result)

    def save(self) -> None:
        """
        Generate an actual result and save it as the original result
        :return: None
        """

        original_result = self._get_actual_result()

        with open(self.__original_result_path, "w") as original_result_file:
            original_result_file.write(original_result)
    # endregion

    # region Static method
    @staticmethod
    def _create_path(*directories: str) -> str:
        path_directory = os.path.join(os.getcwd(), TestAbstract.__DIRECTORY)
        for directory in directories:
            path_directory = os.path.join(path_directory, directory)

        return path_directory

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
    def _compare_results(actual_result: str, original_result: str) -> (bool, (str, str)):
        """
        Check if two strings are identical. If both strings are identical (True, None) is returned. Otherwise (False, (original_result, actual_result)) is returned.
        :param actual_result: string that represents an actual result
        :param original_result: string that represents the original result
        :return: (bool, (str, str))
        """

        if actual_result == original_result:
            return True, None

        return False, (original_result, actual_result)
    # endregion

    # region Private method
    def __get_files(self) -> List[Tuple[str, str]]:
        """
        Return a list of all files (name, path) in the directory (_path_directory)
        :return: list of files
        """

        return [(file, file_path) for file in os.listdir(self.__path_directory)
                if (os.path.isfile(file_path := os.path.join(self.__path_directory, file)))]
    # endregion

    # region Protected method
    def _set_files(self, *directories: str) -> None:
        """
        Get the files from the directory and save them to the _files
        :return: None
        """

        self.__path_directory = self._create_path(*directories)
        self._files = self.__get_files()
        self._files.sort()  # deterministic
    # endregion

    # region Property
    @property
    def test_name(self):
        return self.__test_name

    @property
    def original_result_path(self):
        return self.__original_result_path
    # endregion
