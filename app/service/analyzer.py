import abc as _abc
import collections as _collections
import math as _math

import cli_io as _io


class AbstractAnalyzer(_abc.ABC):
    def __init__(self, input_reader: _io.AbstractInputReader):
        self._input_reader = input_reader


class SquidProxyAccessLogAnalyzer(AbstractAnalyzer):
    def __init__(self, input_reader: _io.SquidProxyAccessLogReader):
        super().__init__(input_reader=input_reader)

    def _get_frequency_by_ip(self) -> _collections.defaultdict[str, int]:
        frequency_by_ip = _collections.defaultdict(int)
        for log_row_dto in self._input_reader.read():
            frequency_by_ip[log_row_dto.client_ip_address] += 1

        return frequency_by_ip

    def get_most_frequent_ip(self) -> str:
        frequency_by_ip = self._get_frequency_by_ip()
        return max(frequency_by_ip, key=frequency_by_ip.get)

    def get_least_frequent_ip(self) -> str:
        frequency_by_ip = self._get_frequency_by_ip()
        return min(frequency_by_ip, key=frequency_by_ip.get)

    def _get_first_event_in_log(self) -> _io.SquidProxyAccessLogRowDTO:
        first_log_by_time: _io.SquidProxyAccessLogRowDTO = ...
        for log in self._input_reader.read():
            if log.timestamp < getattr(first_log_by_time, "timestamp", _math.inf):
                first_log_by_time = log

        return first_log_by_time

    def _get_last_event_in_log(self) -> _io.SquidProxyAccessLogRowDTO:
        last_log_by_time: _io.SquidProxyAccessLogRowDTO = ...
        for log in self._input_reader.read():
            if log.timestamp > getattr(last_log_by_time, "timestamp", -1):
                last_log_by_time = log

        return last_log_by_time

    def _get_events_count(self) -> int:
        events_count = 0
        for _ in self._input_reader.read():
            events_count += 1

        return events_count

    def get_avg_events_per_second(self) -> float:
        """Calculate average events amount per second"""
        events_count = self._get_events_count()
        first_event = self._get_first_event_in_log()
        last_event = self._get_last_event_in_log()

        avg_events_per_second = events_count / (
            last_event.timestamp - first_event.timestamp
        )
        return avg_events_per_second

    def get_total_amount_of_bytes_exchanged(self) -> int:
        total_amount_of_bytes = 0
        for log in self._input_reader.read():
            total_amount_of_bytes += log.response_size

        return total_amount_of_bytes
