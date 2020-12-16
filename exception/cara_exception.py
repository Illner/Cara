"""
class InputFileDoesNotExistException(Exception):
    def __init__(self, path):
        self.path = path
        self.message = f"The input file ({self.path}) doesn't exist!"

        super().__init__(self.message)

    def __str__(self):
        return self.message
"""