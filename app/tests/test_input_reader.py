import pathlib as _pathlib

import pytest as _pytest

import app.cli_io as _io

_TEST_INPUT_DATA_REPOSITORY_PATH = (
    _pathlib.Path(__file__).absolute().parents[0] / "test_input_data"
)
_TEST_SQUID_PROXY_ACCESS_LOG_FILENAME = "test_access_log.log"


class TestSquidProxyAccessLogReader:
    @_pytest.fixture
    def reader(self) -> _io.SquidProxyAccessLogReader:
        return _io.SquidProxyAccessLogReader(
            path_to_file=(
                _TEST_INPUT_DATA_REPOSITORY_PATH / _TEST_SQUID_PROXY_ACCESS_LOG_FILENAME
            ).absolute()
        )

    def test_read_size(self, reader):
        read_result = [raw_line for raw_line in reader.read()]
        assert len(read_result) == 9

    def test_read_content(self, reader):
        read_result = [raw_line for raw_line in reader.read()]
        assert read_result[:3] == [
            _io.SquidProxyAccessLogRowDTO(
                timestamp="1157689312.049",
                response_header_size="5006",
                client_ip_address="10.105.21.199",
                http_response_code="TCP_MISS/200",
                response_size="19763",
                http_request_method="CONNECT",
                url="login.yahoo.com:443",
                username="badeyek",
                type_of_access_and_destination_ip_address="DIRECT/209.73.177.115",
                response_type="-",
            ),
            _io.SquidProxyAccessLogRowDTO(
                timestamp="1157689320.327",
                response_header_size="2864",
                client_ip_address="10.105.21.199",
                http_response_code="TCP_MISS/200",
                response_size="10182",
                http_request_method="GET",
                url="http://www.goonernews.com/",
                username="badeyek",
                type_of_access_and_destination_ip_address="DIRECT/207.58.145.61",
                response_type="text/html",
            ),
            _io.SquidProxyAccessLogRowDTO(
                timestamp="1157689320.343",
                response_header_size="1357",
                client_ip_address="10.105.21.199",
                http_response_code="TCP_REFRESH_HIT/304",
                response_size="214",
                http_request_method="GET",
                url="http://www.goonernews.com/styles.css",
                username="badeyek",
                type_of_access_and_destination_ip_address="DIRECT/207.58.145.61",
                response_type="-",
            ),
        ]

    # TODO: Extend tests to check input data validation
