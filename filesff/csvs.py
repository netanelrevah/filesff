from csv import DictReader, DictWriter
from csv import reader as csv_reader
from csv import writer as csv_writer
from dataclasses import dataclass
from typing import Any, Iterator, Sequence, TextIO

from filesff.core.accessors import FileAccessor
from filesff.core.formatters import TextFileFormatter
from filesff.paths import PathFileHandle


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
class CsvFileDictFormatter(TextFileFormatter):
    def load(self, reader: TextIO, **kwargs) -> Any:
        return CsvFileListsLoader(csv_reader(reader))

    def dump(self, writer: TextIO, value: Any, **kwargs):
        fields_names = kwargs["fields_names"]
        line_terminator = kwargs.get("line_terminator", "\n")
        return CsvFileListsDumper(csv_writer(writer, lineterminator=line_terminator), fields_names=fields_names)

    def create_loader(self, reader: TextIO, **_) -> CsvFileDictsLoader:
        return CsvFileDictsLoader(DictReader(reader))

    def create_dumper(self, writer: TextIO, **kwargs):
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
class CsvFileListsFormatter(TextFileFormatter):
    def create_loader(self, reader: TextIO, **_) -> CsvFileListsLoader:
        return CsvFileListsLoader(csv_reader(reader))

    def create_dumper(self, writer: TextIO, **kwargs):
        fields_names = kwargs["fields_names"]
        line_terminator = kwargs.get("line_terminator", "\n")
        return CsvFileListsDumper(csv_writer(writer, lineterminator=line_terminator), fields_names=fields_names)

    def load(self, reader: TextIO, **_) -> Iterator[list]:
        loader = self.create_loader(reader)
        if loader.fields_names:
            yield loader.fields_names
        yield from loader

    def dump(self, writer: TextIO, value: Sequence[list], **kwargs):
        dumper = self.create_dumper(writer, **kwargs)
        dumper.dump_header()
        for row in value:
            dumper.dump_row(row)


def csv_file_dicts_accessor(file_path, file_handle_cls=PathFileHandle):
    return FileAccessor.of_path(
        file_path=file_path,
        formatter=CsvFileDictFormatter(),
        file_handle_cls=file_handle_cls,
    )


def temp_csv_file_dicts_accessor(file_handle_cls=PathFileHandle):
    return FileAccessor.of_temp(
        formatter=CsvFileDictFormatter(),
        file_handle_cls=file_handle_cls,
    )


def csv_file_lists_accessor(file_path, file_handle_cls=PathFileHandle):
    return FileAccessor.of_path(
        file_path=file_path,
        formatter=CsvFileListsFormatter(),
        file_handle_cls=file_handle_cls,
    )


def temp_csv_file_lists_accessor(file_handle_cls=PathFileHandle):
    return FileAccessor.of_temp(
        formatter=CsvFileListsFormatter(),
        file_handle_cls=file_handle_cls,
    )
