import os as _os
import typing as _typing

INVALID_PATH_MSG = "Provided file path is invalid: "
INVALID_FILETYPE_MSG = "Provided file type is invalid: "


class FileValidationMixin:
    def _is_valid_file_path(self, path: _typing.Union[str, _os.PathLike[str]]) -> bool:
        return _os.path.isfile(path)

    def _is_valid_filetype(
        self, path: _typing.Union[str, _os.PathLike[str]], allowed_file_types: list[str]
    ) -> bool:
        return any(str(path).endswith(file_type) for file_type in allowed_file_types)

    def validate_file(self, path: _typing.Union[str, _os.PathLike[str]]):
        # TODO: Use logging instead of print()
        if not self._is_valid_filetype(path, self.allowed_file_types):
            print(INVALID_FILETYPE_MSG + str(path))
            quit()

        if not self._is_valid_file_path(path):
            print(INVALID_PATH_MSG + str(path))
            quit()
