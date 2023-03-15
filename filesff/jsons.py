from dataclasses import dataclass
from typing import Any, AnyStr, Iterator, TextIO

from filesff.core.formatters import FullTextFileFormatter, TextFileFormatter

try:
    import ujson as json
except ImportError:
    import json  # type: ignore


@dataclass
class JsonFormatter(FullTextFileFormatter):
    def load(self, reader: TextIO, **_) -> AnyStr:
        return json.load(reader)

    def dump(self, writer: TextIO, value: Any, **kwargs):
        indentation = kwargs.get("indentation", 2)
        json.dump(value, writer, indent=indentation)


@dataclass
class JsonLinesFileLoader:
    reader: TextIO

    def __iter__(self):
        for line in self.reader:
            yield json.loads(line)


@dataclass
class JsonLinesFileDumper:
    writer: TextIO

    _first_object: bool = True

    def dump_one(self, value: Any):
        if not self._first_object:
            self.writer.write("\n")
        self._first_object = False
        self.writer.write(json.dumps(value, indent=0))


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
            dumper.dump_one(message)
