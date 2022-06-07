import abc as _abc
import os as _os
import typing as _typing

import pydantic as _pydantic

import cli_io.common as _common


class BaseInputRowDTO(_pydantic.BaseModel):
    pass


class AbstractInputReader(_abc.ABC, _common.FileValidationMixin):
    allowed_file_types: list[str] = ...

    def __init__(self, path_to_file: _typing.Union[str, _os.PathLike[str]]):
        self.validate_file(path_to_file)

        self._path_to_file = path_to_file

    @_abc.abstractmethod
    def read(self) -> _typing.Iterable[BaseInputRowDTO]:
        pass


class SquidProxyAccessLogRowDTO(BaseInputRowDTO):
    timestamp: float
    response_header_size: int
    client_ip_address: str
    http_response_code: str
    response_size: int
    http_request_method: str
    url: str
    username: str
    type_of_access_and_destination_ip_address: str
    response_type: str


class SquidProxyAccessLogReader(AbstractInputReader):
    allowed_file_types = [".txt", ".log"]

    @staticmethod
    def _clean_raw_line(raw_line: str) -> str:
        raw_line = " ".join(raw_line.split())
        raw_line.strip()
        return raw_line

    def read(self) -> _typing.Iterable[SquidProxyAccessLogRowDTO]:
        with open(file=self._path_to_file, mode="rt") as input_file:
            for line in input_file:
                line = self._clean_raw_line(raw_line=line)

                if line == "":
                    continue

                line = line.split(sep=" ")
                dto_keys = SquidProxyAccessLogRowDTO.__fields__.keys()
                dto_kwargs = {key: value for key, value in zip(dto_keys, line)}
                yield SquidProxyAccessLogRowDTO(**dto_kwargs)
