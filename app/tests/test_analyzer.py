import typing as _typing

import pytest as _pytest

import app.cli_io.input_reader as _input_reader
import app.service.analyzer as _analyzer


class TestSquidProxyAccessLogAnalyzer:
    class FakeSquidProxyAccessLogReader:
        def __init__(self, path_to_file: str):
            pass

        def read(self) -> _typing.Iterable[_input_reader.SquidProxyAccessLogRowDTO]:
            return [
                _input_reader.SquidProxyAccessLogRowDTO(
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
                _input_reader.SquidProxyAccessLogRowDTO(
                    timestamp="1157689320.327",
                    response_header_size="2864",
                    client_ip_address="10.104.21.199",
                    http_response_code="TCP_MISS/200",
                    response_size="10182",
                    http_request_method="GET",
                    url="http://www.goonernews.com/",
                    username="badeyek",
                    type_of_access_and_destination_ip_address="DIRECT/207.58.145.61",
                    response_type="text/html",
                ),
                _input_reader.SquidProxyAccessLogRowDTO(
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

    @_pytest.fixture
    def fake_reader(self):
        return self.FakeSquidProxyAccessLogReader(path_to_file="fake_path")

    @_pytest.fixture
    def analyzer(self, fake_reader) -> _analyzer.SquidProxyAccessLogAnalyzer:
        return _analyzer.SquidProxyAccessLogAnalyzer(input_reader=fake_reader)

    def test_get_most_frequent_ip(self, analyzer):
        assert analyzer.get_most_frequent_ip() == "10.105.21.199"

    def test_get_least_frequent_ip(self, analyzer):
        assert analyzer.get_least_frequent_ip() == "10.104.21.199"

    def test_get_avg_events_per_second(self, analyzer):
        assert analyzer.get_avg_events_per_second() == 3 / (
            1157689320.343 - 1157689312.049
        )

    def test_get_total_amount_of_bytes_exchanged(self, analyzer):
        assert analyzer.get_total_amount_of_bytes_exchanged() == 19763 + 10182 + 214
