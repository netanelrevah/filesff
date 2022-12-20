from typing import Any, List

try:
    import ujson as json
except ImportError:
    import json

from filesff.formatted_files import FileAccessor


class JsonLinesFile(FileAccessor):
    LINES_FORMATTER = json

    def load(self):
        return list(iter(self))

    def dump(self, values_list: List[Any]):
        writer = self.create_writer()
        for value in values_list:
            writer.write(self.LINES_FORMATTER.dumps(value) + "\n")

    def __iter__(self):
        for line in self.handle.create_unicode_reader():
            yield self.LINES_FORMATTER.loads(line)
