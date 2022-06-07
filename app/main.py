import os as _os
import argparse as _argparse
import enum as _enum
import service.analyzer as _analyzer
import cli_io as _io
import typing as _typing


class OperationChoices(_enum.Enum):
    MOST_FREQUENT_IP = "MOST_FREQUENT_IP"
    LEAST_FREQUENT_IP = "LEAST_FREQUENT_IP"
    AVG_EVENTS_PER_SECOND = "AVG_EVENTS_PER_SECOND"
    TOTAL_BYTES_EXCHANGED = "TOTAL_BYTES_EXCHANGED"

    def __str__(self):
        return self.value


class CLICommand:
    def __init__(self, command_description: str):
        self._command_description = command_description

    def create_parser(self):
        return _argparse.ArgumentParser(description=self._command_description)

    def add_arguments(self, parser: _argparse.ArgumentParser) -> _argparse.Namespace:
        parser.add_argument(
            "--operation",
            help="How to process the input log file?",
            default=OperationChoices.MOST_FREQUENT_IP,
            choices=list(OperationChoices),
            type=OperationChoices,
        )
        parser.add_argument(
            "-i", "--input-file", type=str, required=True, help="The input file path"
        )

        parser.add_argument(
            "-o", "--output-file", type=str, required=True, help="The output file path"
        )

        args = parser.parse_args()
        return args

    def handle(
        self,
        input_file_path: _typing.Union[str, _os.PathLike[str]],
        output_file_path: _typing.Union[str, _os.PathLike[str]],
        operation: OperationChoices,
    ) -> _typing.Union[str, int, float]:
        reader = _io.SquidProxyAccessLogReader(path_to_file=input_file_path)
        writer = _io.SimpleOutputWriter(path_to_file=output_file_path)
        analyzer = _analyzer.SquidProxyAccessLogAnalyzer(input_reader=reader)

        operation_by_key = {
            OperationChoices.MOST_FREQUENT_IP: analyzer.get_most_frequent_ip,
            OperationChoices.LEAST_FREQUENT_IP: analyzer.get_least_frequent_ip,
            OperationChoices.AVG_EVENTS_PER_SECOND: analyzer.get_avg_events_per_second,
            OperationChoices.TOTAL_BYTES_EXCHANGED: analyzer.get_total_amount_of_bytes_exchanged,
        }

        result = operation_by_key[operation]()
        writer.write(data_to_write=result)

        return result

    def run(self):
        parser = self.create_parser()
        args = self.add_arguments(parser)

        # TODO: Use logging instead of print()
        print(
            self.handle(
                input_file_path=args.input_file,
                output_file_path=args.output_file,
                operation=args.operation,
            )
        )


def main():
    cmd = CLICommand(
        command_description="A command line tool to analyze the content of log files."
    )
    cmd.run()


if __name__ == "__main__":
    main()
