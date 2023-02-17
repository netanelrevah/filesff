from csv import DictReader, DictWriter
from csv import reader as csv_reader
from csv import writer as csv_writer
from dataclasses import dataclass
from typing import IO, Any, Iterator, Sequence

from filesff.core.formatters import FileFormatter, FullFileFormatter


@dataclass
class CsvFileDictsLoader:
    dict_reader: DictReader

    @property
    def fields_names(self):
        return self.dict_reader.fieldnames

    def __iter__(self):
        yield from self.dict_reader


@dataclass
class CsvFileDictDumper:
    dict_writer: DictWriter

    @property
    def fields_names(self):
        return self.dict_writer.fieldnames

    def dump_header(self):
        self.dict_writer.writeheader()

    def dump_row(self, row):
        self.dict_writer.writerow(row)


@dataclass
class CsvFileDictFormatter(FileFormatter):
    def load(self, reader: IO, **kwargs) -> Any:
        return CsvFileListsLoader(csv_reader(reader))

    def dump(self, writer: IO, value: Any, **kwargs):
        fields_names = kwargs["fields_names"]
        line_terminator = kwargs.get("line_terminator", "\n")
        return CsvFileListsDumper(csv_writer(writer, lineterminator=line_terminator), fields_names=fields_names)

    def create_loader(self, reader: IO, **_) -> CsvFileDictsLoader:
        return CsvFileDictsLoader(DictReader(reader))

    def create_dumper(self, writer: IO, **kwargs):
        fields_names = kwargs["fields_names"]
        line_terminator = kwargs.get("line_terminator", "\n")
        return CsvFileDictDumper(DictWriter(writer, fieldnames=fields_names, lineterminator=line_terminator))


@dataclass
class CsvFileListsLoader:
    csv_reader: csv_reader  # type: ignore

    _field_names: list | None = None

    @property
    def fields_names(self) -> list | None:
        if self._field_names is None:
            try:
                self._field_names = next(self.csv_reader)
            except StopIteration:
                pass
        return self._field_names

    def __iter__(self):
        if self.csv_reader.line_num == 0:
            _ = self.fields_names
        yield from self.csv_reader


@dataclass
class CsvFileListsDumper:
    csv_writer: csv_writer  # type: ignore
    fields_names: list

    def dump_header(self):
        self.csv_writer.writerow(self.fields_names)

    def dump_row(self, row):
        self.csv_writer.writerow(row)


@dataclass
class CsvFileListsFormatter(FileFormatter, FullFileFormatter):
    def create_loader(self, reader: IO, **_) -> CsvFileListsLoader:
        return CsvFileListsLoader(csv_reader(reader))

    def create_dumper(self, writer: IO, **kwargs):
        fields_names = kwargs["fields_names"]
        line_terminator = kwargs.get("line_terminator", "\n")
        return CsvFileListsDumper(csv_writer(writer, lineterminator=line_terminator), fields_names=fields_names)

    def load(self, reader: IO, **_) -> Iterator[list]:
        loader = self.create_loader(reader)
        if loader.fields_names:
            yield loader.fields_names
        yield from loader

    def dump(self, writer: IO, value: Sequence[list], **kwargs):
        dumper = self.create_dumper(writer, **kwargs)
        dumper.dump_header()
        for row in value:
            dumper.dump_row(row)
