from dataclasses import dataclass
from typing import Any, List

from filesff.file_accessors import FileAccessor
from filesff.files_handlers import FileHandle
from filesff.json_files import JsonFormatter

try:
    import ujson as json
except ImportError:
    import json


@dataclass
class JsonLinesFile(FileAccessor):
    handle: FileHandle
    formatter: JsonFormatter = json

    def load(self):
        return list(iter(self))

    def dump(self, value: List[Any]):
        with self.handle.create_text_writer() as writer:
            for item in value:
                writer.write(self.formatter.dumps(item) + "\n")

    def __iter__(self):
        with self.handle.create_text_reader() as reader:
            for line in reader:
                yield self.formatter.loads(line)
