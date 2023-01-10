from csv import DictReader, DictWriter
from dataclasses import dataclass
from typing import IO, AnyStr, Generator, Iterator

from filesff.core.formatters import ContinuesFileFormatter


@dataclass
class CsvDictFormatter(ContinuesFileFormatter):
    def load_continuously(self, reader: IO) -> Iterator[AnyStr]:
        yield from DictReader(reader)

    def dump_continuously(self, writer: IO) -> Generator[None, dict | list, None]:
        fieldnames = yield None
        dict_writer = DictWriter(writer, fieldnames=fieldnames)
        dict_writer.writeheader()
        while True:
            row = yield None
            dict_writer.writerow(row)
