from dataclasses import dataclass
from typing import Any, AnyStr, Iterator, TextIO

from filesff.core.accessors import FileAccessor, FullFileAccessor
from filesff.core.formatters import FullTextFileFormatter, TextFileFormatter
from filesff.core.handlers import FSFileHandle

try:
    import ujson as json
except ImportError:
    import json  # type: ignore


@dataclass
class JsonFormatter(FullTextFileFormatter):
    indentation: int

    def load(self, reader: TextIO, **_) -> AnyStr:
        return json.load(fp=reader)

    def dump(self, writer: TextIO, value: Any, **_):
        json.dump(obj=value, fp=writer, indent=self.indentation)


@dataclass
class JsonLinesFileLoader:
    reader: TextIO

    def __iter__(self):
        for line in self.reader:
            yield json.loads(line)


@dataclass
class JsonLinesFileDumper:
    writer: TextIO

    def dump_object(self, message):
        self.writer.write(json.dumps(message, indent=0))


class JsonLinesFormatter(TextFileFormatter):
    def create_loader(self, reader: TextIO, **_):
        return JsonLinesFileLoader(reader)

    def create_dumper(self, writer: TextIO, **_):
        return JsonLinesFileDumper(writer)

    def load(self, reader: TextIO, **kwargs) -> Iterator[Any]:
        loader = self.create_loader(reader, **kwargs)
        yield from loader

    def dump(self, writer: TextIO, value: Iterator[Any], **_):
        dumper = self.create_dumper(writer)
        for message in value:
            dumper.dump_object(message)


def json_file_accessor(file_path, file_handle_cls=FSFileHandle, indentation=2):
    return FullFileAccessor.of(
        file_path=file_path,
        formatter=JsonFormatter(indentation=indentation),
        file_handle_cls=file_handle_cls,
    )


def temp_json_file_accessor(file_handle_cls=FSFileHandle, indentation=2):
    return FullFileAccessor.of_temp(
        formatter=JsonFormatter(indentation=indentation),
        file_handle_cls=file_handle_cls,
    )


def json_lines_file_accessor(file_path, file_handle_cls=FSFileHandle):
    return FileAccessor.of(
        file_path=file_path,
        formatter=JsonLinesFormatter(),
        file_handle_cls=file_handle_cls,
    )


def temp_json_lines_file_accessor(file_handle_cls=FSFileHandle):
    return FileAccessor.of_temp(
        formatter=JsonLinesFormatter(),
        file_handle_cls=file_handle_cls,
    )
