from dataclasses import dataclass
from typing import Any, List

from filesff.accessors.base import FileAccessor
from filesff.accessors.json_files import JsonFormatter
from filesff.core.files_handlers import FileHandle

try:
    import ujson as json
except ImportError:
    import json


@dataclass
class JsonLinesFile(FileAccessor):
    handle: FileHandle
    formatter: JsonFormatter = json

    def load(self):
        return list(self.lines())

    def dump(self, value: List[Any]):
        with self.handle.create_text_writer() as writer:
            for item in value:
                writer.write(self.formatter.dumps(item) + "\n")

    def lines(self):
        with self.handle.create_text_reader() as reader:
            for line in reader:
                yield self.formatter.loads(line)
