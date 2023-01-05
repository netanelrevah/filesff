from dataclasses import dataclass
from typing import Any, List

from filesff.files_handlers import FileHandle
from filesff.json_files import JsonFormatter

try:
    import ujson as json
except ImportError:
    import json

from filesff.file_accessors import FileAccessor


@dataclass
class JsonLinesFile(FileAccessor):
    handle: FileHandle
    formatter: JsonFormatter = json

    def load(self):
        return list(iter(self))

    def dump(self, values_list: List[Any]):
        writer = self.handle.create_text_writer()
        for value in values_list:
            writer.write(self.formatter.dumps(value) + "\n")

    def __iter__(self):
        for line in self.handle.create_text_reader():
            yield self.formatter.loads(line)
