from dataclasses import dataclass
from typing import Any, AnyStr, Iterator, TextIO

from filesff.core.formatters import FullTextFileFormatter, TextFileFormatter

try:
    import ujson as json
except ImportError:
    import json  # type: ignore


@dataclass
class JsonFormatter(FullTextFileFormatter):
    indentation: int = 2

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
