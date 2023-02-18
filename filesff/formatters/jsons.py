from dataclasses import dataclass
from typing import IO, Any, AnyStr, Iterator

from filesff.core.formatters import FileFormatter, FullFileFormatter

try:
    import ujson as json
except ImportError:
    import json  # type: ignore


@dataclass
class JsonFormatter(FullFileFormatter):
    indentation: int

    def load(self, reader: IO, **_) -> AnyStr:
        return json.load(fp=reader)

    def dump(self, writer: IO, value: Any, **_):
        json.dump(obj=value, fp=writer, indent=self.indentation)


@dataclass
class JsonLinesFileLoader:
    reader: IO

    def __iter__(self):
        for line in self.reader:
            yield json.loads(line)


@dataclass
class JsonLinesFileDumper:
    writer: IO

    def dump_object(self, message):
        self.writer.write(json.dumps(message, indent=0))


class JsonLinesFormatter(FileFormatter):
    def create_loader(self, reader: IO, **_):
        return JsonLinesFileLoader(reader)

    def create_dumper(self, writer: IO, **_):
        return JsonLinesFileDumper(writer)

    def load(self, reader: IO, **kwargs) -> Iterator[Any]:
        loader = self.create_loader(reader, **kwargs)
        yield from loader

    def dump(self, writer: IO, value: Iterator[Any], **_):
        dumper = self.create_dumper(writer)
        for message in value:
            dumper.dump_object(message)
