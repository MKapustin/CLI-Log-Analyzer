import abc as _abc
import os as _os
import typing as _typing

import cli_io.common as _common


class AbstractOutputWriter(_abc.ABC, _common.FileValidationMixin):
    allowed_file_types: list[str] = ...

    def __init__(self, path_to_file: _typing.Union[str, _os.PathLike[str]]):
        self.validate_file(path_to_file)

        self._path_to_file = path_to_file

    @_abc.abstractmethod
    def write(self, data_to_write: _typing.Any):
        pass


class SimpleOutputWriter(AbstractOutputWriter):
    allowed_file_types: list[str] = [".txt"]

    def write(self, data_to_write: _typing.Union[str, int, float]):
        with open(file=self._path_to_file, mode="wt") as output_file:
            output_file.write(str(data_to_write))
